#!/usr/bin/env python3
"""Validate Phase 10 v31 multimodal AOIS plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("frontier/aois-p/multimodal-aois.plan.json")

REQUIRED_FALSE_FLAGS = {
    "multimodal_runtime_started",
    "model_runtime_started",
    "vision_model_called",
    "audio_model_called",
    "video_model_called",
    "ocr_engine_started",
    "transcription_engine_started",
    "camera_started",
    "microphone_started",
    "media_file_read",
    "file_uploaded",
    "media_downloaded",
    "media_processed",
    "network_call_made",
    "provider_call_made",
    "tool_calls_executed",
    "command_executed",
    "file_write_performed",
    "external_network_required_for_this_lesson",
    "persistent_storage_created",
    "approved_for_live_multimodal",
}

REQUIRED_SCOPE = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_phase9_platform_controls",
    "local_simulation_only",
    "multimodal_contract_only",
    "no_live_media_ingest",
    "no_live_camera",
    "no_live_microphone",
    "no_media_file_read",
    "no_model_runtime",
    "no_ocr_runtime",
    "no_transcription_runtime",
    "no_network_call",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "modality_declared_required",
    "media_type_allowlist_required",
    "file_signature_validation_required",
    "file_size_limit_required",
    "source_trust_required",
    "consent_required",
    "pii_review_required",
    "redaction_required",
    "accessibility_alternative_required",
    "transcript_required_for_time_based_media",
    "cross_modal_consistency_required",
    "evidence_required",
    "confidence_required",
    "model_route_required",
    "text_fallback_required",
    "observability_trace_required",
    "policy_access_required",
    "release_integration_required",
    "platform_integration_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "incident_id",
    "trace_id",
    "modality",
    "media_type",
    "source_trust",
    "file_validation_status",
    "size_status",
    "consent_status",
    "pii_status",
    "accessibility_alternative_status",
    "transcript_status",
    "modality_alignment_status",
    "evidence_status",
    "confidence",
    "model_route_status",
    "provider_status",
    "policy_status",
    "fallback_available",
    "multimodal_decision",
    "operator_action",
}

REQUIRED_MODALITIES = {"image", "audio", "video", "document"}

REQUIRED_DECISIONS = {
    "allow_image_analysis",
    "allow_audio_analysis",
    "allow_video_analysis",
    "allow_document_analysis",
    "block_unknown_modality",
    "block_unsupported_media_type",
    "block_file_validation_failed",
    "block_size_limit_exceeded",
    "block_missing_consent",
    "block_pii_unredacted",
    "block_missing_accessibility_alternative",
    "block_missing_transcript",
    "block_cross_modal_mismatch",
    "hold_missing_evidence",
    "hold_low_confidence",
    "route_to_text_fallback",
    "block_policy_boundary",
}

REQUIRED_SOURCES = {
    "https://www.w3.org/TR/WCAG22/",
    "https://www.w3.org/TR/media-accessibility-reqs/",
    "https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html",
    "https://opentelemetry.io/docs/concepts/semantic-conventions/",
    "https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook",
}

REQUIRED_LIVE_CHECKS = {
    "media_intake_review",
    "file_upload_security_review",
    "modality_catalog_review",
    "consent_and_privacy_review",
    "pii_redaction_review",
    "accessibility_alternative_review",
    "transcript_review",
    "cross_modal_consistency_review",
    "confidence_threshold_review",
    "model_route_review",
    "text_fallback_review",
    "observability_review",
    "policy_access_review",
    "release_integration_review",
    "platform_integration_review",
    "primary_aois_separation_review",
    "resource_usage_record",
}

REQUIRED_DEFAULTS = {
    "modality": "image",
    "media_type": "image/png",
    "source_trust": "known_operator",
    "file_validation_status": "pass",
    "size_status": "pass",
    "consent_status": "present",
    "pii_status": "redacted",
    "accessibility_alternative_status": "present",
    "transcript_status": "not_required",
    "modality_alignment_status": "pass",
    "evidence_status": "present",
    "model_route_status": "approved",
    "provider_status": "available",
    "policy_status": "pass",
    "fallback_available": True,
}


def _require_true_fields(
    section: object, required: set[str], label: str, missing: list[str]
) -> None:
    if not isinstance(section, dict):
        missing.append(f"{label}_must_be_object")
        return
    for field in sorted(required):
        if section.get(field) is not True:
            missing.append(f"missing_{label}:{field}")


def _require_false_flags(plan: dict[str, object], missing: list[str]) -> None:
    for field in sorted(REQUIRED_FALSE_FLAGS):
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")


def _require_source_notes(source_notes: object, missing: list[str]) -> None:
    if not isinstance(source_notes, list) or len(source_notes) < len(REQUIRED_SOURCES):
        missing.append("complete_source_notes_required")
        return

    urls = set()
    for note in source_notes:
        if not isinstance(note, dict):
            missing.append("source_note_must_be_object")
            continue
        for field in ["source", "url", "date_checked", "supports"]:
            if not note.get(field):
                missing.append(f"source_note_missing_field:{field}")
        if isinstance(note.get("url"), str):
            urls.add(str(note["url"]))
        if note.get("date_checked") != "2026-05-01":
            missing.append(f"source_note_date_must_be_2026_05_01:{note.get('source')}")

    for url in sorted(REQUIRED_SOURCES):
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_modality_catalog(plan: dict[str, object], missing: list[str]) -> None:
    modalities = plan.get("modality_catalog", [])
    observed: set[str] = set()
    if not isinstance(modalities, list) or len(modalities) < len(REQUIRED_MODALITIES):
        missing.append("complete_modality_catalog_required")
        return
    for modality in modalities:
        if not isinstance(modality, dict):
            missing.append("modality_catalog_entry_must_be_object")
            continue
        modality_id = modality.get("modality")
        if isinstance(modality_id, str):
            observed.add(modality_id)
        for field in [
            "modality",
            "allowed_media_types",
            "max_bytes",
            "requires_accessibility_alternative",
            "requires_transcript",
            "primary_risks",
        ]:
            if field not in modality:
                missing.append(f"modality_missing_field:{field}")
        if not isinstance(modality.get("allowed_media_types"), list) or not modality["allowed_media_types"]:
            missing.append(f"modality_allowed_media_types_required:{modality_id}")
        if not isinstance(modality.get("max_bytes"), int) or modality["max_bytes"] <= 0:
            missing.append(f"modality_max_bytes_required:{modality_id}")
        if not isinstance(modality.get("primary_risks"), list) or not modality["primary_risks"]:
            missing.append(f"modality_primary_risks_required:{modality_id}")

    for modality_id in sorted(REQUIRED_MODALITIES):
        if modality_id not in observed:
            missing.append(f"missing_modality:{modality_id}")


def _require_defaults(defaults: object, missing: list[str]) -> None:
    if not isinstance(defaults, dict):
        missing.append("case_defaults_must_be_object")
        return
    for field, expected in REQUIRED_DEFAULTS.items():
        if defaults.get(field) != expected:
            missing.append(f"case_default_mismatch:{field}")
    for field in ["incident_id", "trace_id", "confidence"]:
        if field not in defaults:
            missing.append(f"case_default_required:{field}")
    confidence = defaults.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
        missing.append("case_default_confidence_must_be_numeric")
    elif not 0 <= confidence <= 1:
        missing.append("case_default_confidence_must_be_between_0_and_1")


def _require_cases(plan: dict[str, object], missing: list[str]) -> None:
    cases = plan.get("multimodal_cases", [])
    observed_decisions: set[str] = set()
    required_case_fields = {
        "case_id",
        "name",
        "expected_decision",
        "expected_operator_action",
        "expected_multimodal_state",
    }
    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("multimodal_case_for_each_decision_required")
        return

    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            missing.append("multimodal_case_must_be_object")
            continue
        case_id = str(case.get("case_id", ""))
        if not case_id:
            missing.append("multimodal_case_id_required")
        elif case_id in case_ids:
            missing.append(f"duplicate_multimodal_case_id:{case_id}")
        case_ids.add(case_id)

        for field in sorted(required_case_fields):
            if field not in case:
                missing.append(f"multimodal_case_missing_field:{case_id}:{field}")
        decision = case.get("expected_decision")
        if isinstance(decision, str):
            observed_decisions.add(decision)
        if decision not in REQUIRED_DECISIONS:
            missing.append(f"unexpected_expected_decision:{case_id}:{decision}")
        if "overrides" in case and not isinstance(case["overrides"], dict):
            missing.append(f"multimodal_case_overrides_must_be_object:{case_id}")

    for decision in sorted(REQUIRED_DECISIONS):
        if decision not in observed_decisions:
            missing.append(f"missing_multimodal_case_for_decision:{decision}")


def validate_multimodal_aois_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "multimodal_aois_plan_no_runtime":
        missing.append("mode_must_be_multimodal_aois_plan_no_runtime")
    if plan.get("version") != "v31":
        missing.append("version_must_be_v31")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("multimodal_scope"), REQUIRED_SCOPE, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("multimodal_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_multimodal_dimension:{dimension}")

    decision_gates = plan.get("decision_gates", {})
    if not isinstance(decision_gates, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if not decision_gates.get(decision):
                missing.append(f"missing_decision_gate:{decision}")

    _require_modality_catalog(plan, missing)
    _require_defaults(plan.get("case_defaults"), missing)
    _require_cases(plan, missing)

    live_checks = set(plan.get("required_before_live_multimodal", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_multimodal_check:{check}")

    return {
        "plan": str(PLAN_PATH),
        "mode": plan.get("mode"),
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_multimodal_aois_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
