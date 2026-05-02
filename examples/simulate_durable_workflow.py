#!/usr/bin/env python3
"""Simulate Phase 7 v22 durable workflow decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/durable-workflow.plan.json")

BLOCKING_REGISTRY_DECISIONS = {
    "block_unregistered_tool",
    "block_untrusted_server",
    "block_side_effecting_tool",
    "block_disabled_tool",
}


def _decide(case: dict[str, object]) -> dict[str, object]:
    reasons: list[str] = []
    registry_decision = str(case["registry_decision"])
    approval_status = str(case["approval_status"])
    elapsed = float(case["elapsed_seconds"])
    timeout = float(case["timeout_seconds"])
    retry_count = int(case["retry_count"])
    max_retries = int(case["max_retries"])

    if elapsed > timeout:
        decision = "fail_timeout"
        state = "timed_out"
        terminal_status = "timed_out"
        recovery_action = "operator_review_timeout"
        reasons.append("step_timeout_exceeded")
    elif case["idempotency_key_seen"] is True:
        decision = "skip_duplicate_step"
        state = "completed"
        terminal_status = "completed"
        recovery_action = "reuse_existing_checkpoint"
        reasons.append("idempotency_key_already_checkpointed")
    elif registry_decision in BLOCKING_REGISTRY_DECISIONS:
        decision = "block_registry_denial"
        state = "blocked"
        terminal_status = "blocked"
        recovery_action = "registry_review_required"
        reasons.append(f"registry_denied_tool_exposure:{registry_decision}")
    elif registry_decision == "require_human_approval" and approval_status == "required_missing":
        decision = "pause_for_human_approval"
        state = "waiting_for_approval"
        terminal_status = "non_terminal"
        recovery_action = "wait_for_operator_approval"
        reasons.append("approval_checkpoint_waiting")
    elif registry_decision == "require_human_approval" and approval_status == "granted":
        decision = "resume_after_approval"
        state = "completed"
        terminal_status = "completed"
        recovery_action = "resume_from_approval_checkpoint"
        reasons.append("approval_checkpoint_granted")
    elif retry_count > 0 and retry_count <= max_retries:
        decision = "recover_after_retry"
        state = "completed"
        terminal_status = "completed"
        recovery_action = "retry_then_checkpoint"
        reasons.append("retry_budget_available")
    elif registry_decision == "allow_no_tool_route":
        decision = "complete_no_tool_workflow"
        state = "completed"
        terminal_status = "completed"
        recovery_action = "none"
        reasons.append("no_tools_requested")
    else:
        decision = "complete_read_only_workflow_plan"
        state = "completed"
        terminal_status = "completed"
        recovery_action = "none"
        reasons.append("read_only_tool_plan_recorded")

    expected_decision = str(case["expected_decision"])
    expected_state = str(case["expected_state"])
    expected_terminal_status = str(case["expected_terminal_status"])
    expected_recovery_action = str(case["expected_recovery_action"])

    return {
        "case": case["name"],
        "workflow_id": case["workflow_id"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "route_decision": case["route_decision"],
        "registry_decision": registry_decision,
        "approval_status": approval_status,
        "requested_tools": case["requested_tools"],
        "blocked_tools": case["blocked_tools"],
        "current_step": case["current_step"],
        "decision": decision,
        "state": state,
        "terminal_status": terminal_status,
        "recovery_action": recovery_action,
        "expected_decision": expected_decision,
        "expected_state": expected_state,
        "expected_terminal_status": expected_terminal_status,
        "expected_recovery_action": expected_recovery_action,
        "passed": (
            decision == expected_decision
            and state == expected_state
            and terminal_status == expected_terminal_status
            and recovery_action == expected_recovery_action
        ),
        "reasons": reasons,
    }


def simulate_durable_workflow() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case) for case in plan["workflow_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "durable_workflow_simulation_no_runtime",
        "namespace": plan["namespace"],
        "agent_runtime_started": False,
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
    result = simulate_durable_workflow()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
