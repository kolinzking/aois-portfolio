#!/usr/bin/env python3
"""Validate Phase 9 v30 internal platform patterns without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("platform/aois-p/internal-platform-patterns.plan.json")

REQUIRED_FALSE_FLAGS = {
    "platform_runtime_started",
    "developer_portal_started",
    "service_catalog_started",
    "platform_api_started",
    "template_engine_started",
    "cli_invoked",
    "infrastructure_provisioned",
    "kubernetes_applied",
    "gitops_sync_started",
    "workflow_started",
    "database_started",
    "network_call_made",
    "provider_call_made",
    "tool_calls_executed",
    "command_executed",
    "file_write_performed",
    "external_network_required_for_this_lesson",
    "persistent_storage_created",
    "approved_for_live_platform",
}

REQUIRED_SCOPE = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_phase9_release_and_model_delivery_contracts",
    "local_simulation_only",
    "platform_contract_only",
    "no_live_developer_portal",
    "no_live_service_catalog",
    "no_live_platform_api",
    "no_live_template_render",
    "no_live_infrastructure_provisioning",
    "no_live_cluster_change",
    "no_live_gitops_sync",
    "no_network_call",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "capability_catalog_required",
    "owner_required",
    "documentation_required",
    "golden_path_template_required",
    "self_service_request_contract_required",
    "platform_api_contract_required",
    "versioning_required",
    "deprecation_policy_required",
    "policy_defaults_required",
    "security_boundary_required",
    "cost_boundary_required",
    "tenant_boundary_required",
    "permission_boundary_required",
    "observability_contract_required",
    "release_integration_required",
    "model_delivery_integration_required",
    "rollback_contract_required",
    "approval_record_required",
    "audit_event_required",
    "support_slo_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "capability_id",
    "user_persona",
    "request_type",
    "interface_type",
    "owner",
    "documentation_status",
    "api_contract_status",
    "template_status",
    "policy_status",
    "security_status",
    "cost_status",
    "observability_status",
    "release_integration_status",
    "model_delivery_status",
    "tenant_boundary_status",
    "approval_status",
    "support_slo_status",
    "lifecycle_status",
    "platform_decision",
    "operator_action",
}

REQUIRED_CAPABILITIES = {
    "aois_service_starter",
    "observability_bundle",
    "delivery_pipeline_bundle",
    "model_delivery_bundle",
    "policy_access_bundle",
    "cost_budget_bundle",
    "incident_response_bundle",
    "environment_request",
}

REQUIRED_INTERFACES = {"portal", "api", "template", "cli"}

REQUIRED_DECISIONS = {
    "allow_self_service_capability",
    "block_unknown_capability",
    "block_deprecated_capability",
    "block_missing_owner",
    "block_missing_docs",
    "block_missing_api_contract",
    "block_missing_template",
    "block_policy_boundary",
    "block_security_boundary",
    "hold_cost_review",
    "block_observability_missing",
    "block_release_integration_missing",
    "hold_model_delivery_integration",
    "block_tenant_boundary_missing",
    "block_approval_missing",
    "hold_support_slo_missing",
}

REQUIRED_SOURCES = {
    "https://tag-app-delivery.cncf.io/whitepapers/platforms/",
    "https://backstage.io/docs/features/software-catalog/",
    "https://kubernetes.io/docs/concepts/api-extension/custom-resources/",
    "https://spec.openapis.org/oas/latest.html",
    "https://openfeature.dev/specification/",
}

REQUIRED_LIVE_CHECKS = {
    "platform_product_review",
    "capability_catalog_review",
    "developer_portal_review",
    "platform_api_contract_review",
    "golden_path_template_review",
    "policy_default_review",
    "security_boundary_review",
    "cost_quota_review",
    "tenant_boundary_review",
    "observability_contract_review",
    "release_integration_review",
    "model_delivery_integration_review",
    "approval_workflow_review",
    "support_slo_review",
    "deprecation_policy_review",
    "primary_aois_separation_review",
    "resource_usage_record",
}

REQUIRED_DEFAULTS = {
    "capability_id": "aois_service_starter",
    "documentation_status": "complete",
    "api_contract_status": "complete",
    "template_status": "complete",
    "policy_status": "pass",
    "security_status": "pass",
    "cost_status": "approved",
    "observability_status": "complete",
    "release_integration_status": "complete",
    "model_delivery_status": "not_applicable",
    "tenant_boundary_status": "complete",
    "approval_status": "not_required",
    "support_slo_status": "defined",
    "lifecycle_status": "active",
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


def _require_capabilities(plan: dict[str, object], missing: list[str]) -> None:
    capabilities = plan.get("capability_catalog", [])
    observed: set[str] = set()
    if not isinstance(capabilities, list) or len(capabilities) < len(REQUIRED_CAPABILITIES):
        missing.append("complete_capability_catalog_required")
        return
    for capability in capabilities:
        if not isinstance(capability, dict):
            missing.append("capability_catalog_entry_must_be_object")
            continue
        capability_id = capability.get("capability_id")
        if isinstance(capability_id, str):
            observed.add(capability_id)
        for field in ["capability_id", "description", "owner", "interfaces", "requires_approval"]:
            if field not in capability:
                missing.append(f"capability_missing_field:{field}")
        if not capability.get("owner"):
            missing.append(f"capability_owner_required:{capability_id}")
        if not isinstance(capability.get("interfaces"), list) or not capability["interfaces"]:
            missing.append(f"capability_interfaces_required:{capability_id}")

    for capability_id in sorted(REQUIRED_CAPABILITIES):
        if capability_id not in observed:
            missing.append(f"missing_capability:{capability_id}")


def _require_interfaces(plan: dict[str, object], missing: list[str]) -> None:
    interfaces = plan.get("interface_catalog", [])
    observed: set[str] = set()
    if not isinstance(interfaces, list) or len(interfaces) < len(REQUIRED_INTERFACES):
        missing.append("complete_interface_catalog_required")
        return
    for interface in interfaces:
        if not isinstance(interface, dict):
            missing.append("interface_catalog_entry_must_be_object")
            continue
        interface_type = interface.get("interface_type")
        if isinstance(interface_type, str):
            observed.add(interface_type)
        for field in ["interface_type", "contract", "requires_docs", "requires_owner"]:
            if field not in interface:
                missing.append(f"interface_missing_field:{field}")
        if interface.get("requires_docs") is not True:
            missing.append(f"interface_must_require_docs:{interface_type}")
        if interface.get("requires_owner") is not True:
            missing.append(f"interface_must_require_owner:{interface_type}")

    for interface_type in sorted(REQUIRED_INTERFACES):
        if interface_type not in observed:
            missing.append(f"missing_interface:{interface_type}")


def _require_defaults(defaults: object, missing: list[str]) -> None:
    if not isinstance(defaults, dict):
        missing.append("case_defaults_must_be_object")
        return
    for field, expected in REQUIRED_DEFAULTS.items():
        if defaults.get(field) != expected:
            missing.append(f"case_default_mismatch:{field}")
    for field in ["user_persona", "request_type", "interface_type", "owner"]:
        if not defaults.get(field):
            missing.append(f"case_default_required:{field}")


def _require_cases(plan: dict[str, object], missing: list[str]) -> None:
    cases = plan.get("platform_cases", [])
    observed_decisions: set[str] = set()
    required_case_fields = {
        "case_id",
        "name",
        "expected_decision",
        "expected_operator_action",
        "expected_platform_state",
    }
    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("platform_case_for_each_decision_required")
        return

    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            missing.append("platform_case_must_be_object")
            continue
        case_id = str(case.get("case_id", ""))
        if not case_id:
            missing.append("platform_case_id_required")
        elif case_id in case_ids:
            missing.append(f"duplicate_platform_case_id:{case_id}")
        case_ids.add(case_id)

        for field in sorted(required_case_fields):
            if field not in case:
                missing.append(f"platform_case_missing_field:{case_id}:{field}")
        decision = case.get("expected_decision")
        if isinstance(decision, str):
            observed_decisions.add(decision)
        if decision not in REQUIRED_DECISIONS:
            missing.append(f"unexpected_expected_decision:{case_id}:{decision}")
        if "overrides" in case and not isinstance(case["overrides"], dict):
            missing.append(f"platform_case_overrides_must_be_object:{case_id}")

    for decision in sorted(REQUIRED_DECISIONS):
        if decision not in observed_decisions:
            missing.append(f"missing_platform_case_for_decision:{decision}")


def validate_internal_platform_patterns_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "internal_platform_patterns_plan_no_runtime":
        missing.append("mode_must_be_internal_platform_patterns_plan_no_runtime")
    if plan.get("version") != "v30":
        missing.append("version_must_be_v30")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("platform_scope"), REQUIRED_SCOPE, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("platform_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_platform_dimension:{dimension}")

    decision_gates = plan.get("decision_gates", {})
    if not isinstance(decision_gates, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if not decision_gates.get(decision):
                missing.append(f"missing_decision_gate:{decision}")

    _require_capabilities(plan, missing)
    _require_interfaces(plan, missing)
    _require_defaults(plan.get("case_defaults"), missing)
    _require_cases(plan, missing)

    live_checks = set(plan.get("required_before_live_platform", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_platform_check:{check}")

    return {
        "plan": str(PLAN_PATH),
        "mode": plan.get("mode"),
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_internal_platform_patterns_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
