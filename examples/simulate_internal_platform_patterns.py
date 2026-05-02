#!/usr/bin/env python3
"""Simulate Phase 9 v30 internal platform decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PLAN_PATH = Path("platform/aois-p/internal-platform-patterns.plan.json")


def _expand_case(defaults: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    expanded = dict(defaults)
    expanded.update(case.get("overrides", {}))
    expanded["case_id"] = case["case_id"]
    expanded["name"] = case["name"]
    return expanded


def _requires_approval(case: dict[str, Any], capabilities: dict[str, dict[str, Any]]) -> bool:
    capability = capabilities.get(str(case["capability_id"]))
    return bool(capability and capability["requires_approval"])


def _decision(
    case: dict[str, Any], capabilities: dict[str, dict[str, Any]]
) -> tuple[str, str, str, str]:
    if case["capability_id"] not in capabilities:
        return (
            "block_unknown_capability",
            "register_capability_or_reject_request",
            "blocked",
            "capability_not_in_catalog",
        )
    if case["lifecycle_status"] != "active":
        return (
            "block_deprecated_capability",
            "route_to_supported_capability",
            "blocked",
            "capability_lifecycle_not_active",
        )
    if not case["owner"]:
        return (
            "block_missing_owner",
            "assign_platform_owner",
            "blocked",
            "platform_owner_missing",
        )
    if case["documentation_status"] != "complete":
        return (
            "block_missing_docs",
            "write_onboarding_docs",
            "blocked",
            "documentation_missing",
        )
    if case["api_contract_status"] != "complete":
        return (
            "block_missing_api_contract",
            "define_platform_api_contract",
            "blocked",
            "platform_api_contract_missing",
        )
    if case["template_status"] != "complete":
        return (
            "block_missing_template",
            "create_golden_path_template",
            "blocked",
            "golden_path_template_missing",
        )
    if case["policy_status"] != "pass":
        return (
            "block_policy_boundary",
            "repair_policy_defaults",
            "blocked",
            "policy_defaults_or_boundary_failed",
        )
    if case["security_status"] != "pass":
        return (
            "block_security_boundary",
            "repair_security_boundary",
            "blocked",
            "security_boundary_failed",
        )
    if case["cost_status"] != "approved":
        return (
            "hold_cost_review",
            "complete_cost_and_quota_review",
            "held",
            "cost_or_quota_review_pending",
        )
    if case["observability_status"] != "complete":
        return (
            "block_observability_missing",
            "add_observability_contract",
            "blocked",
            "observability_contract_missing",
        )
    if case["release_integration_status"] != "complete":
        return (
            "block_release_integration_missing",
            "connect_v28_release_controls",
            "blocked",
            "v28_release_controls_not_connected",
        )
    if (
        case["capability_id"] == "model_delivery_bundle"
        and case["model_delivery_status"] != "complete"
    ):
        return (
            "hold_model_delivery_integration",
            "connect_v29_model_delivery_tracking",
            "held",
            "v29_model_delivery_tracking_not_connected",
        )
    if case["tenant_boundary_status"] != "complete":
        return (
            "block_tenant_boundary_missing",
            "define_tenant_and_permission_boundaries",
            "blocked",
            "tenant_or_permission_boundary_missing",
        )
    if _requires_approval(case, capabilities) and case["approval_status"] != "approved":
        return (
            "block_approval_missing",
            "request_platform_capability_approval",
            "blocked",
            "required_capability_approval_missing",
        )
    if case["support_slo_status"] != "defined":
        return (
            "hold_support_slo_missing",
            "define_support_slo",
            "held",
            "support_slo_missing",
        )
    return (
        "allow_self_service_capability",
        "publish_self_service_capability",
        "available",
        "platform_capability_contract_complete",
    )


def _decide(
    defaults: dict[str, Any],
    raw_case: dict[str, Any],
    capabilities: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    case = _expand_case(defaults, raw_case)
    decision, operator_action, platform_state, reason = _decision(case, capabilities)
    expected_decision = str(raw_case["expected_decision"])
    expected_operator_action = str(raw_case["expected_operator_action"])
    expected_platform_state = str(raw_case["expected_platform_state"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "capability_id": case["capability_id"],
        "user_persona": case["user_persona"],
        "interface_type": case["interface_type"],
        "decision": decision,
        "operator_action": operator_action,
        "platform_state": platform_state,
        "expected_decision": expected_decision,
        "expected_operator_action": expected_operator_action,
        "expected_platform_state": expected_platform_state,
        "passed": (
            decision == expected_decision
            and operator_action == expected_operator_action
            and platform_state == expected_platform_state
        ),
        "reasons": [reason],
    }


def simulate_internal_platform_patterns() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    defaults = plan["case_defaults"]
    capabilities = {
        str(capability["capability_id"]): capability
        for capability in plan["capability_catalog"]
    }
    decisions = [
        _decide(defaults, case, capabilities) for case in plan["platform_cases"]
    ]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "internal_platform_patterns_simulation_no_runtime",
        "namespace": plan["namespace"],
        "platform_runtime_started": False,
        "developer_portal_started": False,
        "service_catalog_started": False,
        "platform_api_started": False,
        "template_engine_started": False,
        "cli_invoked": False,
        "infrastructure_provisioned": False,
        "kubernetes_applied": False,
        "gitops_sync_started": False,
        "workflow_started": False,
        "database_started": False,
        "network_call_made": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_internal_platform_patterns()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
