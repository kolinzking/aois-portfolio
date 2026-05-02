#!/usr/bin/env python3
"""Validate Phase 7 v22 durable workflow plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/durable-workflow.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v20_2_route_decisions",
    "uses_v21_tool_registry_results",
    "deterministic_plan_only",
    "durable_state_required",
    "checkpoint_required",
    "approval_wait_required",
    "idempotency_key_required",
    "retry_policy_required",
    "timeout_policy_required",
    "compensation_policy_required",
    "audit_log_required",
    "no_live_workflow_runtime",
    "no_tool_execution",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "state_machine_required",
    "step_owners_required",
    "step_inputs_outputs_required",
    "checkpoint_every_step",
    "approval_gate_required",
    "pause_resume_model_required",
    "retry_budget_required",
    "idempotency_required",
    "timeout_required",
    "failure_recovery_path_required",
    "terminal_status_required",
    "trace_id_required",
    "cost_context_required",
    "registry_context_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "workflow_id",
    "incident_id",
    "trace_id",
    "route_decision",
    "registry_decision",
    "state",
    "current_step",
    "checkpoint_id",
    "idempotency_key",
    "retry_count",
    "timeout_seconds",
    "approval_status",
    "planned_tools",
    "blocked_tools",
    "cost_budget_remaining",
    "terminal_status",
    "recovery_action",
}

REQUIRED_DECISIONS = {
    "complete_no_tool_workflow",
    "complete_read_only_workflow_plan",
    "pause_for_human_approval",
    "resume_after_approval",
    "block_registry_denial",
    "recover_after_retry",
    "fail_timeout",
    "skip_duplicate_step",
}

REQUIRED_LIVE_CHECKS = {
    "official_workflow_engine_review",
    "durable_store_resource_review",
    "checkpoint_schema_review",
    "approval_timeout_policy",
    "retry_budget_review",
    "idempotency_collision_review",
    "workflow_observability_dashboard",
    "audit_log_sink",
    "tool_registry_integration_test",
    "cost_accounting_integration_test",
    "primary_aois_separation_review",
    "resource_usage_record",
}

VALID_TERMINAL_STATES = {"completed", "blocked", "failed", "timed_out"}
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


def _require_true_fields(
    section: object, required: set[str], label: str, missing: list[str]
) -> None:
    if not isinstance(section, dict):
        missing.append(f"{label}_must_be_object")
        return
    for field in sorted(required):
        if section.get(field) is not True:
            missing.append(f"missing_{label}:{field}")


def _require_zero_runtime_flags(plan: dict[str, object], missing: list[str]) -> None:
    for field in [
        "agent_runtime_started",
        "workflow_runtime_started",
        "mcp_server_started",
        "tool_calls_executed",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "durable_store_created",
        "persistent_storage_created",
        "approved_for_live_workflow",
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
        url = note.get("url")
        if isinstance(url, str):
            urls.add(url)
        if note.get("date_checked") != "2026-04-29":
            missing.append(f"source_note_date_must_be_2026_04_29:{note.get('source')}")
    if "https://docs.temporal.io/" not in urls:
        missing.append("missing_temporal_source_note")
    if "https://docs.langchain.com/oss/python/langgraph/durable-execution" not in urls:
        missing.append("missing_langgraph_durable_execution_source_note")


def _require_non_negative_number(value: object, label: str, missing: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        missing.append(f"{label}_must_be_numeric")
    elif value < 0:
        missing.append(f"{label}_must_be_non_negative")


def validate_durable_workflow_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "durable_agent_workflow_plan_no_runtime":
        missing.append("mode_must_be_durable_agent_workflow_plan_no_runtime")
    if plan.get("version") != "v22":
        missing.append("version_must_be_v22")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_zero_runtime_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("workflow_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("workflow_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_workflow_dimension:{dimension}")

    state_machine = plan.get("state_machine", {})
    if not isinstance(state_machine, dict):
        missing.append("state_machine_must_be_object")
    else:
        if state_machine.get("initial_state") != "received":
            missing.append("initial_state_must_be_received")
        terminal_states = set(state_machine.get("terminal_states", []))
        for state in sorted(VALID_TERMINAL_STATES):
            if state not in terminal_states:
                missing.append(f"missing_terminal_state:{state}")
        states = set(state_machine.get("states", []))
        for state in ["waiting_for_approval", "completed", "blocked", "timed_out"]:
            if state not in states:
                missing.append(f"missing_workflow_state:{state}")
        transitions = state_machine.get("transitions", [])
        if not isinstance(transitions, list) or len(transitions) < 10:
            missing.append("at_least_ten_transitions_required")

    steps = plan.get("step_catalog", [])
    if not isinstance(steps, list) or len(steps) < 7:
        missing.append("at_least_seven_workflow_steps_required")
    else:
        for step in steps:
            if not isinstance(step, dict):
                missing.append("step_catalog_item_must_be_object")
                continue
            step_id = step.get("step_id")
            for field in [
                "step_id",
                "owner",
                "input_refs",
                "output_refs",
                "checkpoint_required",
                "idempotency_key_ref",
                "timeout_seconds",
                "max_retries",
                "compensation",
            ]:
                if field not in step:
                    missing.append(f"step_missing_field:{field}:{step_id}")
            if step.get("checkpoint_required") is not True:
                missing.append(f"step_checkpoint_required:{step_id}")
            if not step.get("owner"):
                missing.append(f"step_owner_required:{step_id}")
            if not isinstance(step.get("input_refs"), list):
                missing.append(f"step_input_refs_must_be_list:{step_id}")
            if not isinstance(step.get("output_refs"), list):
                missing.append(f"step_output_refs_must_be_list:{step_id}")
            _require_non_negative_number(step.get("timeout_seconds"), f"step_timeout:{step_id}", missing)
            _require_non_negative_number(step.get("max_retries"), f"step_max_retries:{step_id}", missing)

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    cases = plan.get("workflow_cases", [])
    if not isinstance(cases, list) or len(cases) < 8:
        missing.append("at_least_eight_workflow_cases_required")
    else:
        observed_decisions = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("workflow_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "name",
                "workflow_id",
                "incident_id",
                "trace_id",
                "route_decision",
                "route_id",
                "registry_decision",
                "approval_status",
                "requested_tools",
                "blocked_tools",
                "current_step",
                "elapsed_seconds",
                "timeout_seconds",
                "retry_count",
                "max_retries",
                "idempotency_key_seen",
                "cost_budget_remaining",
                "expected_decision",
                "expected_state",
                "expected_terminal_status",
                "expected_recovery_action",
            ]:
                if field not in case:
                    missing.append(f"workflow_case_missing_field:{field}:{name}")
            if case.get("route_decision") not in VALID_ROUTE_DECISIONS:
                missing.append(f"unexpected_route_decision:{name}")
            if case.get("registry_decision") not in VALID_REGISTRY_DECISIONS:
                missing.append(f"unexpected_registry_decision:{name}")
            if not isinstance(case.get("requested_tools"), list):
                missing.append(f"requested_tools_must_be_list:{name}")
            if not isinstance(case.get("blocked_tools"), list):
                missing.append(f"blocked_tools_must_be_list:{name}")
            if not isinstance(case.get("idempotency_key_seen"), bool):
                missing.append(f"idempotency_key_seen_must_be_boolean:{name}")
            _require_non_negative_number(case.get("elapsed_seconds"), f"elapsed_seconds:{name}", missing)
            _require_non_negative_number(case.get("timeout_seconds"), f"timeout_seconds:{name}", missing)
            _require_non_negative_number(case.get("retry_count"), f"retry_count:{name}", missing)
            _require_non_negative_number(case.get("max_retries"), f"max_retries:{name}", missing)
            _require_non_negative_number(
                case.get("cost_budget_remaining"), f"cost_budget_remaining:{name}", missing
            )
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_expected_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_workflow", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "durable_workflow_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "workflow_runtime_started": False,
        "mcp_server_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "durable_store_created": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_durable_workflow_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
