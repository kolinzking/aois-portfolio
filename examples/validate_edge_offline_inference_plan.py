#!/usr/bin/env python3
"""Validate Phase 10 v32 edge and offline inference plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("frontier/aois-p/edge-offline-inference.plan.json")

REQUIRED_FALSE_FLAGS = {
    "edge_runtime_started",
    "offline_model_loaded",
    "model_runtime_started",
    "model_downloaded",
    "model_quantized",
    "device_accessed",
    "gpu_runtime_started",
    "npu_runtime_started",
    "camera_started",
    "microphone_started",
    "media_file_read",
    "network_call_made",
    "provider_call_made",
    "tool_calls_executed",
    "command_executed",
    "file_write_performed",
    "external_network_required_for_this_lesson",
    "persistent_storage_created",
    "approved_for_live_edge",
}

REQUIRED_SCOPE = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v31_multimodal_contract",
    "uses_phase9_release_controls",
    "local_simulation_only",
    "deployment_contract_only",
    "no_live_device",
    "no_live_model_load",
    "no_hardware_access",
    "no_gpu_access",
    "no_npu_access",
    "no_media_capture",
    "no_network_call",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "deployment_target_required",
    "device_profile_required",
    "connectivity_profile_required",
    "model_format_required",
    "model_size_budget_required",
    "quantization_review_required",
    "memory_budget_required",
    "compute_budget_required",
    "power_budget_required",
    "latency_budget_required",
    "offline_cache_required",
    "sync_policy_required",
    "stale_model_indicator_required",
    "data_residency_required",
    "privacy_redaction_required",
    "fallback_required",
    "observability_buffer_required",
    "update_channel_required",
    "rollback_required",
    "access_policy_required",
    "release_gate_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "incident_id",
    "trace_id",
    "deployment_target",
    "connectivity_status",
    "device_class",
    "device_profile_status",
    "model_format",
    "model_size_mb",
    "model_size_budget_mb",
    "quantization_status",
    "memory_mb",
    "memory_budget_mb",
    "compute_budget_status",
    "power_budget_status",
    "latency_ms",
    "latency_budget_ms",
    "cache_status",
    "sync_status",
    "model_freshness_status",
    "data_residency_status",
    "privacy_status",
    "fallback_status",
    "observability_status",
    "update_channel_status",
    "rollback_ready",
    "access_policy_status",
    "release_gate_status",
    "edge_decision",
    "operator_action",
}

REQUIRED_TARGETS = {"central_cloud", "edge_online", "offline_edge"}
REQUIRED_DEVICE_CLASSES = {
    "workstation_edge",
    "gateway_edge",
    "mobile_edge",
    "micro_edge",
}

REQUIRED_DECISIONS = {
    "allow_central_cloud_inference",
    "allow_edge_online_inference",
    "allow_offline_cached_inference",
    "block_unknown_device_profile",
    "block_model_size_budget_exceeded",
    "block_memory_budget_exceeded",
    "hold_compute_budget_review",
    "hold_power_budget_review",
    "block_latency_budget_exceeded",
    "hold_missing_offline_cache",
    "hold_stale_model",
    "block_data_residency_violation",
    "block_privacy_unredacted",
    "route_to_central_fallback",
    "hold_observability_buffer_missing",
    "block_update_channel_missing",
    "block_no_rollback",
    "block_policy_boundary",
}

REQUIRED_SOURCES = {
    "https://onnxruntime.ai/docs/",
    "https://ai.google.dev/edge/litert/",
    "https://kubeedge.io/",
    "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/",
    "https://opentelemetry.io/docs/collector/resiliency/",
    "https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook",
}

REQUIRED_LIVE_CHECKS = {
    "device_profile_review",
    "deployment_target_review",
    "connectivity_profile_review",
    "runtime_and_model_format_review",
    "model_size_budget_review",
    "quantization_review",
    "memory_budget_review",
    "compute_budget_review",
    "power_budget_review",
    "latency_budget_review",
    "offline_cache_review",
    "sync_policy_review",
    "model_freshness_review",
    "data_residency_review",
    "privacy_redaction_review",
    "fallback_review",
    "observability_buffer_review",
    "update_channel_review",
    "rollback_review",
    "access_policy_review",
    "release_gate_review",
    "primary_aois_separation_review",
    "resource_usage_record",
}

REQUIRED_DEFAULTS = {
    "deployment_target": "edge_online",
    "connectivity_status": "online",
    "device_class": "gateway_edge",
    "device_profile_status": "known",
    "model_format": "onnx",
    "model_size_mb": 192,
    "model_size_budget_mb": 512,
    "quantization_status": "reviewed",
    "memory_mb": 768,
    "memory_budget_mb": 2048,
    "compute_budget_status": "pass",
    "power_budget_status": "pass",
    "latency_ms": 420,
    "latency_budget_ms": 900,
    "cache_status": "ready",
    "sync_status": "ready",
    "model_freshness_status": "fresh",
    "data_residency_status": "pass",
    "privacy_status": "redacted",
    "fallback_status": "central_available",
    "observability_status": "buffered",
    "update_channel_status": "approved",
    "rollback_ready": True,
    "access_policy_status": "pass",
    "release_gate_status": "pass",
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


def _require_targets(plan: dict[str, object], missing: list[str]) -> None:
    targets = plan.get("deployment_targets", [])
    observed: set[str] = set()
    if not isinstance(targets, list) or len(targets) < len(REQUIRED_TARGETS):
        missing.append("complete_deployment_targets_required")
        return
    for target in targets:
        if not isinstance(target, dict):
            missing.append("deployment_target_must_be_object")
            continue
        target_id = target.get("target")
        if isinstance(target_id, str):
            observed.add(target_id)
        for field in [
            "target",
            "allowed_connectivity",
            "primary_constraints",
            "default_operator_action",
        ]:
            if field not in target:
                missing.append(f"deployment_target_missing_field:{field}")
        if not isinstance(target.get("allowed_connectivity"), list) or not target["allowed_connectivity"]:
            missing.append(f"deployment_target_connectivity_required:{target_id}")
        if not isinstance(target.get("primary_constraints"), list) or not target["primary_constraints"]:
            missing.append(f"deployment_target_constraints_required:{target_id}")

    for target_id in sorted(REQUIRED_TARGETS):
        if target_id not in observed:
            missing.append(f"missing_deployment_target:{target_id}")


def _require_device_profiles(plan: dict[str, object], missing: list[str]) -> None:
    profiles = plan.get("device_profiles", [])
    observed: set[str] = set()
    if not isinstance(profiles, list) or len(profiles) < len(REQUIRED_DEVICE_CLASSES):
        missing.append("complete_device_profiles_required")
        return
    for profile in profiles:
        if not isinstance(profile, dict):
            missing.append("device_profile_must_be_object")
            continue
        device_class = profile.get("device_class")
        if isinstance(device_class, str):
            observed.add(device_class)
        for field in [
            "device_class",
            "max_model_size_mb",
            "memory_budget_mb",
            "latency_budget_ms",
            "requires_quantization",
            "power_sensitive",
        ]:
            if field not in profile:
                missing.append(f"device_profile_missing_field:{field}")
        for numeric_field in [
            "max_model_size_mb",
            "memory_budget_mb",
            "latency_budget_ms",
        ]:
            value = profile.get(numeric_field)
            if not isinstance(value, int) or value <= 0:
                missing.append(f"device_profile_positive_int_required:{device_class}:{numeric_field}")

    for device_class in sorted(REQUIRED_DEVICE_CLASSES):
        if device_class not in observed:
            missing.append(f"missing_device_profile:{device_class}")


def _require_defaults(defaults: object, missing: list[str]) -> None:
    if not isinstance(defaults, dict):
        missing.append("case_defaults_must_be_object")
        return
    for field, expected in REQUIRED_DEFAULTS.items():
        if defaults.get(field) != expected:
            missing.append(f"case_default_mismatch:{field}")
    for field in ["incident_id", "trace_id"]:
        if field not in defaults:
            missing.append(f"case_default_required:{field}")


def _require_cases(plan: dict[str, object], missing: list[str]) -> None:
    cases = plan.get("edge_cases", [])
    observed_decisions: set[str] = set()
    required_case_fields = {
        "case_id",
        "name",
        "expected_decision",
        "expected_operator_action",
        "expected_edge_state",
    }
    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("edge_case_for_each_decision_required")
        return

    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            missing.append("edge_case_must_be_object")
            continue
        case_id = str(case.get("case_id", ""))
        if not case_id:
            missing.append("edge_case_id_required")
        elif case_id in case_ids:
            missing.append(f"duplicate_edge_case_id:{case_id}")
        case_ids.add(case_id)

        for field in sorted(required_case_fields):
            if field not in case:
                missing.append(f"edge_case_missing_field:{case_id}:{field}")
        decision = case.get("expected_decision")
        if isinstance(decision, str):
            observed_decisions.add(decision)
        if decision not in REQUIRED_DECISIONS:
            missing.append(f"unexpected_expected_decision:{case_id}:{decision}")
        if "overrides" in case and not isinstance(case["overrides"], dict):
            missing.append(f"edge_case_overrides_must_be_object:{case_id}")

    for decision in sorted(REQUIRED_DECISIONS):
        if decision not in observed_decisions:
            missing.append(f"missing_edge_case_for_decision:{decision}")


def validate_edge_offline_inference_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "edge_offline_inference_plan_no_runtime":
        missing.append("mode_must_be_edge_offline_inference_plan_no_runtime")
    if plan.get("version") != "v32":
        missing.append("version_must_be_v32")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("edge_scope"), REQUIRED_SCOPE, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("edge_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_edge_dimension:{dimension}")

    decision_gates = plan.get("decision_gates", {})
    if not isinstance(decision_gates, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if not decision_gates.get(decision):
                missing.append(f"missing_decision_gate:{decision}")

    _require_targets(plan, missing)
    _require_device_profiles(plan, missing)
    _require_defaults(plan.get("case_defaults"), missing)
    _require_cases(plan, missing)

    live_checks = set(plan.get("required_before_live_edge", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_edge_check:{check}")

    return {
        "plan": str(PLAN_PATH),
        "mode": plan.get("mode"),
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_edge_offline_inference_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
