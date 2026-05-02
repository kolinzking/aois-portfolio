#!/usr/bin/env python3
"""Simulate Phase 7 v23.5 agent evaluation scoring without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/agent-evaluation.plan.json")


def _score_case(
    case: dict[str, object], metrics: list[dict[str, object]], min_case_score: float
) -> dict[str, object]:
    expected = case["expected"]
    observed = case["observed"]
    assert isinstance(expected, dict)
    assert isinstance(observed, dict)

    metric_results: list[dict[str, object]] = []
    weighted_score = 0.0
    critical_pass = True

    for metric in metrics:
        field = str(metric["field"])
        weight = float(metric["weight"])
        passed = expected.get(field) == observed.get(field)
        score = 1.0 if passed else 0.0
        weighted_score += score * weight
        if metric["critical"] is True and not passed:
            critical_pass = False
        metric_results.append(
            {
                "metric_id": metric["metric_id"],
                "field": field,
                "expected": expected.get(field),
                "observed": observed.get(field),
                "weight": weight,
                "critical": metric["critical"],
                "score": score,
                "passed": passed,
            }
        )

    weighted_score = round(weighted_score, 6)
    passed_case = weighted_score >= min_case_score and critical_pass
    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "case_type": case["case_type"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "weighted_score": weighted_score,
        "critical_pass": critical_pass,
        "passed": passed_case,
        "metric_results": metric_results,
    }


def simulate_agent_evaluation() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    metrics = list(plan["metric_catalog"])
    thresholds = plan["thresholds"]
    min_case_score = float(thresholds["min_case_score"])

    case_results = [_score_case(case, metrics, min_case_score) for case in plan["eval_cases"]]
    passed_cases = sum(1 for case in case_results if case["passed"])
    total_cases = len(case_results)
    overall_score = (
        sum(float(case["weighted_score"]) for case in case_results) / total_cases
        if total_cases
        else 0.0
    )
    safety_metric_fields = {
        str(metric["field"]) for metric in metrics if metric["critical"] is True
    }
    safety_checks = [
        result
        for case in case_results
        for result in case["metric_results"]
        if result["field"] in safety_metric_fields
    ]
    safety_score = (
        sum(float(result["score"]) for result in safety_checks) / len(safety_checks)
        if safety_checks
        else 0.0
    )
    critical_pass_rate = (
        sum(1 for case in case_results if case["critical_pass"]) / total_cases
        if total_cases
        else 0.0
    )

    status = "pass"
    if passed_cases != total_cases:
        status = "fail"
    if round(overall_score, 6) < float(thresholds["min_overall_score"]):
        status = "fail"
    if round(safety_score, 6) < float(thresholds["min_safety_score"]):
        status = "fail"
    if round(critical_pass_rate, 6) < float(thresholds["min_critical_pass_rate"]):
        status = "fail"

    return {
        "mode": "agent_evaluation_simulation_no_runtime",
        "namespace": plan["namespace"],
        "agent_runtime_started": False,
        "evaluation_runtime_started": False,
        "provider_call_made": False,
        "external_eval_service_called": False,
        "tool_calls_executed": False,
        "case_results": case_results,
        "passed_cases": passed_cases,
        "total_cases": total_cases,
        "overall_score": round(overall_score, 6),
        "safety_score": round(safety_score, 6),
        "critical_pass_rate": round(critical_pass_rate, 6),
        "status": status,
    }


def main() -> int:
    result = simulate_agent_evaluation()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
