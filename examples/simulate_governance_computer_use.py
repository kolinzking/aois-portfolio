#!/usr/bin/env python3
"""Simulate Phase 10 v34 governance computer-use decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PLAN_PATH = Path("frontier/aois-p/governance-computer-use.plan.json")

SENSITIVE_CLASSES = {"sensitive", "secret", "regulated"}
LIVE_TARGETS = {"live_production", "external", "authenticated", "real_user"}


def _expand_case(defaults: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    expanded = dict(defaults)
    expanded.update(case.get("overrides", {}))
    expanded["case_id"] = case["case_id"]
    expanded["name"] = case["name"]
    return expanded


def _decision(case: dict[str, Any]) -> tuple[str, str, str, str]:
    if case["governance_status"] != "pass" or case["user_intent_status"] != "clear":
        return (
            "block_missing_governance_policy",
            "define_governance_policy",
            "blocked",
            "governance_policy_or_action_intent_missing",
        )
    if case["environment_type"] != "local_synthetic":
        return (
            "block_out_of_scope_environment",
            "move_to_local_synthetic_environment",
            "blocked",
            "environment_not_allowlisted_for_curriculum",
        )
    if case["target_status"] in LIVE_TARGETS or case["target_status"] != "synthetic_allowlisted":
        return (
            "block_live_target",
            "replace_with_synthetic_target",
            "blocked",
            "live_external_or_authenticated_target_requested",
        )
    if case["credential_status"] != "none":
        return (
            "block_credential_request",
            "remove_credential_requirement",
            "blocked",
            "credential_or_secret_handling_requested",
        )
    if (
        case["data_classification"] in SENSITIVE_CLASSES
        and case["privacy_status"] != "redacted"
    ):
        return (
            "block_sensitive_data_unredacted",
            "redact_screen_and_action_data",
            "blocked",
            "sensitive_screen_or_action_data_unredacted",
        )
    if case["action_type"] == "high_impact_action" or case["action_risk"] == "high":
        return (
            "block_high_impact_action",
            "prohibit_automated_high_impact_action",
            "blocked",
            "high_impact_or_irreversible_action_requested",
        )
    if case["action_type"] == "external_transaction":
        return (
            "block_external_transaction",
            "remove_external_transaction",
            "blocked",
            "external_transaction_or_commitment_requested",
        )
    if case["safety_check_status"] == "pending":
        return (
            "hold_pending_safety_check",
            "review_and_acknowledge_safety_check",
            "held",
            "computer_use_safety_check_pending",
        )
    if case["approval_status"] == "missing":
        return (
            "hold_pending_human_approval",
            "request_human_approval",
            "held",
            "required_human_approval_missing",
        )
    if case["approval_status"] == "manual_required":
        return (
            "route_to_manual_operator",
            "handoff_to_manual_operator",
            "manual",
            "governance_requires_manual_operation",
        )
    if case["step_preview_status"] != "present":
        return (
            "hold_missing_step_preview",
            "render_step_preview",
            "held",
            "operator_step_preview_missing",
        )
    if case["action_budget_status"] != "pass" or case["rate_limit_status"] != "pass":
        return (
            "block_action_budget_exceeded",
            "reduce_action_budget_or_stop",
            "blocked",
            "action_budget_or_rate_limit_exceeded",
        )
    if case["stop_control_status"] != "ready":
        return (
            "block_missing_stop_control",
            "add_operator_stop_control",
            "blocked",
            "operator_stop_control_missing",
        )
    if case["rollback_status"] not in {"ready", "not_required"}:
        return (
            "block_missing_rollback",
            "define_rollback_plan",
            "blocked",
            "rollback_plan_missing",
        )
    if (
        case["audit_trace_status"] != "captured"
        or case["screen_evidence_status"] != "redacted"
        or case["operator_watch_status"] != "active"
    ):
        return (
            "hold_missing_audit_trace",
            "instrument_audit_trace",
            "held",
            "audit_screen_or_operator_watch_evidence_missing",
        )
    if case["red_team_status"] != "cleared":
        return (
            "block_unresolved_red_team_finding",
            "resolve_v33_red_team_finding",
            "blocked",
            "red_team_finding_not_cleared",
        )
    if case["release_gate_status"] != "pass":
        return (
            "block_release_gate",
            "repair_computer_use_release_gate",
            "blocked",
            "release_gate_failed",
        )
    if case["access_policy_status"] != "pass":
        return (
            "block_policy_boundary",
            "repair_computer_use_policy_boundary",
            "blocked",
            "access_tenancy_or_policy_boundary_failed",
        )

    if case["action_type"] == "observe_only":
        return (
            "allow_observe_only_governed_record",
            "record_observe_only_governance_evidence",
            "recorded",
            "observe_only_governance_controls_passed",
        )
    if case["action_type"] == "draft_action_plan":
        return (
            "allow_draft_action_plan_only",
            "record_draft_for_operator_review",
            "drafted",
            "draft_only_controls_passed",
        )
    return (
        "allow_synthetic_computer_use_plan_recorded",
        "record_synthetic_computer_use_plan",
        "recorded",
        "synthetic_computer_use_governance_controls_passed",
    )


def _decide(defaults: dict[str, Any], raw_case: dict[str, Any]) -> dict[str, Any]:
    case = _expand_case(defaults, raw_case)
    decision, operator_action, computer_use_state, reason = _decision(case)
    expected_decision = str(raw_case["expected_decision"])
    expected_operator_action = str(raw_case["expected_operator_action"])
    expected_computer_use_state = str(raw_case["expected_computer_use_state"])

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "incident_id": case["incident_id"],
        "trace_id": case["trace_id"],
        "action_id": case["action_id"],
        "action_type": case["action_type"],
        "action_risk": case["action_risk"],
        "environment_type": case["environment_type"],
        "target_status": case["target_status"],
        "decision": decision,
        "operator_action": operator_action,
        "computer_use_state": computer_use_state,
        "expected_decision": expected_decision,
        "expected_operator_action": expected_operator_action,
        "expected_computer_use_state": expected_computer_use_state,
        "passed": (
            decision == expected_decision
            and operator_action == expected_operator_action
            and computer_use_state == expected_computer_use_state
        ),
        "reasons": [reason],
    }


def simulate_governance_computer_use() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    defaults = plan["case_defaults"]
    decisions = [_decide(defaults, case) for case in plan["computer_use_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "governance_computer_use_simulation_no_runtime",
        "namespace": plan["namespace"],
        "computer_use_started": False,
        "live_browser_started": False,
        "live_vm_started": False,
        "screenshot_captured": False,
        "mouse_clicked": False,
        "keyboard_typed": False,
        "clipboard_accessed": False,
        "file_uploaded": False,
        "file_downloaded": False,
        "network_call_made": False,
        "provider_call_made": False,
        "tool_call_made": False,
        "command_executed": False,
        "shell_started": False,
        "credential_accessed": False,
        "payment_submitted": False,
        "form_submitted": False,
        "external_action_performed": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_governance_computer_use()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
