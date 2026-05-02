#!/usr/bin/env python3
"""Simulate Phase 7 v23 stateful orchestration loop decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/stateful-orchestration.plan.json")

TERMINAL_STATES = {"completed", "blocked", "failed", "timed_out"}
REGISTRY_BLOCKS = {
    "block_unregistered_tool",
    "block_untrusted_server",
    "block_side_effecting_tool",
    "block_disabled_tool",
}


def _decide(case: dict[str, object], plan: dict[str, object]) -> dict[str, object]:
    policy = plan["loop_policy"]
    reserve = float(policy["min_budget_reserve_units"])
    state = str(case["current_state"])
    registry_decision = str(case["registry_decision"])
    approval_status = str(case["approval_status"])
    iteration = int(case["iteration"])
    max_iterations = int(case["max_iterations"])
    budget = float(case["budget_remaining_units"])
    state_hash = str(case["state_hash"])
    previous_state_hash = str(case["previous_state_hash"])

    reasons: list[str] = []
    terminal_status = "non_terminal"

    if state in TERMINAL_STATES:
        decision = "stop_terminal_state"
        next_action = "stop"
        stop_reason = "terminal_state"
        terminal_status = state
        reasons.append(f"workflow_state_is_terminal:{state}")
    elif iteration >= max_iterations:
        decision = "stop_iteration_limit"
        next_action = "stop"
        stop_reason = "iteration_limit"
        reasons.append("loop_iteration_limit_reached")
    elif state_hash == previous_state_hash:
        decision = "stop_no_progress"
        next_action = "stop"
        stop_reason = "no_state_change"
        reasons.append("state_hash_did_not_change")
    elif budget <= reserve:
        decision = "stop_budget_reserve"
        next_action = "stop"
        stop_reason = "budget_reserve"
        reasons.append("remaining_budget_at_or_below_reserve")
    elif registry_decision in REGISTRY_BLOCKS:
        decision = "stop_registry_block"
        next_action = "stop"
        stop_reason = "registry_block"
        terminal_status = "blocked"
        reasons.append(f"registry_decision_blocks_orchestration:{registry_decision}")
    elif state == "waiting_for_approval" and approval_status == "required_missing":
        decision = "wait_for_approval"
        next_action = "wait_for_approval"
        stop_reason = "approval_required"
        reasons.append("human_approval_is_required_before_next_action")
    elif state == "waiting_for_approval" and approval_status == "granted":
        decision = "resume_after_approval"
        next_action = "record_evidence_plan"
        stop_reason = "none"
        reasons.append("approval_granted_resume_evidence_plan")
    elif state == "registry_checked" and registry_decision == "allow_read_only_tool_plan":
        decision = "plan_read_only_evidence"
        next_action = "record_evidence_plan"
        stop_reason = "none"
        reasons.append("read_only_registry_plan_can_be_recorded")
    elif state == "evidence_recorded":
        decision = "prepare_answer"
        next_action = "prepare_answer"
        stop_reason = "none"
        reasons.append("evidence_recorded_answer_can_be_prepared")
    elif state == "answer_prepared":
        decision = "close_workflow"
        next_action = "close_workflow"
        stop_reason = "none"
        reasons.append("answer_prepared_workflow_can_close")
    else:
        decision = "stop_no_progress"
        next_action = "stop"
        stop_reason = "unhandled_state"
        reasons.append(f"no_rule_matched_state:{state}")

    expected_decision = str(case["expected_decision"])
    expected_next_action = str(case["expected_next_action"])
    expected_stop_reason = str(case["expected_stop_reason"])
    expected_terminal_status = str(case["expected_terminal_status"])

    return {
        "case": case["name"],
        "loop_id": case["loop_id"],
        "workflow_id": case["workflow_id"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "current_state": state,
        "route_decision": case["route_decision"],
        "registry_decision": registry_decision,
        "approval_status": approval_status,
        "iteration": iteration,
        "max_iterations": max_iterations,
        "budget_remaining_units": budget,
        "decision": decision,
        "next_action": next_action,
        "stop_reason": stop_reason,
        "terminal_status": terminal_status,
        "expected_decision": expected_decision,
        "expected_next_action": expected_next_action,
        "expected_stop_reason": expected_stop_reason,
        "expected_terminal_status": expected_terminal_status,
        "passed": (
            decision == expected_decision
            and next_action == expected_next_action
            and stop_reason == expected_stop_reason
            and terminal_status == expected_terminal_status
        ),
        "reasons": reasons,
    }


def simulate_stateful_orchestration() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case, plan) for case in plan["orchestration_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "stateful_orchestration_simulation_no_runtime",
        "namespace": plan["namespace"],
        "agent_runtime_started": False,
        "orchestration_runtime_started": False,
        "workflow_runtime_started": False,
        "mcp_server_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "durable_store_created": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_stateful_orchestration()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
