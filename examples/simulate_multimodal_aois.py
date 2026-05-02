#!/usr/bin/env python3
"""Simulate Phase 10 v31 multimodal AOIS decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PLAN_PATH = Path("frontier/aois-p/multimodal-aois.plan.json")
MIN_CONFIDENCE_FOR_ACTION = 0.75


def _expand_case(defaults: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    expanded = dict(defaults)
    expanded.update(case.get("overrides", {}))
    expanded["case_id"] = case["case_id"]
    expanded["name"] = case["name"]
    return expanded


def _decision(
    case: dict[str, Any], modalities: dict[str, dict[str, Any]]
) -> tuple[str, str, str, str]:
    modality = modalities.get(str(case["modality"]))
    if modality is None:
        return (
            "block_unknown_modality",
            "reject_unknown_modality",
            "blocked",
            "modality_not_in_catalog",
        )
    if case["media_type"] not in modality["allowed_media_types"]:
        return (
            "block_unsupported_media_type",
            "reject_unsupported_media_type",
            "blocked",
            "media_type_not_allowlisted_for_modality",
        )
    if case["file_validation_status"] != "pass":
        return (
            "block_file_validation_failed",
            "quarantine_media_before_analysis",
            "blocked",
            "file_signature_or_content_validation_failed",
        )
    if case["size_status"] != "pass":
        return (
            "block_size_limit_exceeded",
            "request_smaller_or_sampled_media",
            "blocked",
            "media_size_exceeded_limit",
        )
    if case["consent_status"] != "present":
        return (
            "block_missing_consent",
            "obtain_media_intake_consent",
            "blocked",
            "media_intake_consent_missing",
        )
    if case["pii_status"] not in {"none", "redacted"}:
        return (
            "block_pii_unredacted",
            "redact_sensitive_media_content",
            "blocked",
            "sensitive_media_content_not_redacted",
        )
    if (
        modality["requires_accessibility_alternative"] is True
        and case["accessibility_alternative_status"] != "present"
    ):
        return (
            "block_missing_accessibility_alternative",
            "add_text_alternative_or_description",
            "blocked",
            "required_text_alternative_missing",
        )
    if modality["requires_transcript"] is True and case["transcript_status"] != "present":
        return (
            "block_missing_transcript",
            "add_transcript_or_extracted_text",
            "blocked",
            "required_transcript_or_extracted_text_missing",
        )
    if case["modality_alignment_status"] != "pass":
        return (
            "block_cross_modal_mismatch",
            "investigate_cross_modal_conflict",
            "blocked",
            "cross_modal_signals_conflict",
        )
    if case["policy_status"] != "pass":
        return (
            "block_policy_boundary",
            "repair_multimodal_policy_boundary",
            "blocked",
            "access_tenancy_safety_or_release_policy_failed",
        )
    if case["provider_status"] != "available" and case["fallback_available"] is True:
        return (
            "route_to_text_fallback",
            "use_accessible_text_fallback",
            "fallback",
            "multimodal_provider_unavailable_text_fallback_available",
        )
    if case["evidence_status"] != "present":
        return (
            "hold_missing_evidence",
            "collect_multimodal_evidence",
            "held",
            "multimodal_evidence_missing",
        )
    if float(case["confidence"]) < MIN_CONFIDENCE_FOR_ACTION:
        return (
            "hold_low_confidence",
            "route_to_human_review",
            "held",
            "confidence_below_multimodal_action_threshold",
        )

    modality_name = str(case["modality"])
    if modality_name == "image":
        return (
            "allow_image_analysis",
            "render_image_evidence_summary",
            "allowed",
            "image_multimodal_checks_passed",
        )
    if modality_name == "audio":
        return (
            "allow_audio_analysis",
            "render_audio_transcript_summary",
            "allowed",
            "audio_multimodal_checks_passed",
        )
    if modality_name == "video":
        return (
            "allow_video_analysis",
            "render_video_scene_summary",
            "allowed",
            "video_multimodal_checks_passed",
        )
    return (
        "allow_document_analysis",
        "render_document_evidence_summary",
        "allowed",
        "document_multimodal_checks_passed",
    )


def _decide(
    defaults: dict[str, Any],
    raw_case: dict[str, Any],
    modalities: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    case = _expand_case(defaults, raw_case)
    decision, operator_action, multimodal_state, reason = _decision(case, modalities)
    expected_decision = str(raw_case["expected_decision"])
    expected_operator_action = str(raw_case["expected_operator_action"])
    expected_multimodal_state = str(raw_case["expected_multimodal_state"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "modality": case["modality"],
        "media_type": case["media_type"],
        "decision": decision,
        "operator_action": operator_action,
        "multimodal_state": multimodal_state,
        "expected_decision": expected_decision,
        "expected_operator_action": expected_operator_action,
        "expected_multimodal_state": expected_multimodal_state,
        "passed": (
            decision == expected_decision
            and operator_action == expected_operator_action
            and multimodal_state == expected_multimodal_state
        ),
        "reasons": [reason],
    }


def simulate_multimodal_aois() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    defaults = plan["case_defaults"]
    modalities = {str(item["modality"]): item for item in plan["modality_catalog"]}
    decisions = [
        _decide(defaults, case, modalities) for case in plan["multimodal_cases"]
    ]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "multimodal_aois_simulation_no_runtime",
        "namespace": plan["namespace"],
        "multimodal_runtime_started": False,
        "model_runtime_started": False,
        "vision_model_called": False,
        "audio_model_called": False,
        "video_model_called": False,
        "ocr_engine_started": False,
        "transcription_engine_started": False,
        "camera_started": False,
        "microphone_started": False,
        "media_file_read": False,
        "file_uploaded": False,
        "media_downloaded": False,
        "media_processed": False,
        "network_call_made": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_multimodal_aois()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
