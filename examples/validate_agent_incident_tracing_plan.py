#!/usr/bin/env python3
"""Validate Phase 6 v16.5 agent and incident tracing plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("telemetry/aois-p/agent-incident-tracing.plan.json")

REQUIRED_STEPS = {
    "incident.ingest",
    "incident.security_inspect",
    "incident.classify",
    "incident.route_decision",
    "incident.recommendation",
    "incident.response",
}

REQUIRED_FIELDS = {
    "trace_id",
    "incident_id",
    "request_id",
    "step_id",
    "parent_step_id",
    "agent_run_id",
    "route_id",
    "status",
    "duration_ms",
}

REQUIRED_CORRELATION = {
    "trace_id_required",
    "incident_id_required",
    "request_id_required",
    "step_id_required",
    "parent_step_id_required",
    "agent_run_id_required",
    "route_id_required",
    "tool_call_id_required_when_tool_used",
}

REQUIRED_STEP_CONTROLS = {
    "step_order_required",
    "parent_child_relationship_required",
    "error_status_required",
    "duration_required",
    "input_summary_required",
    "output_summary_required",
    "secret_redaction_required",
    "decision_reason_required",
}

REQUIRED_OBSERVABILITY = {
    "span_links_required",
    "structured_logs_required",
    "step_metrics_required",
    "incident_timeline_required",
    "cardinality_budget_required",
    "sampling_policy_required",
    "retention_policy_required",
}

REQUIRED_LIVE_CHECKS = {
    "official_telemetry_docs_review",
    "agent_step_taxonomy",
    "tool_call_trace_policy",
    "secret_redaction_test",
    "cardinality_budget",
    "sampling_policy",
    "incident_timeline_dashboard",
    "trace_backend_storage_budget",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_agent_incident_tracing_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "agent_incident_tracing_plan_no_runtime":
        missing.append("mode_must_be_no_runtime")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")

    for field in [
        "telemetry_runtime_started",
        "agent_runtime_started",
        "tool_calls_executed",
        "provider_call_made",
        "collector_started",
        "trace_backend_started",
        "external_network_required_for_this_lesson",
        "approved_for_live_agent_tracing",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    trace_model = plan.get("trace_model", {})
    if not isinstance(trace_model, dict):
        missing.append("trace_model_must_be_object")
    else:
        if trace_model.get("root_trace") != "aois.incident_trace":
            missing.append("root_trace_must_be_aois_incident_trace")
        if trace_model.get("agent_run") != "aois.agent_run_placeholder":
            missing.append("agent_run_must_be_placeholder")
        steps = set(trace_model.get("required_step_names", []))
        for step in sorted(REQUIRED_STEPS):
            if step not in steps:
                missing.append(f"missing_step:{step}")
        fields = set(trace_model.get("required_fields", []))
        for field in sorted(REQUIRED_FIELDS):
            if field not in fields:
                missing.append(f"missing_trace_field:{field}")

    correlation = plan.get("correlation_policy", {})
    if not isinstance(correlation, dict):
        missing.append("correlation_policy_must_be_object")
    else:
        for field in sorted(REQUIRED_CORRELATION):
            if correlation.get(field) is not True:
                missing.append(f"missing_correlation_policy:{field}")

    step_controls = plan.get("step_controls", {})
    if not isinstance(step_controls, dict):
        missing.append("step_controls_must_be_object")
    else:
        for field in sorted(REQUIRED_STEP_CONTROLS):
            if step_controls.get(field) is not True:
                missing.append(f"missing_step_control:{field}")

    observability = plan.get("observability_controls", {})
    if not isinstance(observability, dict):
        missing.append("observability_controls_must_be_object")
    else:
        for field in sorted(REQUIRED_OBSERVABILITY):
            if observability.get(field) is not True:
                missing.append(f"missing_observability_control:{field}")

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in [
            "max_agent_runs_for_lesson",
            "max_tool_calls_for_lesson",
            "max_provider_calls_for_lesson",
            "max_persistent_storage_mb",
        ]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    live_checks = set(plan.get("required_before_live_agent_tracing", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "agent_incident_tracing_validation_no_runtime",
        "telemetry_runtime_started": False,
        "agent_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "collector_started": False,
        "trace_backend_started": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_agent_incident_tracing_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
