#!/usr/bin/env python3
"""Validate Phase 6 v18 incident response plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("incident-response/aois-p/incident-response.plan.json")

REQUIRED_SEVERITIES = {"SEV1", "SEV2", "SEV3"}

REQUIRED_ROLES = {
    "incident_commander",
    "operations_lead",
    "communications_lead",
    "scribe",
    "subject_matter_expert",
    "agent_operator",
}

REQUIRED_LIFECYCLE = {
    "detect",
    "triage",
    "declare",
    "stabilize",
    "mitigate",
    "resolve",
    "review",
}

REQUIRED_RUNBOOK_CONTROLS = {
    "severity_assignment_required",
    "single_incident_commander_required",
    "timeline_required",
    "communication_channel_required",
    "rollback_path_required",
    "mitigation_owner_required",
    "safety_gate_required",
    "customer_or_user_impact_required",
    "post_incident_review_required",
    "action_item_owner_required",
}

REQUIRED_AGENT_CONTROLS = {
    "human_approval_for_destructive_action",
    "low_confidence_route_to_human",
    "evidence_required_before_recommendation",
    "tool_call_audit_required",
    "prompt_change_freeze_when_incident_active",
    "provider_call_budget_required",
    "unsafe_recommendation_escalates_severity",
}

REQUIRED_COMMUNICATION_POLICY = {
    "internal_status_required",
    "external_status_review_required",
    "update_cadence_required",
    "plain_language_impact_required",
    "no_root_cause_claim_before_evidence",
    "resolution_criteria_required",
}

REQUIRED_REVIEW = {
    "blameless_review_required",
    "timeline_required",
    "impact_summary_required",
    "root_cause_or_contributing_factors_required",
    "what_went_well_required",
    "what_went_poorly_required",
    "action_items_required",
    "action_item_owners_required",
    "due_dates_required",
    "slo_impact_required",
    "agent_behavior_review_required",
}

REQUIRED_DIAGNOSIS = {
    "start_from_symptom_required",
    "compare_recent_changes_required",
    "check_resource_pressure_required",
    "check_dependency_health_required",
    "check_agent_output_quality_required",
    "check_event_lag_required",
    "evidence_before_root_cause_required",
}

REQUIRED_LIVE_CHECKS = {
    "production_service_inventory",
    "oncall_policy",
    "severity_policy_review",
    "communication_channel_approval",
    "pager_routing_approval",
    "ticketing_workflow_approval",
    "status_page_policy",
    "agent_action_safety_policy",
    "rollback_plan",
    "post_incident_review_template",
    "primary_aois_separation_review",
    "resource_usage_record",
}


def _require_true_fields(section: object, required: set[str], label: str, missing: list[str]) -> None:
    if not isinstance(section, dict):
        missing.append(f"{label}_must_be_object")
        return
    for field in sorted(required):
        if section.get(field) is not True:
            missing.append(f"missing_{label}:{field}")


def validate_incident_response_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "incident_response_plan_no_runtime":
        missing.append("mode_must_be_no_runtime")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")

    for field in [
        "incident_runtime_started",
        "pager_runtime_started",
        "ticketing_runtime_started",
        "chatops_runtime_started",
        "status_page_runtime_started",
        "agent_runtime_started",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "approved_for_live_incident_response",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    severities = plan.get("severity_levels", [])
    if not isinstance(severities, list):
        missing.append("severity_levels_must_be_list")
        severity_names: set[str] = set()
    else:
        severity_names = set()
        for item in severities:
            if not isinstance(item, dict):
                missing.append("severity_entry_must_be_object")
                continue
            name = item.get("name")
            if isinstance(name, str):
                severity_names.add(name)
            if item.get("post_incident_review_required") is not True:
                missing.append(f"severity_review_required:{name}")
            for field in ["declare_within_minutes", "update_every_minutes"]:
                if not isinstance(item.get(field), int) or item[field] <= 0:
                    missing.append(f"severity_{field}_must_be_positive:{name}")
    for severity in sorted(REQUIRED_SEVERITIES):
        if severity not in severity_names:
            missing.append(f"missing_severity:{severity}")

    roles = plan.get("roles", {})
    if not isinstance(roles, dict):
        missing.append("roles_must_be_object")
    else:
        for role in sorted(REQUIRED_ROLES):
            value = roles.get(role)
            if not isinstance(value, str) or not value.startswith("aois-p-"):
                missing.append(f"role_must_use_aois_p_prefix:{role}")

    lifecycle = set(plan.get("lifecycle", []))
    for step in sorted(REQUIRED_LIFECYCLE):
        if step not in lifecycle:
            missing.append(f"missing_lifecycle_step:{step}")

    _require_true_fields(plan.get("runbook_controls"), REQUIRED_RUNBOOK_CONTROLS, "runbook_control", missing)
    _require_true_fields(plan.get("agent_incident_controls"), REQUIRED_AGENT_CONTROLS, "agent_control", missing)
    _require_true_fields(plan.get("communication_policy"), REQUIRED_COMMUNICATION_POLICY, "communication_policy", missing)
    _require_true_fields(plan.get("post_incident_review"), REQUIRED_REVIEW, "post_incident_review", missing)
    _require_true_fields(plan.get("diagnosis_policy"), REQUIRED_DIAGNOSIS, "diagnosis_policy", missing)

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in [
            "max_pager_services_for_lesson",
            "max_ticketing_services_for_lesson",
            "max_chatops_services_for_lesson",
            "max_status_page_services_for_lesson",
            "max_agent_runs_for_lesson",
            "max_provider_calls_for_lesson",
            "max_persistent_storage_mb",
            "max_spend_usd",
        ]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    live_checks = set(plan.get("required_before_live_incident_response", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "incident_response_validation_no_runtime",
        "incident_runtime_started": False,
        "pager_runtime_started": False,
        "ticketing_runtime_started": False,
        "chatops_runtime_started": False,
        "status_page_runtime_started": False,
        "agent_runtime_started": False,
        "provider_call_made": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_incident_response_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
