#!/usr/bin/env python3
"""Simulate Phase 7 v23.8 runtime autonomy control without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/runtime-autonomy-control.plan.json")


def _decide(case: dict[str, object], plan: dict[str, object]) -> dict[str, object]:
    policy = plan["gate_policy"]
    requested_mode = str(case["requested_mode"])
    current_mode = str(case["current_mode"])
    reasons: list[str] = []

    if case["kill_switch"] is True:
        decision = "disable_kill_switch"
        allowed_mode = "disabled"
        next_action = "disable_autonomy"
        stop_reason = "operator_kill_switch"
        reasons.append("operator_kill_switch_is_active")
    elif case["safety_status"] != policy["required_safety_status"]:
        decision = "emergency_stop_safety_event"
        allowed_mode = "disabled"
        next_action = "disable_autonomy"
        stop_reason = "safety_event"
        reasons.append("safety_status_is_not_clear")
    elif case["rollback_signal"] == "eval_regression" or case["eval_status"] != policy["required_eval_status"]:
        decision = "rollback_on_regression"
        allowed_mode = str(policy["rollback_mode"])
        next_action = "rollback_to_shadow"
        stop_reason = "evaluation_regression"
        reasons.append("evaluation_gate_failed")
    elif case["runtime_health"] != policy["required_runtime_health"]:
        decision = "demote_runtime_degraded"
        allowed_mode = "shadow"
        next_action = "demote_to_shadow"
        stop_reason = "runtime_degraded"
        reasons.append("runtime_health_gate_failed")
    elif case["observability_status"] != policy["required_observability_status"]:
        decision = "hold_observability_missing"
        allowed_mode = "shadow"
        next_action = "hold_shadow_mode"
        stop_reason = "observability_missing"
        reasons.append("observability_gate_failed")
    elif case["budget_status"] != policy["required_budget_status"]:
        decision = "pause_budget_exhausted"
        allowed_mode = "shadow"
        next_action = "pause_autonomy"
        stop_reason = "budget_guard"
        reasons.append("budget_guard_failed")
    elif requested_mode == "shadow":
        decision = "allow_shadow_mode"
        allowed_mode = "shadow"
        next_action = "enter_shadow_mode"
        stop_reason = "none"
        reasons.append("shadow_mode_allowed_without_operator_approval")
    elif requested_mode == "supervised" and case["operator_approval"] == "granted":
        decision = "allow_supervised_mode"
        allowed_mode = "supervised"
        next_action = "enter_supervised_mode"
        stop_reason = "none"
        reasons.append("supervised_mode_gate_passed_with_operator_approval")
    elif requested_mode == "limited_autonomous" and case["operator_approval"] != "granted":
        decision = "require_human_approval_for_limited"
        allowed_mode = current_mode if current_mode in {"shadow", "supervised"} else "shadow"
        next_action = "request_operator_approval"
        stop_reason = "approval_required"
        reasons.append("limited_autonomy_requires_operator_approval")
    elif requested_mode == "limited_autonomous" and case["operator_approval"] == "granted":
        decision = "allow_limited_autonomy"
        allowed_mode = "limited_autonomous"
        next_action = "enter_limited_autonomy"
        stop_reason = "none"
        reasons.append("all_gates_passed_for_limited_autonomy")
    else:
        decision = "allow_shadow_mode"
        allowed_mode = "shadow"
        next_action = "enter_shadow_mode"
        stop_reason = "none"
        reasons.append("unhandled_mode_defaults_to_shadow")

    expected_decision = str(case["expected_decision"])
    expected_allowed_mode = str(case["expected_allowed_mode"])
    expected_next_action = str(case["expected_next_action"])
    expected_stop_reason = str(case["expected_stop_reason"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "requested_mode": requested_mode,
        "current_mode": current_mode,
        "decision": decision,
        "allowed_mode": allowed_mode,
        "next_action": next_action,
        "stop_reason": stop_reason,
        "expected_decision": expected_decision,
        "expected_allowed_mode": expected_allowed_mode,
        "expected_next_action": expected_next_action,
        "expected_stop_reason": expected_stop_reason,
        "passed": (
            decision == expected_decision
            and allowed_mode == expected_allowed_mode
            and next_action == expected_next_action
            and stop_reason == expected_stop_reason
        ),
        "reasons": reasons,
    }


def simulate_runtime_autonomy_control() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case, plan) for case in plan["autonomy_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "runtime_autonomy_control_simulation_no_runtime",
        "namespace": plan["namespace"],
        "agent_runtime_started": False,
        "autonomy_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_runtime_autonomy_control()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
