#!/usr/bin/env python3
"""Validate Phase 4 v11 event workflow plan without cloud calls."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("cloud/aws/event-workflow.plan.json")

REQUIRED_MESSAGE_FIELDS = {
    "event_id",
    "trace_id",
    "idempotency_key",
    "source",
    "event_type",
    "created_at",
    "payload",
}

REQUIRED_CONTROLS = {
    "payload_schema_required",
    "trace_id_required",
    "idempotency_key_required",
    "retry_policy_required",
    "dead_letter_queue_required",
    "timeout_budget_required",
    "least_privilege_required",
    "observability_required",
    "cost_gate_required",
    "rollback_plan_required",
}

REQUIRED_LIVE_CHECKS = {
    "official_provider_docs_review",
    "credential_storage_plan",
    "budget_approval",
    "iam_least_privilege_review",
    "event_schema_review",
    "idempotency_test",
    "dlq_replay_runbook",
    "observability_dashboard",
    "rollback_plan",
}


def validate_event_workflow_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "event_workflow_plan_no_cloud_call":
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

    workflow = plan.get("workflow", {})
    if not isinstance(workflow, dict):
        missing.append("workflow_must_be_object")
    else:
        for field in [
            "name",
            "ingress",
            "event_bus",
            "queue",
            "worker",
            "dead_letter_queue",
            "result_sink",
        ]:
            value = workflow.get(field)
            if not isinstance(value, str) or not value.startswith("aois-p-"):
                missing.append(f"workflow_field_must_use_aois_p_prefix:{field}")

    contract = plan.get("message_contract", {})
    if not isinstance(contract, dict):
        missing.append("message_contract_must_be_object")
    else:
        fields = set(contract.get("required_fields", []))
        for field in sorted(REQUIRED_MESSAGE_FIELDS):
            if field not in fields:
                missing.append(f"missing_message_field:{field}")
        limits = contract.get("payload_limits", {})
        if not isinstance(limits, dict) or limits.get("large_payload_policy") != "store_pointer_not_blob":
            missing.append("large_payload_policy_must_use_pointer")

    controls = plan.get("controls", {})
    if not isinstance(controls, dict):
        missing.append("controls_must_be_object")
    else:
        for control in sorted(REQUIRED_CONTROLS):
            if controls.get(control) is not True:
                missing.append(f"missing_or_false_control:{control}")

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in ["max_cloud_invocations", "max_concurrency", "max_spend_usd"]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    retry_policy = plan.get("retry_policy", {})
    if not isinstance(retry_policy, dict):
        missing.append("retry_policy_must_be_object")
    else:
        if retry_policy.get("max_attempts") != 3:
            missing.append("retry_max_attempts_must_be_three")
        if retry_policy.get("dlq_after_exhaustion") is not True:
            missing.append("retry_must_send_to_dlq")

    live_checks = set(plan.get("operational_checks_before_live", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "event_workflow_plan_validation_no_cloud_call",
        "cloud_resources_created": False,
        "credentials_used": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_event_workflow_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
