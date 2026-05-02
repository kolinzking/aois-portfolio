#!/usr/bin/env python3
"""Simulate Phase 7 v24 multi-agent collaboration decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/multi-agent-collaboration.plan.json")


def _role_targets(plan: dict[str, object]) -> dict[str, set[str]]:
    return {
        str(role["agent_id"]): {str(target) for target in role["allowed_targets"]}
        for role in plan["role_catalog"]
    }


def _decide(case: dict[str, object], plan: dict[str, object]) -> dict[str, object]:
    targets = _role_targets(plan)
    current_agent = str(case["current_agent"])
    requested_target = str(case["requested_target"])
    reasons: list[str] = []

    if case["autonomy_mode"] == "shadow":
        decision = "hold_autonomy_mode"
        next_agent = current_agent
        next_action = "record_shadow_collaboration"
        reasons.append("shadow_mode_records_plan_without_handoff")
    elif requested_target not in targets.get(current_agent, set()):
        decision = "block_unknown_agent"
        next_agent = current_agent
        next_action = "reject_handoff"
        reasons.append("requested_target_not_allowed")
    elif int(case["handoff_count"]) >= int(case["max_handoffs"]):
        decision = "stop_handoff_loop"
        next_agent = current_agent
        next_action = "stop_and_review_loop"
        reasons.append("handoff_limit_reached")
    elif case["parallel_requested"] is True:
        decision = "block_parallel_handoff"
        next_agent = current_agent
        next_action = "serialize_handoffs"
        reasons.append("parallel_specialist_handoffs_disabled")
    elif case["context_status"] != "fresh":
        decision = "block_stale_context"
        next_agent = current_agent
        next_action = "refresh_shared_state"
        reasons.append("shared_state_context_not_fresh")
    elif case["conflict_status"] != "none":
        decision = "escalate_conflict"
        next_agent = "human_operator"
        next_action = "escalate_to_operator"
        reasons.append("specialist_findings_conflict")
    elif requested_target == "evidence_agent" and case["evidence_state"] == "missing":
        decision = "handoff_to_evidence_agent"
        next_agent = "evidence_agent"
        next_action = "request_evidence_plan"
        reasons.append("missing_evidence_requires_specialist")
    elif requested_target == "safety_agent" and case["safety_status"] == "review_required":
        decision = "handoff_to_safety_agent"
        next_agent = "safety_agent"
        next_action = "request_safety_review"
        reasons.append("safety_review_required")
    elif requested_target == "budget_agent" and case["budget_status"] == "review_required":
        decision = "handoff_to_budget_agent"
        next_agent = "budget_agent"
        next_action = "request_budget_review"
        reasons.append("budget_review_required")
    elif (
        requested_target == "response_agent"
        and case["evidence_state"] == "complete"
        and case["safety_status"] == "clear"
        and case["budget_status"] == "within_budget"
    ):
        decision = "handoff_to_response_agent"
        next_agent = "response_agent"
        next_action = "request_final_synthesis"
        reasons.append("ready_for_final_synthesis")
    else:
        decision = "block_unknown_agent"
        next_agent = current_agent
        next_action = "reject_handoff"
        reasons.append("no_collaboration_rule_matched")

    expected_decision = str(case["expected_decision"])
    expected_next_agent = str(case["expected_next_agent"])
    expected_next_action = str(case["expected_next_action"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "current_agent": current_agent,
        "requested_target": requested_target,
        "decision": decision,
        "next_agent": next_agent,
        "next_action": next_action,
        "expected_decision": expected_decision,
        "expected_next_agent": expected_next_agent,
        "expected_next_action": expected_next_action,
        "passed": (
            decision == expected_decision
            and next_agent == expected_next_agent
            and next_action == expected_next_action
        ),
        "reasons": reasons,
    }


def simulate_multi_agent_collaboration() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case, plan) for case in plan["collaboration_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "multi_agent_collaboration_simulation_no_runtime",
        "namespace": plan["namespace"],
        "agent_runtime_started": False,
        "multi_agent_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_multi_agent_collaboration()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
