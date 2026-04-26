#!/usr/bin/env python3
"""Simulate Phase 7 v20 tool-using incident responder decisions without tools."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/tool-using-responder.plan.json")


def _decide(case: dict[str, object], plan: dict[str, object]) -> dict[str, object]:
    thresholds = plan["thresholds"]
    minimum_confidence = float(thresholds["minimum_confidence_for_answer"])
    blocked_tools = set(plan["blocked_tools_without_human_approval"])
    allowed_tools = {tool["name"] for tool in plan["allowed_read_only_tools"]}

    planned_sequence = list(case["planned_tool_sequence"])
    blocked_requested = [
        tool_name for tool_name in planned_sequence if tool_name in blocked_tools
    ]
    unknown_requested = [
        tool_name
        for tool_name in planned_sequence
        if tool_name not in allowed_tools and tool_name not in blocked_tools
    ]

    reasons: list[str] = []
    if unknown_requested:
        reasons.append("unknown_tool_requested")
    if case["secret_detected"] is True:
        decision = "block_and_redact"
        reasons.append("secret_detected")
    elif blocked_requested or case["mutating_tool_requested"] is True:
        decision = "request_human_approval"
        reasons.append("mutating_tool_requires_human_approval")
    elif case["tool_result_schema_valid"] is not True:
        decision = "fallback_to_runbook"
        reasons.append("tool_result_schema_invalid")
    elif case["evidence_complete"] is not True:
        decision = "gather_more_evidence"
        reasons.append("evidence_incomplete")
    elif float(case["confidence"]) < minimum_confidence:
        decision = "gather_more_evidence"
        reasons.append("confidence_below_threshold")
    else:
        decision = "answer_with_evidence"
        reasons.append("evidence_complete")

    planned_steps = [
        {
            "tool": tool_name,
            "allowed": tool_name in allowed_tools,
            "requires_human_approval": tool_name in blocked_tools,
            "executed": False,
        }
        for tool_name in planned_sequence
    ]
    expected = str(case["expected_decision"])

    return {
        "case": case["name"],
        "incident_id": case["incident_id"],
        "planned_steps": planned_steps,
        "decision": decision,
        "expected_decision": expected,
        "passed": decision == expected and not unknown_requested,
        "reasons": reasons,
        "next_action": case["expected_next_action"],
    }


def simulate_tool_using_responder() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case, plan) for case in plan["incident_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "tool_using_responder_simulation_no_runtime",
        "namespace": plan["namespace"],
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
    result = simulate_tool_using_responder()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
