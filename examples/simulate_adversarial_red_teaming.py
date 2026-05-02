#!/usr/bin/env python3
"""Simulate Phase 10 v33 adversarial red teaming decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PLAN_PATH = Path("frontier/aois-p/adversarial-red-teaming.plan.json")

POISONING_CATEGORIES = {
    "supply_chain",
    "poisoning",
    "vector_embedding_weakness",
}


def _expand_case(defaults: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    expanded = dict(defaults)
    expanded.update(case.get("overrides", {}))
    expanded["case_id"] = case["case_id"]
    expanded["name"] = case["name"]
    return expanded


def _escalation_for_category(category: str) -> tuple[str, str, str, str]:
    if category == "prompt_injection":
        return (
            "escalate_direct_prompt_injection",
            "escalate_instruction_boundary_failure",
            "escalated",
            "direct_prompt_injection_control_failed",
        )
    if category == "indirect_prompt_injection":
        return (
            "escalate_indirect_prompt_injection",
            "escalate_retrieved_context_boundary_failure",
            "escalated",
            "indirect_prompt_injection_control_failed",
        )
    if category == "system_prompt_leakage":
        return (
            "escalate_system_prompt_leakage",
            "escalate_prompt_secret_boundary_failure",
            "escalated",
            "system_prompt_leakage_control_failed",
        )
    if category == "sensitive_information_disclosure":
        return (
            "escalate_sensitive_information_disclosure",
            "escalate_sensitive_data_boundary_failure",
            "escalated",
            "sensitive_information_control_failed",
        )
    if category in POISONING_CATEGORIES:
        return (
            "escalate_rag_or_data_poisoning",
            "escalate_poisoning_control_failure",
            "escalated",
            "poisoning_or_retrieval_control_failed",
        )
    if category == "excessive_agency":
        return (
            "escalate_excessive_agency",
            "escalate_agent_tool_boundary_failure",
            "escalated",
            "excessive_agency_control_failed",
        )
    if category == "output_handling":
        return (
            "escalate_improper_output_handling",
            "escalate_output_boundary_failure",
            "escalated",
            "output_handling_control_failed",
        )
    if category == "unbounded_consumption":
        return (
            "escalate_unbounded_consumption",
            "escalate_runtime_budget_failure",
            "escalated",
            "runtime_budget_control_failed",
        )
    if category == "edge_cache_poisoning":
        return (
            "escalate_edge_cache_poisoning",
            "escalate_edge_cache_integrity_failure",
            "escalated",
            "edge_cache_integrity_control_failed",
        )
    if category == "fallback_abuse":
        return (
            "escalate_fallback_abuse",
            "escalate_fallback_policy_failure",
            "escalated",
            "fallback_policy_control_failed",
        )
    return (
        "escalate_policy_confusion",
        "escalate_policy_order_failure",
        "escalated",
        "policy_order_control_failed",
    )


def _decision(case: dict[str, Any]) -> tuple[str, str, str, str]:
    if (
        case["authorization_status"] != "approved"
        or case["rules_of_engagement_status"] != "approved"
    ):
        return (
            "block_missing_authorization",
            "obtain_red_team_authorization",
            "blocked",
            "authorization_or_rules_of_engagement_missing",
        )
    if case["scope_status"] != "in_scope":
        return (
            "block_out_of_scope_target",
            "reduce_to_approved_scope",
            "blocked",
            "scenario_outside_approved_scope",
        )
    if case["target_status"] != "local_synthetic":
        return (
            "block_live_target_requested",
            "replace_with_local_synthetic_target",
            "blocked",
            "live_or_external_target_requested",
        )
    if case["payload_safety_status"] != "sanitized":
        return (
            "block_unsanitized_payload",
            "sanitize_or_remove_payload",
            "blocked",
            "payload_not_sanitized",
        )
    if case["policy_status"] != "pass":
        return (
            "block_policy_boundary",
            "repair_red_team_policy_boundary",
            "blocked",
            "policy_boundary_failed",
        )
    if case["tool_permission_status"] != "least_privilege":
        return (
            "block_tool_permission_overreach",
            "reduce_tool_permissions",
            "blocked",
            "tool_permission_overreach",
        )
    if case["data_boundary_status"] != "pass":
        return (
            "block_data_boundary_violation",
            "repair_data_boundary",
            "blocked",
            "tenant_privacy_residency_or_secret_boundary_failed",
        )
    if case["telemetry_status"] != "captured":
        return (
            "hold_missing_telemetry",
            "instrument_red_team_evidence",
            "held",
            "telemetry_not_captured",
        )
    if case["evidence_status"] != "present":
        return (
            "hold_missing_evidence",
            "collect_sanitized_observation_evidence",
            "held",
            "sanitized_evidence_missing",
        )

    if case["observed_behavior_status"] == "control_failed":
        if case["mitigation_status"] != "ready":
            return (
                "hold_missing_mitigation",
                "assign_mitigation_owner",
                "held",
                "confirmed_failure_missing_mitigation_owner",
            )
        if case["regression_status"] != "ready":
            return (
                "require_regression_test",
                "create_regression_case",
                "held",
                "confirmed_failure_missing_regression_case",
            )
        return _escalation_for_category(str(case["threat_category"]))

    return (
        "allow_sanitized_red_team_case_recorded",
        "record_sanitized_red_team_result",
        "recorded",
        "sanitized_red_team_case_passed_controls",
    )


def _decide(defaults: dict[str, Any], raw_case: dict[str, Any]) -> dict[str, Any]:
    case = _expand_case(defaults, raw_case)
    decision, operator_action, red_team_state, reason = _decision(case)
    expected_decision = str(raw_case["expected_decision"])
    expected_operator_action = str(raw_case["expected_operator_action"])
    expected_red_team_state = str(raw_case["expected_red_team_state"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "scenario_id": case["scenario_id"],
        "threat_category": case["threat_category"],
        "attack_surface": case["attack_surface"],
        "modality": case["modality"],
        "deployment_target": case["deployment_target"],
        "decision": decision,
        "operator_action": operator_action,
        "red_team_state": red_team_state,
        "expected_decision": expected_decision,
        "expected_operator_action": expected_operator_action,
        "expected_red_team_state": expected_red_team_state,
        "passed": (
            decision == expected_decision
            and operator_action == expected_operator_action
            and red_team_state == expected_red_team_state
        ),
        "reasons": [reason],
    }


def simulate_adversarial_red_teaming() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    defaults = plan["case_defaults"]
    decisions = [_decide(defaults, case) for case in plan["red_team_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "adversarial_red_teaming_simulation_no_runtime",
        "namespace": plan["namespace"],
        "red_team_run_started": False,
        "live_model_called": False,
        "adversarial_payload_executed": False,
        "exploit_attempted": False,
        "jailbreak_payload_generated": False,
        "prompt_injection_payload_generated": False,
        "tool_call_made": False,
        "network_call_made": False,
        "provider_call_made": False,
        "command_executed": False,
        "file_write_performed": False,
        "secret_accessed": False,
        "data_exfiltrated": False,
        "exploit_artifact_persisted": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_adversarial_red_teaming()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
