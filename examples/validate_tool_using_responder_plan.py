#!/usr/bin/env python3
"""Validate Phase 7 v20 tool-using responder plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/tool-using-responder.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "read_only_investigation_only",
    "no_live_user_impact",
    "no_secret_access",
    "no_destructive_action",
    "human_approval_required_for_mutation",
    "local_simulation_only",
}

REQUIRED_STEP_CONTRACT = {
    "plan_before_tool_selection",
    "one_reason_per_tool",
    "read_only_tool_default",
    "tool_input_schema_required",
    "tool_result_schema_required",
    "evidence_required_before_claim",
    "decision_must_reference_evidence",
    "stop_condition_required",
    "audit_record_required",
}

REQUIRED_CONTROLS = {
    "tool_allowlist_required",
    "tool_denylist_required",
    "strict_tool_schema_required",
    "tool_result_validation_required",
    "evidence_ledger_required",
    "secret_redaction_required",
    "human_approval_for_mutation",
    "bounded_query_limits_required",
    "namespace_boundary_required",
    "primary_aois_separation_required",
    "audit_log_required",
    "fallback_runbook_required",
    "stop_condition_required",
    "resource_usage_record_required",
}

REQUIRED_DECISIONS = {
    "answer_with_evidence",
    "gather_more_evidence",
    "request_human_approval",
    "block_and_redact",
    "fallback_to_runbook",
}

REQUIRED_LIVE_CHECKS = {
    "official_tool_calling_docs_review",
    "mcp_security_review",
    "tool_inventory_owner_assigned",
    "tool_schema_tests",
    "tool_result_validation_tests",
    "secret_redaction_test",
    "human_approval_workflow",
    "audit_log_storage_budget",
    "rollback_plan",
    "primary_aois_separation_review",
    "resource_usage_record",
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


def validate_tool_using_responder_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "tool_using_responder_plan_no_runtime":
        missing.append("mode_must_be_tool_using_responder_plan_no_runtime")
    if plan.get("version") != "v20":
        missing.append("version_must_be_v20")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    for field in [
        "agent_runtime_started",
        "tool_calls_executed",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "persistent_storage_created",
        "approved_for_live_agent_execution",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    _require_true_fields(plan.get("responder_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("step_contract"), REQUIRED_STEP_CONTRACT, "step_contract", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    allowed_tools = plan.get("allowed_read_only_tools", [])
    if not isinstance(allowed_tools, list) or len(allowed_tools) < 4:
        missing.append("at_least_four_allowed_read_only_tools_required")
        allowed_names: set[str] = set()
    else:
        allowed_names = set()
        for tool in allowed_tools:
            if not isinstance(tool, dict):
                missing.append("allowed_tool_must_be_object")
                continue
            name = tool.get("name")
            if isinstance(name, str):
                allowed_names.add(name)
            if tool.get("tool_type") != "read_only":
                missing.append(f"tool_must_be_read_only:{name}")
            if tool.get("strict_schema_required") is not True:
                missing.append(f"strict_schema_required_for_tool:{name}")
            if tool.get("produces_evidence") is not True:
                missing.append(f"tool_must_produce_evidence:{name}")
            if not tool.get("allowed_inputs"):
                missing.append(f"allowed_inputs_required:{name}")
            if not tool.get("disallowed_inputs"):
                missing.append(f"disallowed_inputs_required:{name}")

    blocked_tools = plan.get("blocked_tools_without_human_approval", [])
    if not isinstance(blocked_tools, list) or "delete_pod" not in blocked_tools:
        missing.append("blocked_mutating_tools_required")

    thresholds = plan.get("thresholds", {})
    if not isinstance(thresholds, dict):
        missing.append("thresholds_must_be_object")
    else:
        if thresholds.get("minimum_confidence_for_answer") != 0.75:
            missing.append("minimum_confidence_for_answer_must_be_0_75")
        if thresholds.get("minimum_tool_schema_pass_rate") != 1.0:
            missing.append("minimum_tool_schema_pass_rate_must_be_1_0")
        if thresholds.get("max_allowed_secret_findings") != 0:
            missing.append("max_allowed_secret_findings_must_be_zero")
        if thresholds.get("max_mutating_tool_calls_without_approval") != 0:
            missing.append("max_mutating_tool_calls_without_approval_must_be_zero")

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in [
            "max_agent_runtimes_for_lesson",
            "max_tool_calls_for_lesson",
            "max_provider_calls_for_lesson",
            "max_external_network_calls_for_lesson",
            "max_persistent_storage_mb",
            "max_spend_usd",
        ]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    cases = plan.get("incident_cases", [])
    if not isinstance(cases, list) or len(cases) < 5:
        missing.append("at_least_five_incident_cases_required")
    else:
        observed_decisions = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("incident_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "name",
                "incident_id",
                "symptom",
                "severity",
                "planned_tool_sequence",
                "tool_result_schema_valid",
                "evidence_complete",
                "secret_detected",
                "mutating_tool_requested",
                "confidence",
                "expected_decision",
                "expected_next_action",
            ]:
                if field not in case:
                    missing.append(f"incident_case_missing_field:{field}:{name}")
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_case_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)
            sequence = case.get("planned_tool_sequence", [])
            if not isinstance(sequence, list) or not sequence:
                missing.append(f"planned_tool_sequence_required:{name}")
            else:
                for tool_name in sequence:
                    if tool_name not in allowed_names and tool_name not in blocked_tools:
                        missing.append(f"unknown_tool_in_sequence:{name}:{tool_name}")
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_agent_execution", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "tool_using_responder_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_tool_using_responder_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
