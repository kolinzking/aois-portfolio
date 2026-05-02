#!/usr/bin/env python3
"""Validate Phase 10 v34 governance computer-use plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("frontier/aois-p/governance-computer-use.plan.json")

REQUIRED_FALSE_FLAGS = {
    "computer_use_started",
    "live_browser_started",
    "live_vm_started",
    "screenshot_captured",
    "mouse_clicked",
    "keyboard_typed",
    "clipboard_accessed",
    "file_uploaded",
    "file_downloaded",
    "network_call_made",
    "provider_call_made",
    "tool_call_made",
    "command_executed",
    "shell_started",
    "credential_accessed",
    "payment_submitted",
    "form_submitted",
    "external_action_performed",
    "external_network_required_for_this_lesson",
    "persistent_storage_created",
    "approved_for_live_computer_use",
}

REQUIRED_SCOPE = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v31_multimodal_contract",
    "uses_v32_edge_offline_contract",
    "uses_v33_red_team_contract",
    "uses_phase9_release_controls",
    "local_simulation_only",
    "governance_verification_only",
    "no_live_computer",
    "no_live_browser",
    "no_live_vm",
    "no_screenshot_capture",
    "no_mouse_or_keyboard",
    "no_clipboard",
    "no_credentials",
    "no_file_transfer",
    "no_external_network",
    "no_provider_call",
    "no_tool_execution",
    "no_transaction",
}

REQUIRED_CONTROLS = {
    "governance_policy_required",
    "action_intent_required",
    "action_classification_required",
    "environment_allowlist_required",
    "target_allowlist_required",
    "human_approval_required",
    "manual_handoff_required",
    "high_impact_action_block_required",
    "external_transaction_block_required",
    "credential_boundary_required",
    "data_classification_required",
    "privacy_redaction_required",
    "safety_check_required",
    "pending_safety_ack_required",
    "step_preview_required",
    "action_budget_required",
    "stop_control_required",
    "rollback_plan_required",
    "audit_trace_required",
    "screen_evidence_redaction_required",
    "operator_watch_required",
    "rate_limit_required",
    "red_team_clearance_required",
    "release_gate_required",
    "access_policy_required",
    "primary_aois_separation_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "incident_id",
    "trace_id",
    "action_id",
    "action_type",
    "action_risk",
    "environment_type",
    "target_status",
    "user_intent_status",
    "governance_status",
    "approval_status",
    "safety_check_status",
    "data_classification",
    "credential_status",
    "privacy_status",
    "step_preview_status",
    "action_budget_status",
    "stop_control_status",
    "rollback_status",
    "audit_trace_status",
    "screen_evidence_status",
    "operator_watch_status",
    "rate_limit_status",
    "red_team_status",
    "release_gate_status",
    "access_policy_status",
    "computer_use_decision",
    "operator_action",
}

REQUIRED_ACTION_TYPES = {
    "observe_only",
    "draft_action_plan",
    "navigate_synthetic",
    "enter_synthetic_text",
    "submit_synthetic_form",
    "external_transaction",
    "credential_handling",
    "high_impact_action",
}

REQUIRED_DECISIONS = {
    "allow_observe_only_governed_record",
    "allow_draft_action_plan_only",
    "allow_synthetic_computer_use_plan_recorded",
    "route_to_manual_operator",
    "block_missing_governance_policy",
    "block_out_of_scope_environment",
    "block_live_target",
    "hold_pending_human_approval",
    "block_credential_request",
    "block_sensitive_data_unredacted",
    "block_high_impact_action",
    "block_external_transaction",
    "hold_pending_safety_check",
    "hold_missing_step_preview",
    "block_action_budget_exceeded",
    "block_missing_stop_control",
    "block_missing_rollback",
    "hold_missing_audit_trace",
    "block_unresolved_red_team_finding",
    "block_release_gate",
    "block_policy_boundary",
}

REQUIRED_SOURCES = {
    "https://developers.openai.com/api/docs/guides/tools-computer-use",
    "https://developers.openai.com/api/docs/guides/safety-checks",
    "https://developers.openai.com/api/docs/guides/safety-best-practices",
    "https://genai.owasp.org/initiatives/agentic-security-initiative/",
    "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence",
    "https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook",
    "https://opentelemetry.io/docs/concepts/signals/",
}

REQUIRED_LIVE_CHECKS = {
    "governance_policy_review",
    "action_intent_review",
    "action_classification_review",
    "environment_allowlist_review",
    "target_allowlist_review",
    "human_approval_review",
    "manual_handoff_review",
    "high_impact_action_review",
    "external_transaction_review",
    "credential_boundary_review",
    "data_classification_review",
    "privacy_redaction_review",
    "safety_check_review",
    "pending_safety_ack_review",
    "step_preview_review",
    "action_budget_review",
    "stop_control_review",
    "rollback_plan_review",
    "audit_trace_review",
    "screen_evidence_redaction_review",
    "operator_watch_review",
    "rate_limit_review",
    "red_team_clearance_review",
    "release_gate_review",
    "access_policy_review",
    "primary_aois_separation_review",
    "resource_usage_record",
}

REQUIRED_DEFAULTS = {
    "action_type": "navigate_synthetic",
    "action_risk": "low",
    "environment_type": "local_synthetic",
    "target_status": "synthetic_allowlisted",
    "user_intent_status": "clear",
    "governance_status": "pass",
    "approval_status": "approved",
    "safety_check_status": "clear",
    "data_classification": "internal",
    "credential_status": "none",
    "privacy_status": "redacted",
    "step_preview_status": "present",
    "action_budget_status": "pass",
    "stop_control_status": "ready",
    "rollback_status": "ready",
    "audit_trace_status": "captured",
    "screen_evidence_status": "redacted",
    "operator_watch_status": "active",
    "rate_limit_status": "pass",
    "red_team_status": "cleared",
    "release_gate_status": "pass",
    "access_policy_status": "pass",
}


def _require_true_fields(
    section: object, required: set[str], label: str, missing: list[str]
) -> None:
    if not isinstance(section, dict):
        missing.append(f"{label}_must_be_object")
        return
    for field in sorted(required):
        if section.get(field) is not True:
            missing.append(f"missing_{label}:{field}")


def _require_false_flags(plan: dict[str, object], missing: list[str]) -> None:
    for field in sorted(REQUIRED_FALSE_FLAGS):
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")


def _require_source_notes(source_notes: object, missing: list[str]) -> None:
    if not isinstance(source_notes, list) or len(source_notes) < len(REQUIRED_SOURCES):
        missing.append("complete_source_notes_required")
        return

    urls = set()
    for note in source_notes:
        if not isinstance(note, dict):
            missing.append("source_note_must_be_object")
            continue
        for field in ["source", "url", "date_checked", "supports"]:
            if not note.get(field):
                missing.append(f"source_note_missing_field:{field}")
        if isinstance(note.get("url"), str):
            urls.add(str(note["url"]))
        if note.get("date_checked") != "2026-05-01":
            missing.append(f"source_note_date_must_be_2026_05_01:{note.get('source')}")

    for url in sorted(REQUIRED_SOURCES):
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_action_catalog(plan: dict[str, object], missing: list[str]) -> None:
    actions = plan.get("action_catalog", [])
    observed: set[str] = set()
    if not isinstance(actions, list) or len(actions) < len(REQUIRED_ACTION_TYPES):
        missing.append("complete_action_catalog_required")
        return
    for action in actions:
        if not isinstance(action, dict):
            missing.append("action_catalog_entry_must_be_object")
            continue
        action_type = action.get("action_type")
        if isinstance(action_type, str):
            observed.add(action_type)
        for field in [
            "action_type",
            "allowed_environment_types",
            "requires_human_approval",
            "requires_rollback",
            "default_decision",
            "primary_risks",
        ]:
            if field not in action:
                missing.append(f"action_missing_field:{action_type}:{field}")
        if not isinstance(action.get("allowed_environment_types"), list):
            missing.append(f"action_allowed_environments_must_be_list:{action_type}")
        if not isinstance(action.get("primary_risks"), list) or not action["primary_risks"]:
            missing.append(f"action_primary_risks_required:{action_type}")

    for action_type in sorted(REQUIRED_ACTION_TYPES):
        if action_type not in observed:
            missing.append(f"missing_action_type:{action_type}")


def _require_defaults(defaults: object, missing: list[str]) -> None:
    if not isinstance(defaults, dict):
        missing.append("case_defaults_must_be_object")
        return
    for field, expected in REQUIRED_DEFAULTS.items():
        if defaults.get(field) != expected:
            missing.append(f"case_default_mismatch:{field}")
    for field in ["incident_id", "trace_id", "action_id"]:
        if field not in defaults:
            missing.append(f"case_default_required:{field}")


def _require_cases(plan: dict[str, object], missing: list[str]) -> None:
    cases = plan.get("computer_use_cases", [])
    observed_decisions: set[str] = set()
    required_case_fields = {
        "case_id",
        "name",
        "expected_decision",
        "expected_operator_action",
        "expected_computer_use_state",
    }
    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("computer_use_case_for_each_decision_required")
        return

    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            missing.append("computer_use_case_must_be_object")
            continue
        case_id = str(case.get("case_id", ""))
        if not case_id:
            missing.append("computer_use_case_id_required")
        elif case_id in case_ids:
            missing.append(f"duplicate_computer_use_case_id:{case_id}")
        case_ids.add(case_id)

        for field in sorted(required_case_fields):
            if field not in case:
                missing.append(f"computer_use_case_missing_field:{case_id}:{field}")
        decision = case.get("expected_decision")
        if isinstance(decision, str):
            observed_decisions.add(decision)
        if decision not in REQUIRED_DECISIONS:
            missing.append(f"unexpected_expected_decision:{case_id}:{decision}")
        if "overrides" in case and not isinstance(case["overrides"], dict):
            missing.append(f"computer_use_case_overrides_must_be_object:{case_id}")

    for decision in sorted(REQUIRED_DECISIONS):
        if decision not in observed_decisions:
            missing.append(f"missing_computer_use_case_for_decision:{decision}")


def validate_governance_computer_use_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "governance_computer_use_plan_no_runtime":
        missing.append("mode_must_be_governance_computer_use_plan_no_runtime")
    if plan.get("version") != "v34":
        missing.append("version_must_be_v34")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("computer_use_scope"), REQUIRED_SCOPE, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("computer_use_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_computer_use_dimension:{dimension}")

    decision_gates = plan.get("decision_gates", {})
    if not isinstance(decision_gates, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if not decision_gates.get(decision):
                missing.append(f"missing_decision_gate:{decision}")

    _require_action_catalog(plan, missing)
    _require_defaults(plan.get("case_defaults"), missing)
    _require_cases(plan, missing)

    live_checks = set(plan.get("required_before_live_computer_use", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_computer_use_check:{check}")

    return {
        "plan": str(PLAN_PATH),
        "mode": plan.get("mode"),
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_governance_computer_use_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
