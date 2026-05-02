#!/usr/bin/env python3
"""Simulate Phase 9 v29 experiment/model delivery decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PLAN_PATH = Path("release-safety/aois-p/experiment-model-delivery.plan.json")


def _expand_case(defaults: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    expanded = dict(defaults)
    expanded["metric_delta"] = dict(defaults["metric_delta"])
    overrides = case.get("overrides", {})
    for key, value in overrides.items():
        if key == "metric_delta" and isinstance(value, dict):
            expanded["metric_delta"].update(value)
        else:
            expanded[key] = value
    expanded["case_id"] = case["case_id"]
    expanded["name"] = case["name"]
    return expanded


def _metric_regressed(case: dict[str, Any]) -> bool:
    metric_delta = case["metric_delta"]
    return (
        metric_delta["quality_score"] < 0.02
        or metric_delta["latency_p95_ms"] > 200
        or metric_delta["cost_per_1k_tokens"] > 0.05
    )


def _guardrail_regressed(case: dict[str, Any]) -> bool:
    metric_delta = case["metric_delta"]
    return (
        case["guardrail_status"] != "pass"
        or metric_delta["safety_violation_rate"] > 0
        or metric_delta["policy_regression_count"] > 0
        or metric_delta["tenant_isolation_failures"] > 0
    )


def _decision(case: dict[str, Any]) -> tuple[str, str, str, str]:
    if case["hypothesis_status"] != "documented":
        return (
            "block_missing_hypothesis",
            "document_experiment_hypothesis",
            "blocked",
            "experiment_hypothesis_missing",
        )
    if not case["baseline_model_version"]:
        return (
            "block_missing_baseline",
            "set_baseline_model_version",
            "blocked",
            "baseline_model_version_missing",
        )
    if not case["candidate_model_version"]:
        return (
            "block_missing_candidate_version",
            "set_candidate_model_version",
            "blocked",
            "candidate_model_version_missing",
        )
    if not case["dataset_version"]:
        return (
            "block_missing_dataset_version",
            "pin_eval_dataset_version",
            "blocked",
            "dataset_version_missing",
        )
    if case["offline_eval_status"] != "pass":
        return (
            "block_offline_eval_failed",
            "fix_or_rerun_offline_eval",
            "blocked",
            "offline_eval_failed",
        )
    if _metric_regressed(case):
        return (
            "block_metric_regression",
            "investigate_metric_regression",
            "blocked",
            "quality_latency_or_cost_metric_regressed",
        )
    if _guardrail_regressed(case):
        return (
            "block_guardrail_regression",
            "fix_guardrail_regression",
            "blocked",
            "safety_policy_or_tenant_guardrail_regressed",
        )
    if case["sample_size_status"] != "sufficient":
        return (
            "hold_sample_size_insufficient",
            "collect_more_rollout_samples",
            "held",
            "rollout_sample_size_insufficient",
        )
    if case["rollout_evidence_status"] != "complete":
        return (
            "hold_missing_rollout_evidence",
            "collect_rollout_evidence",
            "held",
            "rollout_evidence_missing",
        )
    if case["model_registry_status"] != "complete":
        return (
            "block_registry_incomplete",
            "complete_model_registry_record",
            "blocked",
            "model_registry_record_incomplete",
        )
    if case["release_gate_status"] != "pass":
        return (
            "block_release_gate_failed",
            "return_to_release_gate",
            "blocked",
            "release_gate_failed",
        )
    if case["feature_flag_status"] != "guarded":
        return (
            "hold_feature_flag_not_ready",
            "repair_feature_flag_guard",
            "held",
            "feature_flag_not_guarded",
        )
    if case["rollback_ready"] is not True:
        return (
            "block_no_rollback",
            "define_model_rollback_target",
            "blocked",
            "model_rollback_target_missing",
        )
    if case["approval_status"] != "approved":
        return (
            "block_missing_approval",
            "request_model_delivery_approval",
            "blocked",
            "model_delivery_approval_missing",
        )
    if case["risk_status"] != "accepted":
        return (
            "hold_risk_review",
            "complete_risk_review",
            "held",
            "risk_review_not_accepted",
        )
    return (
        "allow_model_delivery_candidate",
        "promote_challenger_with_evidence",
        "candidate_ready",
        "all_experiment_and_delivery_evidence_passed",
    )


def _decide(defaults: dict[str, Any], raw_case: dict[str, Any]) -> dict[str, Any]:
    case = _expand_case(defaults, raw_case)
    decision, operator_action, delivery_state, reason = _decision(case)
    expected_decision = str(raw_case["expected_decision"])
    expected_operator_action = str(raw_case["expected_operator_action"])
    expected_delivery_state = str(raw_case["expected_delivery_state"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "experiment_id": case["experiment_id"],
        "change_id": case["change_id"],
        "baseline_model_version": case["baseline_model_version"],
        "candidate_model_version": case["candidate_model_version"],
        "decision": decision,
        "operator_action": operator_action,
        "delivery_state": delivery_state,
        "expected_decision": expected_decision,
        "expected_operator_action": expected_operator_action,
        "expected_delivery_state": expected_delivery_state,
        "passed": (
            decision == expected_decision
            and operator_action == expected_operator_action
            and delivery_state == expected_delivery_state
        ),
        "reasons": [reason],
    }


def simulate_experiment_model_delivery() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    defaults = plan["case_defaults"]
    decisions = [_decide(defaults, case) for case in plan["delivery_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "experiment_model_delivery_simulation_no_runtime",
        "namespace": plan["namespace"],
        "experiment_tracker_started": False,
        "model_registry_started": False,
        "training_job_started": False,
        "eval_job_started": False,
        "model_downloaded": False,
        "model_uploaded": False,
        "model_promoted": False,
        "traffic_shifted": False,
        "feature_flag_service_called": False,
        "rollout_controller_started": False,
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
    result = simulate_experiment_model_delivery()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
