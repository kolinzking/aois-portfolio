#!/usr/bin/env python3
"""Validate Phase 6 v19.5 AI failure governance plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("release-safety/aois-p/ai-failure-governance.plan.json")

REQUIRED_FAILURE_CLASSES = {
    "hallucinated_root_cause",
    "unsafe_remediation",
    "policy_boundary_violation",
    "missing_evidence",
    "secret_or_sensitive_data",
    "excessive_agency",
    "model_degradation",
}

REQUIRED_POLICY_CONTROLS = {
    "policy_version_required",
    "policy_owner_required",
    "structured_output_required",
    "schema_validation_required",
    "evidence_required_before_recommendation",
    "evidence_required_before_root_cause",
    "confidence_threshold_required",
    "human_review_for_low_confidence",
    "human_approval_for_destructive_action",
    "tool_allowlist_required",
    "tool_denylist_required",
    "namespace_boundary_required",
    "cost_budget_boundary_required",
    "data_classification_required",
    "secret_redaction_required",
    "provider_block_on_secret_required",
    "unsafe_output_block_required",
    "fallback_route_required",
    "audit_log_required",
    "post_failure_review_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
}

REQUIRED_SCOPE_CONTROLS = {
    "primary_aois_excluded",
    "aois_p_only",
    "local_tabletop_only",
    "no_live_user_impact",
    "no_secret_access",
    "no_destructive_action",
}

REQUIRED_DECISION_GATES = {"allow", "review", "block", "fallback"}

REQUIRED_LIVE_CHECKS = {
    "official_ai_risk_docs_review",
    "owasp_genai_security_review",
    "policy_owner_assigned",
    "policy_versioning_plan",
    "policy_test_set",
    "human_review_workflow",
    "tool_permission_inventory",
    "secret_redaction_test",
    "audit_log_storage_budget",
    "fallback_route_test",
    "incident_response_link",
    "rollback_plan",
    "primary_aois_separation_review",
    "resource_usage_record",
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


def validate_ai_failure_governance_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "ai_failure_governance_plan_no_runtime":
        missing.append("mode_must_be_ai_failure_governance_plan_no_runtime")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")

    for field in [
        "governance_runtime_started",
        "policy_engine_started",
        "agent_runtime_started",
        "tool_calls_executed",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "approved_for_live_governance_enforcement",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    _require_true_fields(plan.get("policy_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(
        plan.get("policy_controls"), REQUIRED_POLICY_CONTROLS, "policy_control", missing
    )

    decision_gates = plan.get("decision_gates", {})
    if not isinstance(decision_gates, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for gate in sorted(REQUIRED_DECISION_GATES):
            if gate not in decision_gates:
                missing.append(f"missing_decision_gate:{gate}")

    failure_classes = plan.get("failure_classes", [])
    if not isinstance(failure_classes, list):
        missing.append("failure_classes_must_be_list")
        failure_names: set[str] = set()
    else:
        failure_names = set()
        for item in failure_classes:
            if not isinstance(item, dict):
                missing.append("failure_class_entry_must_be_object")
                continue
            name = item.get("name")
            if isinstance(name, str):
                failure_names.add(name)
            for field in ["name", "description", "required_control", "default_decision"]:
                if not isinstance(item.get(field), str) or not item[field]:
                    missing.append(f"failure_class_missing_field:{field}:{name}")
    for name in sorted(REQUIRED_FAILURE_CLASSES):
        if name not in failure_names:
            missing.append(f"missing_failure_class:{name}")

    tool_policy = plan.get("tool_permission_policy", {})
    if not isinstance(tool_policy, dict):
        missing.append("tool_permission_policy_must_be_object")
    else:
        if tool_policy.get("default_tool_access") != "deny":
            missing.append("default_tool_access_must_be_deny")
        if tool_policy.get("primary_aois_tools_allowed") is not False:
            missing.append("primary_aois_tools_allowed_must_be_false")
        if tool_policy.get("tool_call_audit_required") is not True:
            missing.append("tool_call_audit_required_must_be_true")
        if not tool_policy.get("allowed_read_only_tools"):
            missing.append("allowed_read_only_tools_required")
        if not tool_policy.get("blocked_tools_without_human_approval"):
            missing.append("blocked_tools_without_human_approval_required")

    thresholds = plan.get("thresholds", {})
    if not isinstance(thresholds, dict):
        missing.append("thresholds_must_be_object")
    else:
        if thresholds.get("minimum_confidence_for_allow") != 0.75:
            missing.append("minimum_confidence_for_allow_must_be_0_75")
        if thresholds.get("minimum_policy_test_pass_rate") != 1.0:
            missing.append("minimum_policy_test_pass_rate_must_be_1_0")
        if thresholds.get("max_allowed_secret_findings") != 0:
            missing.append("max_allowed_secret_findings_must_be_zero")
        if thresholds.get("max_destructive_actions_without_approval") != 0:
            missing.append("max_destructive_actions_without_approval_must_be_zero")

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in [
            "max_governance_runtimes_for_lesson",
            "max_policy_engines_for_lesson",
            "max_agent_runs_for_lesson",
            "max_tool_calls_for_lesson",
            "max_provider_calls_for_lesson",
            "max_persistent_storage_mb",
            "max_spend_usd",
        ]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    cases = plan.get("evaluation_cases", [])
    if not isinstance(cases, list):
        missing.append("evaluation_cases_must_be_list")
    elif len(cases) < 5:
        missing.append("at_least_five_evaluation_cases_required")
    else:
        allowed_decisions = {"allow", "review", "block", "fallback_to_local_baseline"}
        for case in cases:
            if not isinstance(case, dict):
                missing.append("evaluation_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "name",
                "input",
                "evidence_present",
                "schema_valid",
                "model_quality_ok",
                "confidence",
                "secret_detected",
                "destructive_action_requested",
                "policy_boundary_passed",
                "expected_decision",
            ]:
                if field not in case:
                    missing.append(f"evaluation_case_missing_field:{field}:{name}")
            if case.get("expected_decision") not in allowed_decisions:
                missing.append(f"unexpected_case_decision:{name}")

    live_checks = set(plan.get("required_before_live_governance", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "ai_failure_governance_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "governance_runtime_started": False,
        "policy_engine_started": False,
        "agent_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_ai_failure_governance_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
