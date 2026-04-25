#!/usr/bin/env python3
"""Simulate Phase 6 v19.5 AI governance decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("release-safety/aois-p/ai-failure-governance.plan.json")


def _decide(case: dict[str, object], minimum_confidence: float) -> dict[str, object]:
    blockers: list[str] = []
    review_reasons: list[str] = []

    if case["policy_boundary_passed"] is not True:
        blockers.append("policy_boundary_failed")
    if case["secret_detected"] is True:
        blockers.append("secret_detected")
    if case["destructive_action_requested"] is True:
        blockers.append("destructive_action_requires_human_approval")

    if case["evidence_present"] is not True:
        review_reasons.append("evidence_missing")
    if float(case["confidence"]) < minimum_confidence:
        review_reasons.append("confidence_below_threshold")

    if blockers:
        decision = "block"
        action = "do not send to provider or tool execution; escalate to owner"
    elif case["schema_valid"] is not True or case["model_quality_ok"] is not True:
        decision = "fallback_to_local_baseline"
        action = "use deterministic baseline and record model quality failure"
    elif review_reasons:
        decision = "review"
        action = "route to human review with evidence request"
    else:
        decision = "allow"
        action = "allow local recommendation; keep audit record"

    expected = str(case["expected_decision"])
    return {
        "case": case["name"],
        "decision": decision,
        "expected_decision": expected,
        "passed": decision == expected,
        "blockers": blockers,
        "review_reasons": review_reasons,
        "recommended_action": action,
    }


def simulate_ai_failure_governance() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    minimum_confidence = float(plan["thresholds"]["minimum_confidence_for_allow"])
    decisions = [
        _decide(case, minimum_confidence)
        for case in plan["evaluation_cases"]
    ]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "ai_failure_governance_simulation_no_runtime",
        "namespace": plan["namespace"],
        "governance_runtime_started": False,
        "policy_engine_started": False,
        "agent_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_ai_failure_governance()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
