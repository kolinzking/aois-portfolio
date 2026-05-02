#!/usr/bin/env python3
"""Validate Phase 8 v27 policy-aware access plan without auth runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("product/aois-p/policy-aware-access.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v26_dashboard_panels",
    "identity_required",
    "tenant_required",
    "role_required",
    "policy_decision_required",
    "deny_by_default",
    "least_privilege_required",
    "approval_action_separation_required",
    "budget_visibility_scoped",
    "trace_visibility_scoped",
    "execution_boundary_visibility_scoped",
    "redaction_required",
    "audit_event_required",
    "local_simulation_only",
    "no_live_identity_provider",
    "no_live_session",
    "no_policy_engine_runtime",
    "no_frontend_runtime",
    "no_network_call",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "subject_id_required",
    "tenant_id_required",
    "role_catalog_required",
    "resource_catalog_required",
    "permission_matrix_required",
    "ownership_check_required",
    "tenant_boundary_required",
    "break_glass_policy_required",
    "approval_separation_required",
    "deny_unknown_role_required",
    "deny_cross_tenant_required",
    "deny_missing_permission_required",
    "redaction_gate_required",
    "audit_event_required",
    "trace_id_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "subject_id",
    "tenant_id",
    "role",
    "resource_type",
    "resource_id",
    "resource_tenant_id",
    "action",
    "ownership_status",
    "approval_relationship",
    "break_glass",
    "policy_context",
    "redaction_status",
    "decision",
    "visible_fields",
    "operator_action",
    "audit_event",
}

REQUIRED_ROLES = {
    "viewer",
    "operator",
    "approver",
    "finops",
    "security",
    "tenant_admin",
    "auditor",
}

REQUIRED_RESOURCES = {
    "incident",
    "trace",
    "route_registry",
    "workflow",
    "autonomy_agents",
    "approvals",
    "budget",
    "execution_boundaries",
    "access_audit",
}

REQUIRED_POLICY_ORDER = [
    "deny_unknown_role",
    "deny_unredacted_sensitive",
    "deny_self_approval",
    "allow_break_glass_limited_view",
    "deny_cross_tenant",
    "deny_missing_permission",
    "allow_explicit_permission",
    "deny_default",
]

REQUIRED_DECISIONS = {
    "allow_incident_overview",
    "allow_trace_view",
    "allow_approval_review",
    "allow_budget_view",
    "allow_execution_boundary_view",
    "allow_access_audit_view",
    "deny_unknown_role",
    "deny_cross_tenant",
    "deny_missing_permission",
    "deny_unredacted_sensitive",
    "deny_self_approval",
    "allow_break_glass_limited_view",
}

REQUIRED_SOURCES = {
    "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html",
    "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html",
    "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html",
    "https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html",
    "https://pages.nist.gov/800-63-4/sp800-63b.html",
}

REQUIRED_LIVE_CHECKS = {
    "identity_provider_selection_review",
    "authentication_assurance_review",
    "session_security_review",
    "tenant_context_binding_review",
    "permission_matrix_review",
    "policy_engine_integration_review",
    "redaction_policy_review",
    "approval_separation_review",
    "break_glass_runbook_review",
    "access_audit_retention_review",
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
        "auth_server_started",
        "identity_provider_called",
        "token_issued",
        "session_created",
        "api_server_started",
        "frontend_runtime_started",
        "browser_started",
        "policy_engine_started",
        "database_started",
        "network_call_made",
        "provider_call_made",
        "tool_calls_executed",
        "command_executed",
        "file_write_performed",
        "external_network_required_for_this_lesson",
        "persistent_storage_created",
        "approved_for_live_access",
    ]:
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
        if note.get("date_checked") != "2026-04-30":
            missing.append(f"source_note_date_must_be_2026_04_30:{note.get('source')}")

    for url in sorted(REQUIRED_SOURCES):
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_catalogs(plan: dict[str, object], missing: list[str]) -> None:
    roles = plan.get("role_catalog", [])
    observed_roles: set[str] = set()
    if not isinstance(roles, list) or len(roles) < len(REQUIRED_ROLES):
        missing.append("complete_role_catalog_required")
    else:
        for role in roles:
            if not isinstance(role, dict):
                missing.append("role_catalog_entry_must_be_object")
                continue
            role_name = role.get("role")
            if isinstance(role_name, str):
                observed_roles.add(role_name)
            for field in [
                "role",
                "description",
                "permissions",
                "sensitive_fields_allowed",
                "may_approve",
                "cross_tenant_allowed",
            ]:
                if field not in role:
                    missing.append(f"role_missing_field:{field}")
            permissions = role.get("permissions")
            if not isinstance(permissions, list) or not permissions:
                missing.append(f"role_permissions_required:{role_name}")
            else:
                for permission in permissions:
                    if permission == "*" or not isinstance(permission, str) or ":" not in permission:
                        missing.append(f"invalid_role_permission:{role_name}:{permission}")
            if role.get("cross_tenant_allowed") is not False:
                missing.append(f"role_cross_tenant_must_default_false:{role_name}")

    for role_name in sorted(REQUIRED_ROLES):
        if role_name not in observed_roles:
            missing.append(f"missing_role:{role_name}")

    resources = plan.get("resource_catalog", [])
    observed_resources: set[str] = set()
    if not isinstance(resources, list) or len(resources) < len(REQUIRED_RESOURCES):
        missing.append("complete_resource_catalog_required")
    else:
        for resource in resources:
            if not isinstance(resource, dict):
                missing.append("resource_catalog_entry_must_be_object")
                continue
            resource_type = resource.get("resource_type")
            if isinstance(resource_type, str):
                observed_resources.add(resource_type)
            for field in [
                "resource_type",
                "panel_id",
                "tenant_scoped",
                "sensitivity",
                "allowed_actions",
                "default_visible_fields",
            ]:
                if field not in resource:
                    missing.append(f"resource_missing_field:{field}")
            if resource.get("tenant_scoped") is not True:
                missing.append(f"resource_must_be_tenant_scoped:{resource_type}")
            if not isinstance(resource.get("allowed_actions"), list) or not resource["allowed_actions"]:
                missing.append(f"resource_allowed_actions_required:{resource_type}")
            if not isinstance(resource.get("default_visible_fields"), list):
                missing.append(f"resource_default_visible_fields_required:{resource_type}")

    for resource_type in sorted(REQUIRED_RESOURCES):
        if resource_type not in observed_resources:
            missing.append(f"missing_resource:{resource_type}")


def _require_cases(plan: dict[str, object], missing: list[str]) -> None:
    cases = plan.get("access_cases", [])
    observed_decisions: set[str] = set()
    required_case_fields = {
        "case_id",
        "name",
        "subject_id",
        "tenant_id",
        "role",
        "resource_type",
        "resource_id",
        "resource_tenant_id",
        "action",
        "ownership_status",
        "approval_relationship",
        "break_glass",
        "policy_context",
        "redaction_status",
        "expected_decision",
        "expected_visible_fields",
        "expected_operator_action",
        "expected_audit_event",
    }

    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("access_case_for_each_decision_required")
        return

    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            missing.append("access_case_must_be_object")
            continue
        case_id = str(case.get("case_id", ""))
        if not case_id:
            missing.append("access_case_id_required")
        elif case_id in case_ids:
            missing.append(f"duplicate_access_case_id:{case_id}")
        case_ids.add(case_id)

        for field in sorted(required_case_fields):
            if field not in case:
                missing.append(f"access_case_missing_field:{case_id}:{field}")

        decision = case.get("expected_decision")
        if isinstance(decision, str):
            observed_decisions.add(decision)
        if decision not in REQUIRED_DECISIONS:
            missing.append(f"unexpected_expected_decision:{case_id}:{decision}")
        if not isinstance(case.get("expected_visible_fields"), list):
            missing.append(f"expected_visible_fields_must_be_list:{case_id}")
        if case.get("break_glass") is True and case.get("expected_decision") != "allow_break_glass_limited_view":
            missing.append(f"break_glass_case_must_use_limited_view:{case_id}")
        if case.get("break_glass") is True and "break_glass_reason" not in case.get(
            "expected_visible_fields", []
        ):
            missing.append(f"break_glass_visible_reason_required:{case_id}")

    for decision in sorted(REQUIRED_DECISIONS):
        if decision not in observed_decisions:
            missing.append(f"missing_access_case_for_decision:{decision}")


def validate_policy_aware_access_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "policy_aware_access_plan_no_runtime":
        missing.append("mode_must_be_policy_aware_access_plan_no_runtime")
    if plan.get("version") != "v27":
        missing.append("version_must_be_v27")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("access_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("access_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_access_dimension:{dimension}")

    policy_order = plan.get("policy_order", [])
    if policy_order != REQUIRED_POLICY_ORDER:
        missing.append("policy_order_must_match_deny_first_sequence")

    decision_gates = plan.get("decision_gates", {})
    if not isinstance(decision_gates, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if not decision_gates.get(decision):
                missing.append(f"missing_decision_gate:{decision}")

    _require_catalogs(plan, missing)
    _require_cases(plan, missing)

    live_checks = set(plan.get("required_before_live_access", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_access_check:{check}")

    return {
        "plan": str(PLAN_PATH),
        "mode": plan.get("mode"),
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_policy_aware_access_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
