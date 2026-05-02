#!/usr/bin/env python3
"""Validate Phase 7 v25 safe execution boundaries without execution."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/safe-execution-boundaries.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v20_tool_plan",
    "uses_v21_registry_decision",
    "uses_v22_workflow_state",
    "uses_v23_orchestration_state",
    "uses_v23_8_autonomy_mode",
    "uses_v24_role_policy",
    "plan_only_execution_policy",
    "deny_by_default",
    "action_classification_required",
    "approval_required_for_sensitive_and_mutating",
    "sandbox_required_for_execution",
    "network_egress_policy_required",
    "filesystem_scope_required",
    "secret_redaction_required",
    "idempotency_required",
    "rollback_required",
    "observability_required",
    "local_simulation_only",
    "no_live_execution_runtime",
    "no_tool_execution",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "action_catalog_required",
    "risk_tier_required",
    "default_deny_required",
    "human_approval_required",
    "sandbox_required",
    "network_policy_required",
    "filesystem_policy_required",
    "credential_boundary_required",
    "guardrail_order_required",
    "registry_binding_required",
    "role_binding_required",
    "autonomy_mode_gate_required",
    "approval_expiry_required",
    "audit_event_required",
    "trace_id_required",
    "dry_run_required",
    "rollback_plan_required",
    "output_validation_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "incident_id",
    "trace_id",
    "actor_role",
    "requested_action",
    "action_category",
    "risk_tier",
    "registry_decision",
    "autonomy_mode",
    "approval_status",
    "sandbox_status",
    "filesystem_scope",
    "network_policy",
    "credential_scope",
    "guardrail_status",
    "idempotency_status",
    "rollback_status",
    "dry_run_available",
    "output_validation_status",
    "decision",
    "execution_mode",
    "next_action",
    "audit_event",
}

REQUIRED_CATEGORIES = {
    "plan_only",
    "read_only",
    "sensitive_read",
    "mutating",
    "external_side_effect",
    "shell",
    "code_execution",
    "network_egress",
    "forbidden",
}

REQUIRED_DECISIONS = {
    "record_plan_only",
    "allow_read_only_dry_run",
    "require_sensitive_read_approval",
    "require_mutation_approval",
    "require_execution_sandbox",
    "block_forbidden_action",
    "block_registry_denied",
    "block_autonomy_disabled",
    "block_network_egress",
    "block_credential_scope",
    "block_guardrail_tripwire",
    "block_output_validation_failure",
    "block_missing_rollback",
    "block_missing_dry_run",
    "allow_approved_bounded_dry_run",
}

REQUIRED_GUARDRAIL_ORDER = [
    "deny_forbidden_category",
    "deny_disabled_autonomy",
    "deny_registry_denied",
    "deny_broad_credentials",
    "deny_unapproved_network_egress",
    "deny_guardrail_tripwire",
    "deny_output_validation_failure",
    "require_execution_sandbox",
    "require_human_approval",
    "require_rollback",
    "require_dry_run",
    "record_or_allow_dry_run",
]

REQUIRED_LIVE_CHECKS = {
    "official_framework_review",
    "agentic_threat_model_review",
    "tool_registry_binding_review",
    "permission_boundary_review",
    "human_approval_flow_test",
    "sandbox_escape_review",
    "network_egress_review",
    "secret_handling_review",
    "dry_run_and_idempotency_test",
    "rollback_drill",
    "output_validation_review",
    "audit_log_sink",
    "incident_response_runbook",
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


def _require_false_flags(plan: dict[str, object], missing: list[str]) -> None:
    for field in [
        "agent_runtime_started",
        "execution_runtime_started",
        "multi_agent_runtime_started",
        "autonomy_runtime_started",
        "orchestration_runtime_started",
        "workflow_runtime_started",
        "mcp_server_started",
        "sandbox_started",
        "tool_calls_executed",
        "command_executed",
        "file_write_performed",
        "network_call_made",
        "provider_call_made",
        "cloud_resource_touched",
        "external_network_required_for_this_lesson",
        "durable_store_created",
        "persistent_storage_created",
        "approved_for_live_execution",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")


def _require_source_notes(source_notes: object, missing: list[str]) -> None:
    if not isinstance(source_notes, list) or len(source_notes) < 4:
        missing.append("at_least_four_source_notes_required")
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
        if note.get("date_checked") != "2026-04-30":
            missing.append(f"source_note_date_must_be_2026_04_30:{note.get('source')}")
    for url in [
        "https://openai.github.io/openai-agents-python/guardrails/",
        "https://openai.github.io/openai-agents-python/human_in_the_loop/",
        "https://openai.github.io/openai-agents-python/ref/sandbox/permissions/",
        "https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/",
    ]:
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_boolean(value: object, label: str, missing: list[str]) -> None:
    if not isinstance(value, bool):
        missing.append(f"{label}_must_be_boolean")


def validate_safe_execution_boundaries_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "safe_execution_boundaries_plan_no_runtime":
        missing.append("mode_must_be_safe_execution_boundaries_plan_no_runtime")
    if plan.get("version") != "v25":
        missing.append("version_must_be_v25")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("execution_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("execution_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_execution_dimension:{dimension}")

    catalog = plan.get("action_boundary_catalog", [])
    observed_categories: set[str] = set()
    category_defaults: dict[str, str] = {}
    if not isinstance(catalog, list) or len(catalog) < len(REQUIRED_CATEGORIES):
        missing.append("complete_action_boundary_catalog_required")
    else:
        for item in catalog:
            if not isinstance(item, dict):
                missing.append("action_boundary_catalog_item_must_be_object")
                continue
            category = item.get("category")
            if isinstance(category, str):
                observed_categories.add(category)
                category_defaults[category] = str(item.get("default_decision"))
            for field in [
                "category",
                "risk_tier",
                "default_decision",
                "requires_approval",
                "requires_sandbox",
                "allows_network",
                "allows_filesystem_write",
                "requires_rollback",
                "requires_dry_run",
                "live_execution_allowed",
            ]:
                if field not in item:
                    missing.append(f"catalog_missing_field:{field}:{category}")
            for field in [
                "requires_approval",
                "requires_sandbox",
                "allows_network",
                "allows_filesystem_write",
                "requires_rollback",
                "requires_dry_run",
            ]:
                _require_boolean(item.get(field), f"catalog_{field}:{category}", missing)
            if item.get("live_execution_allowed") is not False:
                missing.append(f"catalog_live_execution_allowed_must_be_false:{category}")
        for category in sorted(REQUIRED_CATEGORIES):
            if category not in observed_categories:
                missing.append(f"missing_action_category:{category}")
        if category_defaults.get("forbidden") != "block_forbidden_action":
            missing.append("forbidden_category_must_default_to_block")

    guardrail_order = plan.get("guardrail_order", [])
    if not isinstance(guardrail_order, list):
        missing.append("guardrail_order_must_be_list")
    else:
        for item in REQUIRED_GUARDRAIL_ORDER:
            if item not in guardrail_order:
                missing.append(f"missing_guardrail_order_item:{item}")

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    cases = plan.get("boundary_cases", [])
    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("at_least_one_case_per_decision_required")
    else:
        observed_decisions = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("boundary_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "case_id",
                "name",
                "incident_id",
                "trace_id",
                "actor_role",
                "requested_action",
                "action_category",
                "risk_tier",
                "registry_decision",
                "autonomy_mode",
                "approval_status",
                "sandbox_status",
                "filesystem_scope",
                "network_policy",
                "credential_scope",
                "guardrail_status",
                "idempotency_status",
                "rollback_status",
                "dry_run_available",
                "output_validation_status",
                "expected_decision",
                "expected_execution_mode",
                "expected_next_action",
            ]:
                if field not in case:
                    missing.append(f"boundary_case_missing_field:{field}:{name}")
            if case.get("action_category") not in REQUIRED_CATEGORIES:
                missing.append(f"unknown_action_category:{name}:{case.get('action_category')}")
            if not isinstance(case.get("dry_run_available"), bool):
                missing.append(f"dry_run_available_must_be_boolean:{name}")
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_expected_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_execution", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "safe_execution_boundaries_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "execution_runtime_started": False,
        "tool_calls_executed": False,
        "command_executed": False,
        "provider_call_made": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_safe_execution_boundaries_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
