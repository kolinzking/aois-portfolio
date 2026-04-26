#!/usr/bin/env python3
"""Simulate Phase 7 v20.2 budget-aware routing without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/budget-aware-routing.plan.json")


def _route_score(route: dict[str, object]) -> float:
    cost = float(route["estimated_cost_units"])
    value = float(route["expected_value_units"])
    return value / cost if cost else 0.0


def _route_summary(route: dict[str, object]) -> dict[str, object]:
    return {
        "route_id": route["route_id"],
        "model_tier": route["model_tier"],
        "planned_tools": route["planned_tools"],
        "estimated_cost_units": route["estimated_cost_units"],
        "expected_value_units": route["expected_value_units"],
        "value_to_cost_ratio": round(_route_score(route), 4),
    }


def _fits_budget(
    route: dict[str, object], remaining_budget: float, reserve: float
) -> bool:
    return float(route["estimated_cost_units"]) <= remaining_budget - reserve


def _best_by_id(
    routes: list[dict[str, object]], route_id: str
) -> dict[str, object] | None:
    matches = [route for route in routes if route["route_id"] == route_id]
    if not matches:
        return None
    return max(matches, key=_route_score)


def _best_viable_route(
    routes: list[dict[str, object]],
    remaining_budget: float,
    reserve: float,
    min_ratio: float,
) -> dict[str, object] | None:
    viable = [
        route
        for route in routes
        if _fits_budget(route, remaining_budget, reserve)
        and _route_score(route) >= min_ratio
    ]
    if not viable:
        return None
    return max(viable, key=lambda route: (_route_score(route), -float(route["estimated_cost_units"])))


def _decide(case: dict[str, object], plan: dict[str, object]) -> dict[str, object]:
    thresholds = plan["thresholds"]
    reserve = float(thresholds["min_remaining_budget_after_route"])
    min_ratio = float(thresholds["min_expected_value_to_cost_ratio"])
    confidence = float(case["confidence"])
    remaining_budget = float(case["remaining_budget_units"])
    severity = str(case["severity"])
    evidence_state = str(case["evidence_state"])
    routes = list(case["candidate_routes"])
    severity_limit = float(plan["severity_route_limits"][severity])

    reasons: list[str] = []
    selected_route = "none"
    selected_route_summary: dict[str, object] | None = None

    if case["accounting_complete"] is not True:
        decision = "block_incomplete_accounting"
        selected_route = "blocked"
        reasons.append("cost_ledger_incomplete")
    elif remaining_budget <= reserve:
        decision = "stop_budget_exhausted"
        selected_route = "stop"
        reasons.append("budget_reserve_exhausted")
    else:
        small_route = _best_by_id(routes, "small_model_no_tool")
        read_only_route = _best_by_id(routes, "read_only_evidence")
        full_route = _best_by_id(routes, "full_investigation")

        if (
            evidence_state == "complete"
            and confidence >= float(thresholds["min_confidence_skip_tool"])
            and small_route is not None
            and _fits_budget(small_route, remaining_budget, reserve)
            and float(small_route["estimated_cost_units"])
            <= float(thresholds["max_low_severity_route_cost"])
        ):
            decision = "route_small_model_no_tool"
            selected_route = str(small_route["route_id"])
            selected_route_summary = _route_summary(small_route)
            reasons.append("high_confidence_complete_evidence")
        elif (
            severity == "high"
            and full_route is not None
            and _fits_budget(full_route, remaining_budget, reserve)
            and float(full_route["estimated_cost_units"]) <= severity_limit
            and _route_score(full_route) >= min_ratio
        ):
            decision = "route_high_severity_full_investigation"
            selected_route = str(full_route["route_id"])
            selected_route_summary = _route_summary(full_route)
            reasons.append("high_severity_value_justifies_full_route")
        elif (
            read_only_route is not None
            and evidence_state in {"partial", "missing"}
            and _fits_budget(read_only_route, remaining_budget, reserve)
            and float(read_only_route["estimated_cost_units"]) <= severity_limit
            and _route_score(read_only_route) >= min_ratio
        ):
            decision = "route_read_only_tool"
            selected_route = str(read_only_route["route_id"])
            selected_route_summary = _route_summary(read_only_route)
            reasons.append("bounded_read_only_route_has_positive_value")
        else:
            best = _best_viable_route(routes, remaining_budget, reserve, min_ratio)
            if (
                best is not None
                and severity != "high"
                and float(best["estimated_cost_units"])
                >= float(thresholds["expensive_branch_review_cost"])
            ):
                decision = "request_budget_review"
                selected_route = "human_budget_review"
                selected_route_summary = _route_summary(best)
                reasons.append("expensive_non_high_severity_branch_requires_review")
            else:
                decision = "stop_budget_exhausted"
                selected_route = "stop"
                reasons.append("no_viable_route_within_policy")

    expected_decision = str(case["expected_decision"])
    expected_route = str(case["expected_route"])
    return {
        "case": case["name"],
        "incident_id": case["incident_id"],
        "severity": severity,
        "evidence_state": evidence_state,
        "remaining_budget_units": remaining_budget,
        "candidate_routes": [_route_summary(route) for route in routes],
        "decision": decision,
        "selected_route": selected_route,
        "selected_route_summary": selected_route_summary,
        "expected_decision": expected_decision,
        "expected_route": expected_route,
        "passed": decision == expected_decision and selected_route == expected_route,
        "reasons": reasons,
        "next_action": case["expected_next_action"],
    }


def simulate_budget_aware_routing() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case, plan) for case in plan["incident_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "budget_aware_routing_simulation_no_runtime",
        "namespace": plan["namespace"],
        "agent_runtime_started": False,
        "routing_runtime_started": False,
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
    result = simulate_budget_aware_routing()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
