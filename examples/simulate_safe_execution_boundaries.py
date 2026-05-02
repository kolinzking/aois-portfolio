#!/usr/bin/env python3
"""Simulate Phase 7 v25 safe execution boundary decisions without execution."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/safe-execution-boundaries.plan.json")

APPROVAL_REQUIRED_CATEGORIES = {
    "sensitive_read",
    "mutating",
    "external_side_effect",
    "shell",
    "code_execution",
    "network_egress",
}

SANDBOX_REQUIRED_CATEGORIES = {
    "mutating",
    "external_side_effect",
    "shell",
    "code_execution",
    "network_egress",
}

ROLLBACK_REQUIRED_CATEGORIES = {
    "mutating",
    "external_side_effect",
}

DRY_RUN_REQUIRED_CATEGORIES = {
    "read_only",
    "sensitive_read",
    "mutating",
    "external_side_effect",
    "shell",
    "code_execution",
    "network_egress",
}


def _decide(case: dict[str, object]) -> dict[str, object]:
    category = str(case["action_category"])
    reasons: list[str] = []

    if category == "forbidden":
        decision = "block_forbidden_action"
        execution_mode = "blocked"
        next_action = "deny_action"
        reasons.append("forbidden_category_denied_first")
    elif case["autonomy_mode"] == "disabled":
        decision = "block_autonomy_disabled"
        execution_mode = "blocked"
        next_action = "deny_action"
        reasons.append("autonomy_disabled_blocks_execution_boundary")
    elif case["registry_decision"] != "allowed":
        decision = "block_registry_denied"
        execution_mode = "blocked"
        next_action = "deny_action"
        reasons.append("tool_registry_did_not_allow_action")
    elif case["credential_scope"] in {"broad", "unknown", "unscoped"}:
        decision = "block_credential_scope"
        execution_mode = "blocked"
        next_action = "deny_action"
        reasons.append("credential_scope_not_bounded")
    elif category in {"network_egress", "external_side_effect"} and case["network_policy"] != "approved_egress":
        decision = "block_network_egress"
        execution_mode = "blocked"
        next_action = "deny_action"
        reasons.append("network_egress_not_explicitly_approved")
    elif case["guardrail_status"] == "tripwire":
        decision = "block_guardrail_tripwire"
        execution_mode = "blocked"
        next_action = "deny_action"
        reasons.append("guardrail_tripwire_triggered")
    elif case["output_validation_status"] != "pass":
        decision = "block_output_validation_failure"
        execution_mode = "blocked"
        next_action = "deny_action"
        reasons.append("output_validation_failed")
    elif category in SANDBOX_REQUIRED_CATEGORIES and case["sandbox_status"] != "isolated":
        decision = "require_execution_sandbox"
        execution_mode = "blocked_pending_boundary"
        next_action = "configure_isolated_sandbox"
        reasons.append("execution_capable_action_requires_sandbox")
    elif category == "sensitive_read" and case["approval_status"] != "granted":
        decision = "require_sensitive_read_approval"
        execution_mode = "approval_wait"
        next_action = "request_human_approval"
        reasons.append("sensitive_read_requires_approval")
    elif category in APPROVAL_REQUIRED_CATEGORIES and case["approval_status"] != "granted":
        decision = "require_mutation_approval"
        execution_mode = "approval_wait"
        next_action = "request_human_approval"
        reasons.append("execution_capable_action_requires_approval")
    elif category in ROLLBACK_REQUIRED_CATEGORIES and case["rollback_status"] != "available":
        decision = "block_missing_rollback"
        execution_mode = "blocked"
        next_action = "deny_action"
        reasons.append("rollback_required_before_mutation")
    elif category in DRY_RUN_REQUIRED_CATEGORIES and case["dry_run_available"] is not True:
        decision = "block_missing_dry_run"
        execution_mode = "blocked"
        next_action = "deny_action"
        reasons.append("dry_run_required_before_execution")
    elif category == "plan_only":
        decision = "record_plan_only"
        execution_mode = "plan_only"
        next_action = "record_policy_decision"
        reasons.append("plan_only_action_never_executes")
    elif category == "read_only":
        decision = "allow_read_only_dry_run"
        execution_mode = "dry_run_only"
        next_action = "prepare_read_only_invocation"
        reasons.append("read_only_action_staged_as_dry_run")
    else:
        decision = "allow_approved_bounded_dry_run"
        execution_mode = "dry_run_only"
        next_action = "stage_bounded_execution_plan"
        reasons.append("approved_bounded_action_staged_without_execution")

    expected_decision = str(case["expected_decision"])
    expected_execution_mode = str(case["expected_execution_mode"])
    expected_next_action = str(case["expected_next_action"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "actor_role": case["actor_role"],
        "requested_action": case["requested_action"],
        "action_category": category,
        "decision": decision,
        "execution_mode": execution_mode,
        "next_action": next_action,
        "expected_decision": expected_decision,
        "expected_execution_mode": expected_execution_mode,
        "expected_next_action": expected_next_action,
        "passed": (
            decision == expected_decision
            and execution_mode == expected_execution_mode
            and next_action == expected_next_action
        ),
        "reasons": reasons,
    }


def simulate_safe_execution_boundaries() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case) for case in plan["boundary_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "safe_execution_boundaries_simulation_no_runtime",
        "namespace": plan["namespace"],
        "agent_runtime_started": False,
        "execution_runtime_started": False,
        "sandbox_started": False,
        "tool_calls_executed": False,
        "command_executed": False,
        "file_write_performed": False,
        "network_call_made": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_safe_execution_boundaries()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
