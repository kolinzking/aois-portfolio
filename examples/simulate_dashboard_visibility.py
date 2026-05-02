#!/usr/bin/env python3
"""Simulate Phase 8 v26 dashboard visibility decisions without a UI runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("product/aois-p/dashboard-visibility.plan.json")

EVENT_PANEL = {
    "incident_created": "incident_overview",
    "incident_updated": "incident_overview",
    "trace_started": "trace_timeline",
    "trace_completed": "trace_timeline",
    "route_decided": "route_registry",
    "registry_checked": "route_registry",
    "workflow_checkpointed": "workflow_orchestration",
    "orchestration_decided": "workflow_orchestration",
    "eval_scored": "workflow_orchestration",
    "autonomy_changed": "autonomy_agents",
    "agent_handoff": "autonomy_agents",
    "approval_requested": "approvals",
    "approval_recorded": "approvals",
    "budget_updated": "budget",
    "execution_boundary_decided": "execution_boundaries",
}


def _panel_for(case: dict[str, object]) -> str:
    return EVENT_PANEL.get(str(case["latest_event"]), "incident_overview")


def _decide(case: dict[str, object]) -> dict[str, object]:
    latest_event = str(case["latest_event"])
    active_panel = _panel_for(case)
    reasons: list[str] = []

    if case["payload_sensitivity"] == "sensitive" and case["redaction_status"] != "redacted":
        decision = "block_unredacted_payload"
        status_badge = "redaction_block"
        operator_action = "fix_redaction_before_render"
        reasons.append("sensitive_payload_not_redacted")
    elif case["accessibility_status"] != "pass":
        decision = "block_inaccessible_widget"
        status_badge = "accessibility_block"
        operator_action = "fix_accessibility_before_release"
        reasons.append("accessibility_gate_failed")
    elif case["connection_status"] != "connected":
        decision = "show_connection_loss_banner"
        status_badge = "connection_lost"
        operator_action = "check_stream_health"
        reasons.append("event_stream_disconnected")
    elif case["has_incidents"] is not True:
        decision = "show_empty_state"
        active_panel = "incident_overview"
        status_badge = "empty"
        operator_action = "wait_for_incident"
        reasons.append("no_incidents_in_scope")
    elif int(case["event_age_seconds"]) > int(case["max_stale_seconds"]):
        decision = "show_stale_data_warning"
        status_badge = "stale"
        operator_action = "refresh_or_check_stream"
        reasons.append("event_age_exceeds_freshness_budget")
    elif latest_event in {"approval_requested", "approval_recorded"}:
        decision = "show_approval_queue"
        status_badge = "approval_wait"
        operator_action = "review_approval_request"
        reasons.append("approval_event_requires_operator_attention")
    elif latest_event == "execution_boundary_decided":
        decision = "show_execution_boundary"
        status_badge = "execution_blocked"
        operator_action = "inspect_boundary_reason"
        reasons.append("execution_boundary_decision_is_latest")
    elif latest_event == "budget_updated" and case["budget_status"] in {"reserve_low", "exhausted"}:
        decision = "show_budget_risk"
        status_badge = "budget_risk"
        operator_action = "inspect_budget_reserve"
        reasons.append("budget_event_reports_risk")
    elif latest_event in {"autonomy_changed", "agent_handoff"}:
        decision = "show_autonomy_agent_state"
        status_badge = "handoff" if latest_event == "agent_handoff" else "autonomy"
        operator_action = "inspect_agent_owner"
        reasons.append("autonomy_or_agent_event_is_latest")
    elif latest_event in {"workflow_checkpointed", "orchestration_decided", "eval_scored"}:
        decision = "show_workflow_state"
        status_badge = "loop_decided"
        operator_action = "inspect_next_action"
        reasons.append("workflow_or_orchestration_event_is_latest")
    elif latest_event in {"route_decided", "registry_checked"}:
        decision = "show_route_registry_state"
        status_badge = "policy_checked"
        operator_action = "inspect_tool_exposure"
        reasons.append("route_or_registry_event_is_latest")
    elif latest_event in {"trace_started", "trace_completed"}:
        decision = "show_trace_timeline"
        status_badge = "complete" if latest_event == "trace_completed" else "tracing"
        operator_action = "inspect_trace_timeline"
        reasons.append("trace_event_is_latest")
    else:
        decision = "show_incident_overview"
        status_badge = "active"
        operator_action = "inspect_incident_summary"
        reasons.append("incident_event_is_latest")

    expected_decision = str(case["expected_decision"])
    expected_active_panel = str(case["expected_active_panel"])
    expected_status_badge = str(case["expected_status_badge"])
    expected_operator_action = str(case["expected_operator_action"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "latest_event": latest_event,
        "decision": decision,
        "active_panel": active_panel,
        "status_badge": status_badge,
        "operator_action": operator_action,
        "expected_decision": expected_decision,
        "expected_active_panel": expected_active_panel,
        "expected_status_badge": expected_status_badge,
        "expected_operator_action": expected_operator_action,
        "passed": (
            decision == expected_decision
            and active_panel == expected_active_panel
            and status_badge == expected_status_badge
            and operator_action == expected_operator_action
        ),
        "reasons": reasons,
    }


def simulate_dashboard_visibility() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case) for case in plan["visibility_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "dashboard_visibility_simulation_no_runtime",
        "namespace": plan["namespace"],
        "api_server_started": False,
        "frontend_runtime_started": False,
        "browser_started": False,
        "websocket_server_started": False,
        "sse_stream_started": False,
        "network_call_made": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_dashboard_visibility()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
