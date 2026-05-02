#!/usr/bin/env python3
"""Validate Phase 8 v26 dashboard visibility plan without frontend runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("product/aois-p/dashboard-visibility.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_phase7_route_state",
    "uses_phase7_registry_state",
    "uses_phase7_workflow_state",
    "uses_phase7_orchestration_state",
    "uses_phase7_evaluation_state",
    "uses_phase7_autonomy_state",
    "uses_phase7_multi_agent_state",
    "uses_phase7_execution_boundary_state",
    "operator_read_surface",
    "dashboard_contract_only",
    "event_replay_required",
    "stale_state_indicator_required",
    "redaction_required",
    "accessibility_required",
    "no_live_frontend_runtime",
    "no_live_streaming_runtime",
    "no_tool_execution",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "incident_overview_required",
    "trace_timeline_required",
    "route_registry_panel_required",
    "workflow_orchestration_panel_required",
    "autonomy_agent_panel_required",
    "approval_queue_required",
    "budget_panel_required",
    "execution_boundary_panel_required",
    "event_order_required",
    "connection_state_required",
    "stale_indicator_required",
    "empty_state_required",
    "error_state_required",
    "accessibility_labels_required",
    "keyboard_navigation_required",
    "redaction_gate_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "incident_id",
    "trace_id",
    "severity",
    "latest_event",
    "event_age_seconds",
    "max_stale_seconds",
    "connection_status",
    "payload_sensitivity",
    "redaction_status",
    "accessibility_status",
    "budget_status",
    "has_incidents",
    "decision",
    "active_panel",
    "status_badge",
    "operator_action",
}

REQUIRED_PANELS = {
    "incident_overview",
    "trace_timeline",
    "route_registry",
    "workflow_orchestration",
    "autonomy_agents",
    "approvals",
    "budget",
    "execution_boundaries",
}

REQUIRED_EVENTS = {
    "incident_created",
    "incident_updated",
    "trace_started",
    "trace_completed",
    "route_decided",
    "registry_checked",
    "workflow_checkpointed",
    "orchestration_decided",
    "eval_scored",
    "autonomy_changed",
    "agent_handoff",
    "approval_requested",
    "approval_recorded",
    "budget_updated",
    "execution_boundary_decided",
}

REQUIRED_EVENT_FIELDS = {
    "event_id",
    "sequence_number",
    "incident_id",
    "trace_id",
    "event_type",
    "created_at",
    "source_phase",
    "summary",
    "redaction_status",
    "audit_event",
}

REQUIRED_DECISIONS = {
    "show_incident_overview",
    "show_trace_timeline",
    "show_route_registry_state",
    "show_workflow_state",
    "show_autonomy_agent_state",
    "show_approval_queue",
    "show_budget_risk",
    "show_execution_boundary",
    "show_stale_data_warning",
    "show_empty_state",
    "block_unredacted_payload",
    "block_inaccessible_widget",
    "show_connection_loss_banner",
}

REQUIRED_LIVE_CHECKS = {
    "react_component_tree_review",
    "api_contract_review",
    "event_stream_contract_review",
    "stale_state_drill",
    "redaction_review",
    "accessibility_review",
    "keyboard_navigation_test",
    "operator_workflow_review",
    "dashboard_error_state_review",
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
        "api_server_started",
        "frontend_runtime_started",
        "dashboard_deployed",
        "browser_started",
        "websocket_server_started",
        "sse_stream_started",
        "agent_runtime_started",
        "execution_runtime_started",
        "tool_calls_executed",
        "command_executed",
        "file_write_performed",
        "network_call_made",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "persistent_storage_created",
        "approved_for_live_dashboard",
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
        "https://react.dev/learn/thinking-in-react",
        "https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events",
        "https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API",
        "https://www.w3.org/WAI/WCAG22/quickref/",
    ]:
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_non_negative_number(value: object, label: str, missing: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        missing.append(f"{label}_must_be_numeric")
    elif value < 0:
        missing.append(f"{label}_must_be_non_negative")


def validate_dashboard_visibility_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "dashboard_visibility_plan_no_runtime":
        missing.append("mode_must_be_dashboard_visibility_plan_no_runtime")
    if plan.get("version") != "v26":
        missing.append("version_must_be_v26")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("dashboard_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("dashboard_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_dashboard_dimension:{dimension}")

    panels = plan.get("dashboard_panels", [])
    observed_panels: set[str] = set()
    if not isinstance(panels, list) or len(panels) < len(REQUIRED_PANELS):
        missing.append("complete_dashboard_panel_catalog_required")
    else:
        for panel in panels:
            if not isinstance(panel, dict):
                missing.append("dashboard_panel_must_be_object")
                continue
            panel_id = panel.get("panel_id")
            if isinstance(panel_id, str):
                observed_panels.add(panel_id)
            for field in [
                "panel_id",
                "title",
                "source_phase",
                "owner",
                "primary_fields",
                "update_events",
                "empty_state",
                "stale_after_seconds",
                "accessibility_label",
            ]:
                if not panel.get(field):
                    missing.append(f"panel_missing_field:{field}:{panel_id}")
            _require_non_negative_number(
                panel.get("stale_after_seconds"), f"stale_after_seconds:{panel_id}", missing
            )
            if not isinstance(panel.get("primary_fields"), list):
                missing.append(f"panel_primary_fields_must_be_list:{panel_id}")
            if not isinstance(panel.get("update_events"), list):
                missing.append(f"panel_update_events_must_be_list:{panel_id}")
        for panel_id in sorted(REQUIRED_PANELS):
            if panel_id not in observed_panels:
                missing.append(f"missing_dashboard_panel:{panel_id}")

    event_model = plan.get("event_model", {})
    if not isinstance(event_model, dict):
        missing.append("event_model_must_be_object")
    else:
        if event_model.get("ordering_key") != "sequence_number":
            missing.append("event_model_ordering_key_must_be_sequence_number")
        if event_model.get("dedupe_key") != "event_id":
            missing.append("event_model_dedupe_key_must_be_event_id")
        event_fields = set(event_model.get("required_fields", []))
        for field in sorted(REQUIRED_EVENT_FIELDS):
            if field not in event_fields:
                missing.append(f"missing_event_field:{field}")
        event_types = set(event_model.get("supported_event_types", []))
        for event_type in sorted(REQUIRED_EVENTS):
            if event_type not in event_types:
                missing.append(f"missing_event_type:{event_type}")

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    cases = plan.get("visibility_cases", [])
    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("at_least_one_case_per_decision_required")
    else:
        observed_decisions = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("visibility_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "case_id",
                "name",
                "incident_id",
                "trace_id",
                "severity",
                "latest_event",
                "event_age_seconds",
                "max_stale_seconds",
                "connection_status",
                "payload_sensitivity",
                "redaction_status",
                "accessibility_status",
                "budget_status",
                "has_incidents",
                "expected_decision",
                "expected_active_panel",
                "expected_status_badge",
                "expected_operator_action",
            ]:
                if field not in case:
                    missing.append(f"visibility_case_missing_field:{field}:{name}")
            if not isinstance(case.get("has_incidents"), bool):
                missing.append(f"has_incidents_must_be_boolean:{name}")
            _require_non_negative_number(case.get("event_age_seconds"), f"event_age_seconds:{name}", missing)
            _require_non_negative_number(case.get("max_stale_seconds"), f"max_stale_seconds:{name}", missing)
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_expected_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)
            if case.get("expected_active_panel") not in REQUIRED_PANELS:
                missing.append(f"unknown_expected_active_panel:{name}:{case.get('expected_active_panel')}")
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_dashboard", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "dashboard_visibility_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "api_server_started": False,
        "frontend_runtime_started": False,
        "websocket_server_started": False,
        "sse_stream_started": False,
        "browser_started": False,
        "provider_call_made": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_dashboard_visibility_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
