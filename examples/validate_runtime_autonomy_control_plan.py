#!/usr/bin/env python3
"""Validate Phase 7 v23.8 runtime autonomy control plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/runtime-autonomy-control.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v23_5_evaluation_gate",
    "autonomy_mode_required",
    "operator_control_required",
    "kill_switch_required",
    "human_approval_required_for_autonomy_increase",
    "observability_required",
    "safety_event_stop_required",
    "budget_guard_required",
    "runtime_health_required",
    "rollback_policy_required",
    "audit_event_required",
    "local_simulation_only",
    "no_live_agent_runtime",
    "no_tool_execution",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "mode_catalog_required",
    "promotion_gate_required",
    "demotion_gate_required",
    "kill_switch_required",
    "operator_override_required",
    "eval_gate_required",
    "safety_gate_required",
    "budget_gate_required",
    "observability_gate_required",
    "runtime_health_gate_required",
    "rollback_action_required",
    "audit_event_required",
    "trace_id_required",
    "autonomy_owner_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "incident_id",
    "trace_id",
    "requested_mode",
    "current_mode",
    "allowed_mode",
    "eval_status",
    "safety_status",
    "budget_status",
    "observability_status",
    "runtime_health",
    "operator_approval",
    "kill_switch",
    "rollback_signal",
    "decision",
    "next_action",
    "stop_reason",
    "audit_event",
}

REQUIRED_DECISIONS = {
    "disable_kill_switch",
    "emergency_stop_safety_event",
    "rollback_on_regression",
    "demote_runtime_degraded",
    "hold_observability_missing",
    "pause_budget_exhausted",
    "allow_shadow_mode",
    "allow_supervised_mode",
    "require_human_approval_for_limited",
    "allow_limited_autonomy",
}

REQUIRED_MODES = {"disabled", "shadow", "supervised", "limited_autonomous"}

REQUIRED_LIVE_CHECKS = {
    "official_deployment_checklist_review",
    "operator_runbook_review",
    "kill_switch_test",
    "rollback_drill",
    "observability_dashboard_review",
    "alert_route_review",
    "autonomy_owner_assigned",
    "safety_event_response_workflow",
    "budget_guard_integration_test",
    "evaluation_gate_integration_test",
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
        "autonomy_runtime_started",
        "orchestration_runtime_started",
        "workflow_runtime_started",
        "mcp_server_started",
        "tool_calls_executed",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "durable_store_created",
        "persistent_storage_created",
        "approved_for_live_autonomy",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")


def _require_source_notes(source_notes: object, missing: list[str]) -> None:
    if not isinstance(source_notes, list) or len(source_notes) < 4:
        missing.append("at_least_four_source_notes_required")
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
        "https://developers.openai.com/api/docs/guides/deployment-checklist",
        "https://developers.openai.com/api/docs/guides/agents/guardrails-approvals",
        "https://developers.openai.com/api/docs/guides/agents/integrations-observability",
        "https://developers.openai.com/api/docs/guides/safety-checks",
    ]:
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_non_negative_number(value: object, label: str, missing: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        missing.append(f"{label}_must_be_numeric")
    elif value < 0:
        missing.append(f"{label}_must_be_non_negative")


def validate_runtime_autonomy_control_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "runtime_autonomy_control_plan_no_runtime":
        missing.append("mode_must_be_runtime_autonomy_control_plan_no_runtime")
    if plan.get("version") != "v23.8":
        missing.append("version_must_be_v23_8")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("autonomy_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("autonomy_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_autonomy_dimension:{dimension}")

    mode_catalog = plan.get("mode_catalog", [])
    catalog_modes: set[str] = set()
    if not isinstance(mode_catalog, list) or len(mode_catalog) < 4:
        missing.append("at_least_four_autonomy_modes_required")
    else:
        for mode in mode_catalog:
            if not isinstance(mode, dict):
                missing.append("mode_catalog_item_must_be_object")
                continue
            mode_name = mode.get("mode")
            if isinstance(mode_name, str):
                catalog_modes.add(mode_name)
            for field in [
                "mode",
                "max_autonomy_level",
                "description",
                "requires_operator_approval",
                "executes_tools",
                "calls_provider",
            ]:
                if field not in mode:
                    missing.append(f"mode_missing_field:{field}:{mode_name}")
            _require_non_negative_number(
                mode.get("max_autonomy_level"), f"max_autonomy_level:{mode_name}", missing
            )
            if not isinstance(mode.get("requires_operator_approval"), bool):
                missing.append(f"mode_requires_operator_approval_must_be_boolean:{mode_name}")
            if mode.get("executes_tools") is not False:
                missing.append(f"mode_executes_tools_must_be_false:{mode_name}")
            if mode.get("calls_provider") is not False:
                missing.append(f"mode_calls_provider_must_be_false:{mode_name}")
        for mode_name in sorted(REQUIRED_MODES):
            if mode_name not in catalog_modes:
                missing.append(f"missing_autonomy_mode:{mode_name}")

    gate_policy = plan.get("gate_policy", {})
    if not isinstance(gate_policy, dict):
        missing.append("gate_policy_must_be_object")
    else:
        expected_gate_fields = {
            "required_eval_status": "pass",
            "required_safety_status": "clear",
            "required_budget_status": "within_budget",
            "required_observability_status": "healthy",
            "required_runtime_health": "healthy",
            "kill_switch_mode": "disabled",
            "rollback_mode": "shadow",
            "max_mode_without_approval": "shadow",
        }
        for field, expected in expected_gate_fields.items():
            if gate_policy.get(field) != expected:
                missing.append(f"{field}_must_be_{expected}")
        approval_modes = set(gate_policy.get("operator_approval_required_for_modes", []))
        for mode_name in ["supervised", "limited_autonomous"]:
            if mode_name not in approval_modes:
                missing.append(f"approval_required_for_mode:{mode_name}")

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    cases = plan.get("autonomy_cases", [])
    if not isinstance(cases, list) or len(cases) < 10:
        missing.append("at_least_ten_autonomy_cases_required")
    else:
        observed_decisions = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("autonomy_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "case_id",
                "name",
                "incident_id",
                "trace_id",
                "requested_mode",
                "current_mode",
                "eval_status",
                "safety_status",
                "budget_status",
                "observability_status",
                "runtime_health",
                "operator_approval",
                "kill_switch",
                "rollback_signal",
                "expected_decision",
                "expected_allowed_mode",
                "expected_next_action",
                "expected_stop_reason",
            ]:
                if field not in case:
                    missing.append(f"autonomy_case_missing_field:{field}:{name}")
            if case.get("requested_mode") not in REQUIRED_MODES:
                missing.append(f"unexpected_requested_mode:{name}")
            if case.get("current_mode") not in REQUIRED_MODES:
                missing.append(f"unexpected_current_mode:{name}")
            if case.get("expected_allowed_mode") not in REQUIRED_MODES:
                missing.append(f"unexpected_expected_allowed_mode:{name}")
            if not isinstance(case.get("kill_switch"), bool):
                missing.append(f"kill_switch_must_be_boolean:{name}")
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_expected_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_autonomy", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "runtime_autonomy_control_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "autonomy_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_runtime_autonomy_control_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
