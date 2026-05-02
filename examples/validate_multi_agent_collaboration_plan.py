#!/usr/bin/env python3
"""Validate Phase 7 v24 multi-agent collaboration plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/multi-agent-collaboration.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v23_8_autonomy_mode",
    "supervisor_required",
    "specialist_roles_required",
    "handoff_contract_required",
    "shared_state_required",
    "single_active_specialist_required",
    "context_filter_required",
    "conflict_resolution_required",
    "handoff_loop_limit_required",
    "operator_escalation_required",
    "audit_event_required",
    "local_simulation_only",
    "no_live_multi_agent_runtime",
    "no_tool_execution",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "role_catalog_required",
    "supervisor_role_required",
    "handoff_allowed_targets_required",
    "handoff_payload_schema_required",
    "context_scope_required",
    "state_owner_required",
    "conflict_policy_required",
    "parallel_agent_block_required",
    "loop_limit_required",
    "autonomy_mode_gate_required",
    "safety_gate_required",
    "budget_gate_required",
    "audit_event_required",
    "trace_id_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "incident_id",
    "trace_id",
    "current_agent",
    "requested_target",
    "allowed_target",
    "autonomy_mode",
    "handoff_count",
    "max_handoffs",
    "context_status",
    "safety_status",
    "budget_status",
    "conflict_status",
    "parallel_requested",
    "decision",
    "next_agent",
    "next_action",
    "audit_event",
}

REQUIRED_DECISIONS = {
    "handoff_to_evidence_agent",
    "handoff_to_safety_agent",
    "handoff_to_budget_agent",
    "handoff_to_response_agent",
    "block_unknown_agent",
    "block_parallel_handoff",
    "block_stale_context",
    "escalate_conflict",
    "stop_handoff_loop",
    "hold_autonomy_mode",
}

REQUIRED_AGENTS = {
    "supervisor_agent",
    "evidence_agent",
    "safety_agent",
    "budget_agent",
    "response_agent",
    "human_operator",
}

REQUIRED_LIVE_CHECKS = {
    "official_multi_agent_framework_review",
    "handoff_contract_review",
    "shared_state_schema_review",
    "role_owner_review",
    "conflict_resolution_runbook",
    "handoff_loop_drill",
    "parallel_execution_policy_review",
    "autonomy_mode_integration_test",
    "multi_agent_observability_dashboard",
    "audit_log_sink",
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


def _require_false_flags(plan: dict[str, object], missing: list[str]) -> None:
    for field in [
        "agent_runtime_started",
        "multi_agent_runtime_started",
        "autonomy_runtime_started",
        "orchestration_runtime_started",
        "workflow_runtime_started",
        "mcp_server_started",
        "tool_calls_executed",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "durable_store_created",
        "persistent_storage_created",
        "approved_for_live_multi_agent",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")


def _require_source_notes(source_notes: object, missing: list[str]) -> None:
    if not isinstance(source_notes, list) or len(source_notes) < 3:
        missing.append("at_least_three_source_notes_required")
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
        if note.get("date_checked") != "2026-04-30":
            missing.append(f"source_note_date_must_be_2026_04_30:{note.get('source')}")
    for url in [
        "https://openai.github.io/openai-agents-python/handoffs/",
        "https://openai.github.io/openai-agents-js/guides/guardrails/",
        "https://docs.langchain.com/oss/python/langchain/multi-agent/index",
        "https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs",
    ]:
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_non_negative_number(value: object, label: str, missing: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        missing.append(f"{label}_must_be_numeric")
    elif value < 0:
        missing.append(f"{label}_must_be_non_negative")


def validate_multi_agent_collaboration_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "multi_agent_collaboration_plan_no_runtime":
        missing.append("mode_must_be_multi_agent_collaboration_plan_no_runtime")
    if plan.get("version") != "v24":
        missing.append("version_must_be_v24")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("collaboration_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("collaboration_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_collaboration_dimension:{dimension}")

    role_catalog = plan.get("role_catalog", [])
    role_ids: set[str] = set()
    role_targets: dict[str, set[str]] = {}
    if not isinstance(role_catalog, list) or len(role_catalog) < 6:
        missing.append("at_least_six_agent_roles_required")
    else:
        for role in role_catalog:
            if not isinstance(role, dict):
                missing.append("role_catalog_item_must_be_object")
                continue
            agent_id = role.get("agent_id")
            if isinstance(agent_id, str):
                role_ids.add(agent_id)
            for field in [
                "agent_id",
                "role",
                "owner",
                "allowed_targets",
                "may_execute_tools",
                "may_call_provider",
                "context_scope",
            ]:
                if field not in role:
                    missing.append(f"role_missing_field:{field}:{agent_id}")
            if not role.get("owner"):
                missing.append(f"role_owner_required:{agent_id}")
            if not isinstance(role.get("allowed_targets"), list):
                missing.append(f"allowed_targets_must_be_list:{agent_id}")
                role_targets[str(agent_id)] = set()
            else:
                role_targets[str(agent_id)] = {str(target) for target in role["allowed_targets"]}
            if role.get("may_execute_tools") is not False:
                missing.append(f"role_may_execute_tools_must_be_false:{agent_id}")
            if role.get("may_call_provider") is not False:
                missing.append(f"role_may_call_provider_must_be_false:{agent_id}")
        for agent_id in sorted(REQUIRED_AGENTS):
            if agent_id not in role_ids:
                missing.append(f"missing_agent_role:{agent_id}")

    contract = plan.get("handoff_contract", {})
    if not isinstance(contract, dict):
        missing.append("handoff_contract_must_be_object")
    else:
        payload_fields = set(contract.get("required_payload_fields", []))
        for field in ["reason", "priority", "state_summary", "requested_output"]:
            if field not in payload_fields:
                missing.append(f"missing_handoff_payload_field:{field}")
        if contract.get("context_filter") != "minimal_role_scoped_state":
            missing.append("context_filter_must_be_minimal_role_scoped_state")
        if contract.get("single_active_specialist") is not True:
            missing.append("single_active_specialist_must_be_true")
        if contract.get("parallel_handoffs_allowed") is not False:
            missing.append("parallel_handoffs_allowed_must_be_false")
        _require_non_negative_number(
            contract.get("max_handoffs_per_incident"), "max_handoffs_per_incident", missing
        )

    state_contract = plan.get("shared_state_contract", {})
    if not isinstance(state_contract, dict):
        missing.append("shared_state_contract_must_be_object")
    else:
        if state_contract.get("state_owner") != "supervisor_agent":
            missing.append("shared_state_owner_must_be_supervisor_agent")
        if state_contract.get("conflict_policy") != "escalate_to_operator":
            missing.append("conflict_policy_must_be_escalate_to_operator")
        required_state_fields = set(state_contract.get("required_fields", []))
        for field in ["incident_id", "trace_id", "active_agent", "handoff_count"]:
            if field not in required_state_fields:
                missing.append(f"missing_shared_state_field:{field}")

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    cases = plan.get("collaboration_cases", [])
    if not isinstance(cases, list) or len(cases) < 10:
        missing.append("at_least_ten_collaboration_cases_required")
    else:
        observed_decisions = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("collaboration_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "case_id",
                "name",
                "incident_id",
                "trace_id",
                "current_agent",
                "requested_target",
                "autonomy_mode",
                "evidence_state",
                "safety_status",
                "budget_status",
                "context_status",
                "conflict_status",
                "parallel_requested",
                "handoff_count",
                "max_handoffs",
                "expected_decision",
                "expected_next_agent",
                "expected_next_action",
            ]:
                if field not in case:
                    missing.append(f"collaboration_case_missing_field:{field}:{name}")
            current_agent = case.get("current_agent")
            requested_target = case.get("requested_target")
            if current_agent not in role_ids:
                missing.append(f"unknown_current_agent:{name}:{current_agent}")
            if requested_target in role_ids and requested_target not in role_targets.get(str(current_agent), set()):
                missing.append(f"target_not_allowed_from_agent:{name}:{current_agent}:{requested_target}")
            if not isinstance(case.get("parallel_requested"), bool):
                missing.append(f"parallel_requested_must_be_boolean:{name}")
            _require_non_negative_number(case.get("handoff_count"), f"handoff_count:{name}", missing)
            _require_non_negative_number(case.get("max_handoffs"), f"max_handoffs:{name}", missing)
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_expected_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_multi_agent", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "multi_agent_collaboration_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "multi_agent_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_multi_agent_collaboration_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
