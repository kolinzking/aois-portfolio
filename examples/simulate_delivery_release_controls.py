#!/usr/bin/env python3
"""Simulate Phase 9 v28 delivery release decisions without CI/runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("release-safety/aois-p/delivery-release-controls.plan.json")


def _expand_case(defaults: dict[str, object], case: dict[str, object]) -> dict[str, object]:
    expanded = dict(defaults)
    expanded.update(case.get("overrides", {}))
    expanded["case_id"] = case["case_id"]
    expanded["name"] = case["name"]
    expanded["change_id"] = case.get("change_id", f"change-{case['case_id']}")
    expanded["source_revision"] = case.get("source_revision", f"rev-{case['case_id']}")
    return expanded


def _decision(case: dict[str, object]) -> tuple[str, str, str, str]:
    if case["branch_status"] != "reviewed":
        return (
            "block_unreviewed_branch",
            "return_to_code_review",
            "blocked",
            "branch_policy_or_review_missing",
        )
    if case["workflow_permissions"] != "least_privilege":
        return (
            "block_workflow_overprivileged",
            "reduce_workflow_permissions",
            "blocked",
            "workflow_permissions_too_broad",
        )
    if case["dependency_review"] != "pass":
        return (
            "block_dependency_review_failed",
            "resolve_dependency_risk",
            "blocked",
            "dependency_review_failed",
        )
    if case["test_status"] != "pass":
        return (
            "block_tests_failed",
            "fix_regression_tests",
            "blocked",
            "build_or_regression_tests_failed",
        )
    if case["policy_test_status"] != "pass":
        return (
            "block_policy_tests_failed",
            "fix_aois_policy_regressions",
            "blocked",
            "aois_policy_regression_tests_failed",
        )
    if case["security_scan_status"] != "pass":
        return (
            "block_security_scan_failed",
            "resolve_security_findings",
            "blocked",
            "security_scan_failed",
        )
    if not case["artifact_digest"]:
        return (
            "block_missing_digest",
            "produce_artifact_digest",
            "blocked",
            "artifact_digest_missing",
        )
    if case["provenance_status"] != "present":
        return (
            "block_missing_provenance",
            "produce_build_provenance",
            "blocked",
            "build_provenance_missing",
        )
    if case["signature_status"] == "missing":
        return (
            "block_unsigned_artifact",
            "sign_release_artifact",
            "blocked",
            "artifact_signature_missing",
        )
    if case["signature_status"] != "verified":
        return (
            "block_signature_unverified",
            "verify_artifact_signature",
            "blocked",
            "artifact_signature_not_verified",
        )
    if case["environment_approval"] != "approved":
        return (
            "block_missing_environment_approval",
            "request_environment_approval",
            "blocked",
            "environment_approval_missing",
        )
    if case["health_status"] != "healthy":
        return (
            "hold_rollout_health",
            "pause_rollout_and_investigate_health",
            "held",
            "rollout_health_not_healthy",
        )
    if case["rollback_ready"] is not True:
        return (
            "block_no_rollback",
            "define_rollback_target",
            "blocked",
            "rollback_plan_missing",
        )
    if case["model_rollout_status"] != "staged":
        return (
            "hold_model_rollout",
            "stage_model_rollout",
            "held",
            "model_rollout_not_staged",
        )
    if case["feature_flag_status"] != "guarded":
        return (
            "hold_feature_flag",
            "repair_feature_flag_guard",
            "held",
            "feature_flag_not_guarded",
        )
    return (
        "allow_release_candidate",
        "promote_canary",
        "candidate_ready",
        "all_release_gates_passed",
    )


def _decide(defaults: dict[str, object], raw_case: dict[str, object]) -> dict[str, object]:
    case = _expand_case(defaults, raw_case)
    decision, operator_action, release_state, reason = _decision(case)
    expected_decision = str(raw_case["expected_decision"])
    expected_operator_action = str(raw_case["expected_operator_action"])
    expected_release_state = str(raw_case["expected_release_state"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "change_id": case["change_id"],
        "source_revision": case["source_revision"],
        "decision": decision,
        "operator_action": operator_action,
        "release_state": release_state,
        "expected_decision": expected_decision,
        "expected_operator_action": expected_operator_action,
        "expected_release_state": expected_release_state,
        "passed": (
            decision == expected_decision
            and operator_action == expected_operator_action
            and release_state == expected_release_state
        ),
        "reasons": [reason],
    }


def simulate_delivery_release_controls() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    defaults = plan["case_defaults"]
    decisions = [_decide(defaults, case) for case in plan["release_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "delivery_release_controls_simulation_no_runtime",
        "namespace": plan["namespace"],
        "ci_runtime_started": False,
        "workflow_started": False,
        "build_started": False,
        "test_runner_started": False,
        "container_build_started": False,
        "image_pushed": False,
        "image_signed": False,
        "signature_verified": False,
        "deployment_started": False,
        "kubernetes_applied": False,
        "rollout_started": False,
        "traffic_shifted": False,
        "feature_flag_service_called": False,
        "model_endpoint_changed": False,
        "network_call_made": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_delivery_release_controls()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
