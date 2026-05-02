#!/usr/bin/env python3
"""Simulate Phase 8 v27 policy-aware access decisions without auth runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("product/aois-p/policy-aware-access.plan.json")

SENSITIVE_RESOURCE_TYPES = {
    "trace",
    "approvals",
    "budget",
    "execution_boundaries",
    "access_audit",
}

ALLOW_DECISIONS = {
    "incident": ("allow_incident_overview", "render_incident_overview"),
    "trace": ("allow_trace_view", "render_trace_timeline"),
    "approvals": ("allow_approval_review", "render_approval_review"),
    "budget": ("allow_budget_view", "render_budget_panel"),
    "execution_boundaries": (
        "allow_execution_boundary_view",
        "render_execution_boundary_panel",
    ),
    "access_audit": ("allow_access_audit_view", "render_access_audit"),
}


def _index_by(items: list[dict[str, object]], key: str) -> dict[str, dict[str, object]]:
    return {str(item[key]): item for item in items}


def _deny(
    case: dict[str, object],
    decision: str,
    operator_action: str,
    audit_event: str,
    reason: str,
) -> dict[str, object]:
    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "subject_id": case["subject_id"],
        "tenant_id": case["tenant_id"],
        "role": case["role"],
        "resource_type": case["resource_type"],
        "resource_tenant_id": case["resource_tenant_id"],
        "decision": decision,
        "visible_fields": [],
        "operator_action": operator_action,
        "audit_event": audit_event,
        "expected_decision": case["expected_decision"],
        "expected_visible_fields": case["expected_visible_fields"],
        "expected_operator_action": case["expected_operator_action"],
        "expected_audit_event": case["expected_audit_event"],
        "passed": (
            decision == case["expected_decision"]
            and [] == case["expected_visible_fields"]
            and operator_action == case["expected_operator_action"]
            and audit_event == case["expected_audit_event"]
        ),
        "reasons": [reason],
    }


def _permission_for(case: dict[str, object]) -> str:
    return f"{case['resource_type']}:{case['action']}"


def _can_break_glass(case: dict[str, object]) -> bool:
    return (
        case["break_glass"] is True
        and case["role"] == "security"
        and case["resource_type"] == "incident"
        and case["action"] == "view"
        and case["policy_context"] == "active_safety_incident"
        and case["redaction_status"] == "redacted"
    )


def _decide(
    case: dict[str, object],
    roles: dict[str, dict[str, object]],
    resources: dict[str, dict[str, object]],
) -> dict[str, object]:
    role = roles.get(str(case["role"]))
    resource = resources.get(str(case["resource_type"]))
    reasons: list[str] = []

    if role is None:
        return _deny(
            case,
            "deny_unknown_role",
            "show_access_denied",
            "access_denied_unknown_role",
            "subject_role_not_in_catalog",
        )

    if resource is None:
        return _deny(
            case,
            "deny_missing_permission",
            "show_access_denied",
            "access_denied_missing_permission",
            "resource_type_not_in_catalog",
        )

    if (
        case["resource_type"] in SENSITIVE_RESOURCE_TYPES
        and case["redaction_status"] != "redacted"
    ):
        return _deny(
            case,
            "deny_unredacted_sensitive",
            "fix_redaction_before_render",
            "access_denied_redaction",
            "sensitive_resource_not_redacted",
        )

    if case["action"] == "approve" and case["approval_relationship"] == "requester":
        return _deny(
            case,
            "deny_self_approval",
            "route_to_independent_approver",
            "access_denied_self_approval",
            "subject_is_requester_for_approval",
        )

    if _can_break_glass(case):
        decision = "allow_break_glass_limited_view"
        visible_fields = [
            "incident_id",
            "severity",
            "current_status",
            "break_glass_reason",
        ]
        operator_action = "record_break_glass_review"
        audit_event = "break_glass_access_allowed"
        reasons.append("security_break_glass_limited_redacted_incident_view")
    elif case["tenant_id"] != case["resource_tenant_id"]:
        return _deny(
            case,
            "deny_cross_tenant",
            "show_access_denied",
            "access_denied_cross_tenant",
            "resource_tenant_does_not_match_subject_tenant",
        )
    elif _permission_for(case) not in role["permissions"]:
        return _deny(
            case,
            "deny_missing_permission",
            "show_access_denied",
            "access_denied_missing_permission",
            "role_lacks_requested_resource_action",
        )
    elif case["resource_type"] in ALLOW_DECISIONS:
        decision, operator_action = ALLOW_DECISIONS[str(case["resource_type"])]
        visible_fields = list(resource["default_visible_fields"])
        audit_event = (
            "approval_access_allowed"
            if case["resource_type"] == "approvals" and case["action"] == "approve"
            else "access_allowed"
        )
        reasons.append("role_permission_tenant_and_redaction_checks_passed")
    else:
        return _deny(
            case,
            "deny_missing_permission",
            "show_access_denied",
            "access_denied_missing_permission",
            "resource_has_no_allow_decision",
        )

    expected_decision = str(case["expected_decision"])
    expected_visible_fields = list(case["expected_visible_fields"])
    expected_operator_action = str(case["expected_operator_action"])
    expected_audit_event = str(case["expected_audit_event"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "subject_id": case["subject_id"],
        "tenant_id": case["tenant_id"],
        "role": case["role"],
        "resource_type": case["resource_type"],
        "resource_tenant_id": case["resource_tenant_id"],
        "decision": decision,
        "visible_fields": visible_fields,
        "operator_action": operator_action,
        "audit_event": audit_event,
        "expected_decision": expected_decision,
        "expected_visible_fields": expected_visible_fields,
        "expected_operator_action": expected_operator_action,
        "expected_audit_event": expected_audit_event,
        "passed": (
            decision == expected_decision
            and visible_fields == expected_visible_fields
            and operator_action == expected_operator_action
            and audit_event == expected_audit_event
        ),
        "reasons": reasons,
    }


def simulate_policy_aware_access() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    roles = _index_by(plan["role_catalog"], "role")
    resources = _index_by(plan["resource_catalog"], "resource_type")
    decisions = [_decide(case, roles, resources) for case in plan["access_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "policy_aware_access_simulation_no_runtime",
        "namespace": plan["namespace"],
        "auth_server_started": False,
        "identity_provider_called": False,
        "token_issued": False,
        "session_created": False,
        "api_server_started": False,
        "frontend_runtime_started": False,
        "policy_engine_started": False,
        "network_call_made": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_policy_aware_access()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
