#!/usr/bin/env python3
"""Validate Phase 6 v17.5 service and agent SLO plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("reliability/aois-p/service-agent-slo.plan.json")

REQUIRED_SERVICE_NAMES = {
    "aois-p-api",
    "aois-p-incident-stream-consumer",
}

REQUIRED_AGENT_NAMES = {
    "aois-p-incident-agent",
}

REQUIRED_SLIS = {
    "availability",
    "latency",
    "freshness",
    "agent_success",
    "agent_quality",
    "agent_safety",
}

REQUIRED_ALERT_POLICY = {
    "burn_rate_alerts_required",
    "fast_burn_page_required",
    "slow_burn_ticket_required",
    "symptom_based_alerts_required",
    "cause_based_alerts_disallowed_as_primary_page",
}

REQUIRED_ERROR_BUDGET_POLICY = {
    "budget_calculation_required",
    "burn_rate_calculation_required",
    "freeze_risky_changes_when_budget_exhausted",
    "route_agent_actions_to_human_review_when_budget_exhausted",
    "post_incident_review_required",
}

REQUIRED_DASHBOARD_POLICY = {
    "service_slo_dashboard_required",
    "agent_slo_dashboard_required",
    "error_budget_dashboard_required",
    "burn_rate_dashboard_required",
    "user_impact_panel_required",
}

REQUIRED_CONTROLS = {
    "official_docs_review_required",
    "sli_definitions_required",
    "slo_objectives_required",
    "error_budget_policy_required",
    "burn_rate_alerts_required",
    "dashboard_plan_required",
    "agent_quality_gate_required",
    "agent_safety_gate_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
}

REQUIRED_LIVE_CHECKS = {
    "official_observability_docs_review",
    "production_service_inventory",
    "sli_event_definitions",
    "slo_objective_review",
    "agent_quality_evaluation_set",
    "agent_safety_policy",
    "error_budget_policy",
    "burn_rate_alert_plan",
    "dashboard_plan",
    "storage_budget",
    "rollback_plan",
    "primary_aois_separation_review",
}


def _require_true_fields(section: object, required: set[str], label: str, missing: list[str]) -> None:
    if not isinstance(section, dict):
        missing.append(f"{label}_must_be_object")
        return
    for field in sorted(required):
        if section.get(field) is not True:
            missing.append(f"missing_{label}:{field}")


def _validate_slo_entry(entry: object, label: str, missing: list[str]) -> str | None:
    if not isinstance(entry, dict):
        missing.append(f"{label}_entry_must_be_object")
        return None

    name = entry.get("name")
    if not isinstance(name, str) or not name.startswith("aois-p-"):
        missing.append(f"{label}_name_must_use_aois_p_prefix")
        name = None

    objective = entry.get("objective_percent")
    if not isinstance(objective, (int, float)) or not 0 < float(objective) < 100:
        missing.append(f"{label}_objective_must_be_between_0_and_100")

    if entry.get("window_days") != 30:
        missing.append(f"{label}_window_days_must_be_30")

    for field in ["sli", "good_event", "total_event", "latency_sli", "error_budget_policy"]:
        if not isinstance(entry.get(field), str) or not entry[field]:
            missing.append(f"{label}_missing_field:{field}")

    if entry.get("burn_rate_alerts_required") is not True:
        missing.append(f"{label}_burn_rate_alerts_required")

    return name


def validate_service_agent_slo_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "service_agent_slo_plan_no_runtime":
        missing.append("mode_must_be_no_runtime")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")

    for field in [
        "slo_runtime_started",
        "metrics_backend_started",
        "alerting_runtime_started",
        "dashboard_runtime_started",
        "agent_runtime_started",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "approved_for_live_slo_monitoring",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    windows = plan.get("slo_windows", {})
    if not isinstance(windows, dict):
        missing.append("slo_windows_must_be_object")
    else:
        expected_windows = {
            "primary_window_days": 30,
            "fast_burn_window_minutes": 5,
            "slow_burn_window_hours": 6,
            "reporting_window_days": 7,
        }
        for field, expected in expected_windows.items():
            if windows.get(field) != expected:
                missing.append(f"{field}_must_be_{expected}")

    service_names = {
        name
        for name in (
            _validate_slo_entry(entry, "service_slo", missing)
            for entry in plan.get("service_slos", [])
        )
        if name
    }
    for name in sorted(REQUIRED_SERVICE_NAMES):
        if name not in service_names:
            missing.append(f"missing_service_slo:{name}")

    agent_names = set()
    for entry in plan.get("agent_slos", []):
        name = _validate_slo_entry(entry, "agent_slo", missing)
        if name:
            agent_names.add(name)
        if isinstance(entry, dict):
            for field in [
                "quality_gate_required",
                "safety_gate_required",
                "human_review_required_for_destructive_action",
                "provider_error_budget_required",
            ]:
                if entry.get(field) is not True:
                    missing.append(f"missing_agent_control:{field}")
    for name in sorted(REQUIRED_AGENT_NAMES):
        if name not in agent_names:
            missing.append(f"missing_agent_slo:{name}")

    slis = set(plan.get("required_slis", []))
    for sli in sorted(REQUIRED_SLIS):
        if sli not in slis:
            missing.append(f"missing_sli:{sli}")

    _require_true_fields(plan.get("alert_policy"), REQUIRED_ALERT_POLICY, "alert_policy", missing)
    _require_true_fields(
        plan.get("error_budget_policy"),
        REQUIRED_ERROR_BUDGET_POLICY,
        "error_budget_policy",
        missing,
    )
    _require_true_fields(plan.get("dashboard_policy"), REQUIRED_DASHBOARD_POLICY, "dashboard_policy", missing)
    _require_true_fields(plan.get("controls"), REQUIRED_CONTROLS, "control", missing)

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in [
            "max_metrics_backends_for_lesson",
            "max_alerting_services_for_lesson",
            "max_dashboard_services_for_lesson",
            "max_agent_runs_for_lesson",
            "max_provider_calls_for_lesson",
            "max_persistent_storage_mb",
            "max_spend_usd",
        ]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    live_checks = set(plan.get("required_before_live_slo_monitoring", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "service_agent_slo_validation_no_runtime",
        "slo_runtime_started": False,
        "metrics_backend_started": False,
        "alerting_runtime_started": False,
        "dashboard_runtime_started": False,
        "agent_runtime_started": False,
        "provider_call_made": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_service_agent_slo_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
