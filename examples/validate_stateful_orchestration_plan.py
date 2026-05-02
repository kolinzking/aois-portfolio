#!/usr/bin/env python3
"""Validate Phase 7 v23 stateful orchestration loop plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/stateful-orchestration.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v20_2_route_decisions",
    "uses_v21_tool_registry_results",
    "uses_v22_workflow_state",
    "state_snapshot_required",
    "ordered_decision_rules_required",
    "loop_guard_required",
    "state_change_required",
    "stop_conditions_required",
    "approval_wait_respected",
    "registry_blocks_terminal",
    "budget_stop_required",
    "local_simulation_only",
    "no_live_orchestration_runtime",
    "no_tool_execution",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "state_schema_required",
    "decision_precedence_required",
    "max_iterations_required",
    "state_hash_required",
    "no_progress_stop_required",
    "terminal_state_stop_required",
    "approval_wait_stop_required",
    "registry_block_stop_required",
    "budget_reserve_required",
    "allowed_next_actions_required",
    "action_owner_required",
    "audit_event_required",
    "trace_id_required",
    "workflow_checkpoint_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "loop_id",
    "workflow_id",
    "incident_id",
    "trace_id",
    "current_state",
    "route_decision",
    "registry_decision",
    "approval_status",
    "iteration",
    "max_iterations",
    "state_hash",
    "state_changed",
    "budget_remaining_units",
    "next_action",
    "stop_reason",
    "audit_event",
    "terminal_status",
}

REQUIRED_DECISIONS = {
    "stop_terminal_state",
    "stop_iteration_limit",
    "stop_no_progress",
    "stop_budget_reserve",
    "stop_registry_block",
    "wait_for_approval",
    "resume_after_approval",
    "plan_read_only_evidence",
    "prepare_answer",
    "close_workflow",
}

REQUIRED_LIVE_CHECKS = {
    "official_orchestration_framework_review",
    "loop_policy_owner_review",
    "state_schema_review",
    "state_hash_collision_review",
    "max_iteration_policy_review",
    "no_progress_detector_review",
    "workflow_runtime_integration_test",
    "tool_registry_integration_test",
    "cost_budget_integration_test",
    "approval_wait_integration_test",
    "orchestration_observability_dashboard",
    "audit_log_sink",
    "primary_aois_separation_review",
    "resource_usage_record",
}

VALID_ROUTE_DECISIONS = {
    "route_small_model_no_tool",
    "route_read_only_tool",
    "route_high_severity_full_investigation",
}
VALID_REGISTRY_DECISIONS = {
    "allow_no_tool_route",
    "allow_read_only_tool_plan",
    "require_human_approval",
    "block_unregistered_tool",
    "block_untrusted_server",
    "block_side_effecting_tool",
    "block_disabled_tool",
}
VALID_ACTIONS = {
    "wait_for_approval",
    "record_evidence_plan",
    "prepare_answer",
    "close_workflow",
    "stop",
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
        "orchestration_runtime_started",
        "workflow_runtime_started",
        "mcp_server_started",
        "tool_calls_executed",
        "provider_call_made",
        "durable_store_created",
        "persistent_storage_created",
        "external_network_required_for_this_lesson",
        "approved_for_live_orchestration",
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
        if note.get("date_checked") != "2026-04-29":
            missing.append(f"source_note_date_must_be_2026_04_29:{note.get('source')}")
    for url in [
        "https://docs.langchain.com/oss/python/langgraph/overview",
        "https://docs.langchain.com/oss/python/langgraph/workflows-agents",
        "https://docs.temporal.io/workflow-definition",
    ]:
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_non_negative_number(value: object, label: str, missing: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        missing.append(f"{label}_must_be_numeric")
    elif value < 0:
        missing.append(f"{label}_must_be_non_negative")


def validate_stateful_orchestration_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "stateful_orchestration_loop_plan_no_runtime":
        missing.append("mode_must_be_stateful_orchestration_loop_plan_no_runtime")
    if plan.get("version") != "v23":
        missing.append("version_must_be_v23")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("orchestration_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("orchestration_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_orchestration_dimension:{dimension}")

    loop_policy = plan.get("loop_policy", {})
    if not isinstance(loop_policy, dict):
        missing.append("loop_policy_must_be_object")
    else:
        if loop_policy.get("max_iterations") != 5:
            missing.append("max_iterations_must_be_5")
        if loop_policy.get("min_budget_reserve_units") != 0.5:
            missing.append("min_budget_reserve_units_must_be_0_5")
        if loop_policy.get("state_change_required_between_iterations") is not True:
            missing.append("state_change_required_between_iterations_must_be_true")
        precedence = loop_policy.get("decision_precedence", [])
        if not isinstance(precedence, list):
            missing.append("decision_precedence_must_be_list")
        else:
            if precedence[:5] != [
                "stop_terminal_state",
                "stop_iteration_limit",
                "stop_no_progress",
                "stop_budget_reserve",
                "stop_registry_block",
            ]:
                missing.append("stop_conditions_must_precede_actions")
            for decision in sorted(REQUIRED_DECISIONS):
                if decision not in precedence:
                    missing.append(f"missing_precedence_decision:{decision}")

    actions = plan.get("allowed_next_actions", [])
    if not isinstance(actions, list) or len(actions) < 5:
        missing.append("at_least_five_allowed_next_actions_required")
    else:
        action_names = set()
        for action in actions:
            if not isinstance(action, dict):
                missing.append("allowed_next_action_must_be_object")
                continue
            action_name = action.get("action")
            if isinstance(action_name, str):
                action_names.add(action_name)
            for field in [
                "action",
                "owner",
                "allowed_states",
                "audit_event",
                "executes_tool",
                "calls_provider",
            ]:
                if field not in action:
                    missing.append(f"action_missing_field:{field}:{action_name}")
            if not action.get("owner"):
                missing.append(f"action_owner_required:{action_name}")
            if not action.get("audit_event"):
                missing.append(f"action_audit_event_required:{action_name}")
            if not isinstance(action.get("allowed_states"), list):
                missing.append(f"action_allowed_states_must_be_list:{action_name}")
            if action.get("executes_tool") is not False:
                missing.append(f"action_executes_tool_must_be_false:{action_name}")
            if action.get("calls_provider") is not False:
                missing.append(f"action_calls_provider_must_be_false:{action_name}")
        for action_name in sorted(VALID_ACTIONS):
            if action_name not in action_names:
                missing.append(f"missing_allowed_action:{action_name}")

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    cases = plan.get("orchestration_cases", [])
    if not isinstance(cases, list) or len(cases) < 10:
        missing.append("at_least_ten_orchestration_cases_required")
    else:
        observed_decisions = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("orchestration_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "name",
                "loop_id",
                "workflow_id",
                "incident_id",
                "trace_id",
                "current_state",
                "route_decision",
                "registry_decision",
                "approval_status",
                "iteration",
                "max_iterations",
                "state_hash",
                "previous_state_hash",
                "last_action",
                "budget_remaining_units",
                "expected_decision",
                "expected_next_action",
                "expected_stop_reason",
                "expected_terminal_status",
            ]:
                if field not in case:
                    missing.append(f"orchestration_case_missing_field:{field}:{name}")
            if case.get("route_decision") not in VALID_ROUTE_DECISIONS:
                missing.append(f"unexpected_route_decision:{name}")
            if case.get("registry_decision") not in VALID_REGISTRY_DECISIONS:
                missing.append(f"unexpected_registry_decision:{name}")
            if case.get("expected_next_action") not in VALID_ACTIONS:
                missing.append(f"unexpected_expected_next_action:{name}")
            _require_non_negative_number(case.get("iteration"), f"iteration:{name}", missing)
            _require_non_negative_number(case.get("max_iterations"), f"max_iterations:{name}", missing)
            _require_non_negative_number(
                case.get("budget_remaining_units"), f"budget_remaining_units:{name}", missing
            )
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_expected_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_orchestration", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "stateful_orchestration_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "orchestration_runtime_started": False,
        "workflow_runtime_started": False,
        "mcp_server_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "durable_store_created": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_stateful_orchestration_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
