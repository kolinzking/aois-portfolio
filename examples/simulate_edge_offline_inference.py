#!/usr/bin/env python3
"""Simulate Phase 10 v32 edge and offline inference decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PLAN_PATH = Path("frontier/aois-p/edge-offline-inference.plan.json")


def _expand_case(defaults: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    expanded = dict(defaults)
    expanded.update(case.get("overrides", {}))
    expanded["case_id"] = case["case_id"]
    expanded["name"] = case["name"]
    return expanded


def _central_fallback_available(case: dict[str, Any]) -> bool:
    return (
        case["fallback_status"] == "central_available"
        and case["connectivity_status"] in {"online", "degraded"}
        and case["data_residency_status"] == "pass"
        and case["privacy_status"] in {"redacted", "none"}
        and case["access_policy_status"] == "pass"
        and case["release_gate_status"] == "pass"
    )


def _resource_failure(
    case: dict[str, Any], device_profile: dict[str, Any] | None
) -> tuple[str, str, str, str] | None:
    if device_profile is None or case["device_profile_status"] not in {"known", "managed"}:
        return (
            "block_unknown_device_profile",
            "register_and_review_device_profile",
            "blocked",
            "edge_device_profile_not_approved",
        )
    if case["model_size_mb"] > case["model_size_budget_mb"]:
        return (
            "block_model_size_budget_exceeded",
            "choose_smaller_or_quantized_model",
            "blocked",
            "model_package_exceeds_target_budget",
        )
    if case["memory_mb"] > case["memory_budget_mb"]:
        return (
            "block_memory_budget_exceeded",
            "resize_model_or_move_target",
            "blocked",
            "projected_memory_exceeds_device_budget",
        )
    if case["compute_budget_status"] != "pass":
        if _central_fallback_available(case):
            return (
                "route_to_central_fallback",
                "route_to_central_fallback",
                "fallback",
                "edge_compute_failed_central_fallback_available",
            )
        return (
            "hold_compute_budget_review",
            "measure_compute_budget",
            "held",
            "compute_budget_not_approved",
        )
    if device_profile["power_sensitive"] is True and case["power_budget_status"] != "pass":
        return (
            "hold_power_budget_review",
            "measure_power_draw",
            "held",
            "power_sensitive_target_needs_power_budget",
        )
    if case["latency_ms"] > case["latency_budget_ms"]:
        return (
            "block_latency_budget_exceeded",
            "reduce_latency_or_route_elsewhere",
            "blocked",
            "projected_latency_exceeds_budget",
        )
    return None


def _decision(
    case: dict[str, Any], device_profiles: dict[str, dict[str, Any]]
) -> tuple[str, str, str, str]:
    if case["data_residency_status"] != "pass":
        return (
            "block_data_residency_violation",
            "choose_residency_compliant_target",
            "blocked",
            "deployment_target_violates_residency_policy",
        )
    if case["privacy_status"] not in {"redacted", "none"}:
        return (
            "block_privacy_unredacted",
            "redact_before_edge_inference",
            "blocked",
            "payload_not_redacted_for_edge_or_sync",
        )
    if case["access_policy_status"] != "pass" or case["release_gate_status"] != "pass":
        return (
            "block_policy_boundary",
            "repair_edge_policy_boundary",
            "blocked",
            "access_or_release_policy_failed",
        )
    if case["update_channel_status"] != "approved":
        return (
            "block_update_channel_missing",
            "configure_signed_update_channel",
            "blocked",
            "approved_update_channel_missing",
        )
    if case["rollback_ready"] is not True:
        return (
            "block_no_rollback",
            "prepare_edge_rollback_plan",
            "blocked",
            "edge_rollback_not_ready",
        )

    target = str(case["deployment_target"])
    if target == "central_cloud":
        if case["connectivity_status"] == "online":
            return (
                "allow_central_cloud_inference",
                "route_to_central_inference",
                "central",
                "central_controls_passed",
            )
        return (
            "hold_compute_budget_review",
            "measure_compute_budget",
            "held",
            "central_target_requires_online_connectivity",
        )

    device_profile = device_profiles.get(str(case["device_class"]))
    resource_failure = _resource_failure(case, device_profile)
    if resource_failure is not None:
        return resource_failure

    if target == "offline_edge":
        if case["cache_status"] != "ready":
            return (
                "hold_missing_offline_cache",
                "prepare_offline_cache",
                "held",
                "offline_cache_not_ready",
            )
        if case["model_freshness_status"] != "fresh":
            return (
                "hold_stale_model",
                "refresh_or_attest_model_version",
                "held",
                "offline_model_freshness_not_current",
            )
        if case["sync_status"] != "ready":
            return (
                "hold_missing_offline_cache",
                "prepare_offline_cache",
                "held",
                "offline_sync_policy_not_ready",
            )
        if case["observability_status"] != "buffered":
            return (
                "hold_observability_buffer_missing",
                "configure_local_telemetry_buffer",
                "held",
                "offline_observability_buffer_missing",
            )
        return (
            "allow_offline_cached_inference",
            "allow_offline_cached_inference",
            "offline",
            "offline_cache_freshness_sync_and_buffers_ready",
        )

    if case["observability_status"] not in {"buffered", "streaming"}:
        return (
            "hold_observability_buffer_missing",
            "configure_local_telemetry_buffer",
            "held",
            "edge_observability_missing",
        )

    return (
        "allow_edge_online_inference",
        "allow_edge_inference",
        "edge_online",
        "edge_online_controls_passed",
    )


def _decide(
    defaults: dict[str, Any],
    raw_case: dict[str, Any],
    device_profiles: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    case = _expand_case(defaults, raw_case)
    decision, operator_action, edge_state, reason = _decision(case, device_profiles)
    expected_decision = str(raw_case["expected_decision"])
    expected_operator_action = str(raw_case["expected_operator_action"])
    expected_edge_state = str(raw_case["expected_edge_state"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "deployment_target": case["deployment_target"],
        "connectivity_status": case["connectivity_status"],
        "device_class": case["device_class"],
        "model_format": case["model_format"],
        "decision": decision,
        "operator_action": operator_action,
        "edge_state": edge_state,
        "expected_decision": expected_decision,
        "expected_operator_action": expected_operator_action,
        "expected_edge_state": expected_edge_state,
        "passed": (
            decision == expected_decision
            and operator_action == expected_operator_action
            and edge_state == expected_edge_state
        ),
        "reasons": [reason],
    }


def simulate_edge_offline_inference() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    defaults = plan["case_defaults"]
    device_profiles = {
        str(item["device_class"]): item for item in plan["device_profiles"]
    }
    decisions = [
        _decide(defaults, case, device_profiles) for case in plan["edge_cases"]
    ]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "edge_offline_inference_simulation_no_runtime",
        "namespace": plan["namespace"],
        "edge_runtime_started": False,
        "offline_model_loaded": False,
        "model_runtime_started": False,
        "model_downloaded": False,
        "model_quantized": False,
        "device_accessed": False,
        "gpu_runtime_started": False,
        "npu_runtime_started": False,
        "camera_started": False,
        "microphone_started": False,
        "media_file_read": False,
        "network_call_made": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_edge_offline_inference()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
