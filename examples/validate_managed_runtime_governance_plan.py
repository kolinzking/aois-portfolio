#!/usr/bin/env python3
"""Validate Phase 4 v12 managed runtime governance plan without cloud calls."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("cloud/aws/managed-runtime-governance.plan.json")

REQUIRED_RUNTIME_FIELDS = {
    "cluster",
    "node_pool",
    "workload_identity",
    "service_account",
    "log_group",
    "metrics_dashboard",
    "budget_alarm",
}

REQUIRED_OBSERVABILITY = {
    "logs_required",
    "metrics_required",
    "traces_required",
    "events_required",
    "dashboards_required",
    "alerts_required",
    "slo_required",
}

REQUIRED_OPERATIONAL_CONTROLS = {
    "runbook_required",
    "rollback_plan_required",
    "capacity_plan_required",
    "backup_restore_plan_required",
    "incident_response_required",
    "resource_usage_record_required",
}

REQUIRED_LIVE_CHECKS = {
    "official_provider_docs_review",
    "credential_storage_plan",
    "budget_approval",
    "iam_least_privilege_review",
    "workload_identity_review",
    "network_boundary_review",
    "observability_dashboard",
    "cost_alarm_review",
    "capacity_plan",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_managed_runtime_governance_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "managed_runtime_governance_plan_no_cloud_call":
        missing.append("mode_must_be_no_cloud_call")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("cloud_resources_created") is not False:
        missing.append("cloud_resources_created_must_be_false")
    if plan.get("credentials_used") is not False:
        missing.append("credentials_used_must_be_false")
    if plan.get("external_network_required_for_this_lesson") is not False:
        missing.append("network_must_not_be_required")
    if plan.get("approved_for_live_cloud") is not False:
        missing.append("live_cloud_must_not_be_approved")

    runtime = plan.get("managed_runtime", {})
    if not isinstance(runtime, dict):
        missing.append("managed_runtime_must_be_object")
    else:
        for field in sorted(REQUIRED_RUNTIME_FIELDS):
            value = runtime.get(field)
            if not isinstance(value, str) or not value.startswith("aois-p-"):
                missing.append(f"runtime_field_must_use_aois_p_prefix:{field}")

    iam = plan.get("iam_boundaries", {})
    if not isinstance(iam, dict):
        missing.append("iam_boundaries_must_be_object")
    else:
        if iam.get("least_privilege_required") is not True:
            missing.append("least_privilege_required_must_be_true")
        if iam.get("wildcard_admin_policy_allowed") is not False:
            missing.append("wildcard_admin_policy_must_be_false")
        if iam.get("long_lived_static_keys_allowed") is not False:
            missing.append("static_keys_must_be_false")
        if iam.get("workload_identity_required") is not True:
            missing.append("workload_identity_required_must_be_true")
        if iam.get("secret_in_repo_allowed") is not False:
            missing.append("secret_in_repo_must_be_false")

    observability = plan.get("observability", {})
    if not isinstance(observability, dict):
        missing.append("observability_must_be_object")
    else:
        for field in sorted(REQUIRED_OBSERVABILITY):
            if observability.get(field) is not True:
                missing.append(f"missing_observability:{field}")

    cost = plan.get("cost_controls", {})
    if not isinstance(cost, dict):
        missing.append("cost_controls_must_be_object")
    else:
        if cost.get("budget_approved") is not False:
            missing.append("budget_approved_must_be_false")
        for field in ["max_spend_usd", "max_clusters", "max_nodes"]:
            if cost.get(field) != 0:
                missing.append(f"{field}_must_be_zero")
        for field in ["cost_tags_required", "quota_review_required", "scale_down_plan_required"]:
            if cost.get(field) is not True:
                missing.append(f"missing_cost_control:{field}")

    operational = plan.get("operational_controls", {})
    if not isinstance(operational, dict):
        missing.append("operational_controls_must_be_object")
    else:
        for field in sorted(REQUIRED_OPERATIONAL_CONTROLS):
            if operational.get(field) is not True:
                missing.append(f"missing_operational_control:{field}")

    live_checks = set(plan.get("required_before_live", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "managed_runtime_governance_validation_no_cloud_call",
        "cloud_resources_created": False,
        "credentials_used": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_managed_runtime_governance_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
