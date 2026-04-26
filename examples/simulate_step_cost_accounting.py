#!/usr/bin/env python3
"""Simulate Phase 7 v20.1 cost accounting decisions without runtime."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/step-cost-accounting.plan.json")


def _step_cost(step: dict[str, object], unit_costs: dict[str, object]) -> dict[str, object]:
    usage = step["usage"]
    input_cost = (
        float(usage["input_tokens"])
        / 1000
        * float(unit_costs["model_input_per_1k_tokens"])
    )
    cached_input_cost = (
        float(usage["cached_input_tokens"])
        / 1000
        * float(unit_costs["model_cached_input_per_1k_tokens"])
    )
    output_cost = (
        float(usage["output_tokens"])
        / 1000
        * float(unit_costs["model_output_per_1k_tokens"])
    )
    reasoning_cost = (
        float(usage["reasoning_tokens"])
        / 1000
        * float(unit_costs["model_reasoning_per_1k_tokens"])
    )
    tool_cost = float(usage["tool_call_count"]) * float(
        unit_costs["read_only_tool_call"]
    )
    approval_wait_cost = float(usage["approval_wait_minutes"]) * float(
        unit_costs["approval_wait_minute"]
    )
    retry_cost = float(usage["retry_count"]) * float(unit_costs["retry_penalty"])
    invalid_result_cost = (
        0.0 if step["result_valid"] is True else float(unit_costs["invalid_result_penalty"])
    )
    total = (
        input_cost
        + cached_input_cost
        + output_cost
        + reasoning_cost
        + tool_cost
        + approval_wait_cost
        + retry_cost
        + invalid_result_cost
    )

    return {
        "step_id": step["step_id"],
        "planned_tool": step["planned_tool"],
        "accounted": step["accounted"],
        "input_cost_units": round(input_cost, 4),
        "cached_input_cost_units": round(cached_input_cost, 4),
        "output_cost_units": round(output_cost, 4),
        "reasoning_cost_units": round(reasoning_cost, 4),
        "tool_cost_units": round(tool_cost, 4),
        "approval_wait_cost_units": round(approval_wait_cost, 4),
        "retry_cost_units": round(retry_cost, 4),
        "invalid_result_cost_units": round(invalid_result_cost, 4),
        "cost_units": round(total, 4),
    }


def _decide(case: dict[str, object], plan: dict[str, object]) -> dict[str, object]:
    unit_costs = plan["unit_costs"]
    thresholds = plan["thresholds"]
    step_costs = [_step_cost(step, unit_costs) for step in case["steps"]]
    total_cost = round(sum(float(step["cost_units"]) for step in step_costs), 4)
    approval_wait_cost = round(
        sum(float(step["approval_wait_cost_units"]) for step in step_costs), 4
    )

    tool_counts = Counter(
        step["planned_tool"]
        for step in case["steps"]
        if int(step["usage"]["tool_call_count"]) > 0
    )

    reasons: list[str] = []
    if any(step["accounted"] is not True for step in case["steps"]):
        decision = "accounting_incomplete"
        reasons.append("required_step_usage_record_missing")
    elif approval_wait_cost > float(thresholds["max_approval_wait_cost_units"]):
        decision = "approval_cost_review"
        reasons.append("approval_wait_cost_exceeded")
    elif total_cost > float(thresholds["max_total_cost_units_per_incident"]):
        decision = "incident_budget_exceeded"
        reasons.append("incident_cost_exceeded")
    elif any(
        count > int(thresholds["max_same_tool_calls_per_incident"])
        for count in tool_counts.values()
    ):
        decision = "step_waste_flagged"
        reasons.append("same_tool_repeated")
    elif any(
        int(step["usage"]["retry_count"]) > int(thresholds["max_retries_per_step"])
        for step in case["steps"]
    ):
        decision = "step_waste_flagged"
        reasons.append("retry_threshold_exceeded")
    elif any(
        float(step["cost_units"]) > float(thresholds["max_step_cost_units"])
        for step in step_costs
    ):
        decision = "step_waste_flagged"
        reasons.append("step_cost_exceeded")
    else:
        decision = "within_budget"
        reasons.append("accounting_complete_and_within_budget")

    expected = str(case["expected_decision"])
    return {
        "case": case["name"],
        "incident_id": case["incident_id"],
        "step_costs": step_costs,
        "total_cost_units": total_cost,
        "approval_wait_cost_units": approval_wait_cost,
        "decision": decision,
        "expected_decision": expected,
        "passed": decision == expected,
        "reasons": reasons,
        "next_action": case["expected_next_action"],
    }


def simulate_step_cost_accounting() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case, plan) for case in plan["incident_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "step_cost_accounting_simulation_no_runtime",
        "namespace": plan["namespace"],
        "agent_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "billing_api_called": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_step_cost_accounting()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
