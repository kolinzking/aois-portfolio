#!/usr/bin/env python3
"""Validate Phase 7 v21 governed MCP tool registry plan without runtime."""

from __future__ import annotations

import json
import re
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/governed-tool-registry.plan.json")
ALLOWED_TOOL_NAME_PATTERN = r"^[A-Za-z0-9_.-]+$"

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v20_2_route_decisions",
    "route_allowlist_required",
    "server_trust_required",
    "tool_manifest_required",
    "owner_required",
    "schema_required",
    "audit_event_required",
    "approval_policy_required",
    "side_effect_classification_required",
    "local_simulation_only",
    "no_live_mcp_server",
    "no_tool_execution",
}

REQUIRED_CONTROLS = {
    "mcp_server_label_required",
    "tool_name_policy_required",
    "tool_description_treated_as_untrusted",
    "input_schema_required",
    "output_schema_expected",
    "owner_required",
    "route_allowlist_required",
    "side_effect_classification_required",
    "human_approval_for_sensitive_tools",
    "block_unregistered_tools",
    "block_untrusted_servers",
    "block_side_effecting_tools_by_default",
    "audit_event_required",
    "budget_route_context_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "tool_name",
    "server_label",
    "operation_class",
    "side_effect_level",
    "data_scope",
    "input_schema_ref",
    "output_schema_ref",
    "owner",
    "approval_policy",
    "allowed_routes",
    "allowed_decisions",
    "audit_event",
    "status",
    "default_enabled",
}

REQUIRED_DECISIONS = {
    "allow_no_tool_route",
    "allow_read_only_tool_plan",
    "require_human_approval",
    "block_unregistered_tool",
    "block_untrusted_server",
    "block_side_effecting_tool",
    "block_disabled_tool",
}

REQUIRED_TOOL_NAMES = {
    "query_service_metrics",
    "fetch_recent_logs",
    "read_incident_trace",
    "lookup_runbook_step",
    "restart_pod",
    "shell_exec",
}

REQUIRED_LIVE_CHECKS = {
    "official_mcp_spec_review",
    "threat_model_review",
    "tool_owner_review",
    "schema_contract_review",
    "human_approval_workflow",
    "tool_result_sanitization_review",
    "mcp_server_identity_review",
    "registry_change_control",
    "audit_log_sink",
    "route_policy_integration_test",
    "primary_aois_separation_review",
    "resource_usage_record",
}

VALID_SIDE_EFFECTS = {"read_only", "sensitive_read", "write_effect", "privileged_execution"}
VALID_APPROVAL_POLICIES = {
    "preapproved_read_only_plan_only",
    "human_approval_required",
    "blocked",
}
VALID_STATUSES = {"active", "review_required", "disabled"}
VALID_ROUTE_IDS = {"small_model_no_tool", "read_only_evidence", "full_investigation"}
VALID_ROUTE_DECISIONS = {
    "route_small_model_no_tool",
    "route_read_only_tool",
    "route_high_severity_full_investigation",
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


def _require_zero_limits(limits: object, missing: list[str]) -> None:
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
        return
    for field in [
        "max_agent_runtimes_for_lesson",
        "max_mcp_servers_for_lesson",
        "max_tool_registry_runtimes_for_lesson",
        "max_tool_calls_for_lesson",
        "max_provider_calls_for_lesson",
        "max_external_network_calls_for_lesson",
        "max_persistent_storage_mb",
        "max_spend_usd",
    ]:
        if limits.get(field) != 0:
            missing.append(f"{field}_must_be_zero")


def _require_source_notes(source_notes: object, missing: list[str]) -> None:
    if not isinstance(source_notes, list) or len(source_notes) < 3:
        missing.append("at_least_three_source_notes_required")
        return
    urls = set()
    for note in source_notes:
        if not isinstance(note, dict):
            missing.append("source_note_must_be_object")
            continue
        for field in ["source", "url", "date_checked", "supports"]:
            if not note.get(field):
                missing.append(f"source_note_missing_field:{field}")
        url = note.get("url")
        if isinstance(url, str):
            urls.add(url)
        if note.get("date_checked") != "2026-04-29":
            missing.append(f"source_note_date_must_be_2026_04_29:{note.get('source')}")
    if "https://modelcontextprotocol.io/specification/" not in urls:
        missing.append("missing_mcp_spec_source_note")


def _tool_key(tool: dict[str, object]) -> tuple[str, str]:
    return str(tool.get("server_label")), str(tool.get("tool_name"))


def validate_governed_tool_registry_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "governed_tool_registry_plan_no_runtime":
        missing.append("mode_must_be_governed_tool_registry_plan_no_runtime")
    if plan.get("version") != "v21":
        missing.append("version_must_be_v21")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    for field in [
        "agent_runtime_started",
        "mcp_server_started",
        "tool_registry_runtime_started",
        "tool_calls_executed",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "persistent_storage_created",
        "approved_for_live_mcp",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("registry_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)
    _require_zero_limits(plan.get("limits"), missing)

    registry_dimensions = set(plan.get("registry_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in registry_dimensions:
            missing.append(f"missing_registry_dimension:{dimension}")

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    server_labels = plan.get("allowed_server_labels", [])
    if not isinstance(server_labels, list) or not server_labels:
        missing.append("allowed_server_labels_required")
        allowed_server_labels: set[str] = set()
    else:
        allowed_server_labels = {str(label) for label in server_labels}

    tool_name_policy = plan.get("tool_name_policy", {})
    if not isinstance(tool_name_policy, dict):
        missing.append("tool_name_policy_must_be_object")
        tool_pattern = re.compile(ALLOWED_TOOL_NAME_PATTERN)
    else:
        if tool_name_policy.get("max_length") != 128:
            missing.append("tool_name_max_length_must_be_128")
        if tool_name_policy.get("allowed_pattern") != ALLOWED_TOOL_NAME_PATTERN:
            missing.append("tool_name_allowed_pattern_must_be_fixed_safe_pattern")
        if tool_name_policy.get("spaces_allowed") is not False:
            missing.append("tool_name_spaces_allowed_must_be_false")
        if tool_name_policy.get("unique_within_server") is not True:
            missing.append("tool_name_unique_within_server_must_be_true")
        tool_pattern = re.compile(ALLOWED_TOOL_NAME_PATTERN)

    catalog = plan.get("tool_catalog", [])
    catalog_names: set[str] = set()
    catalog_keys: set[tuple[str, str]] = set()
    if not isinstance(catalog, list) or len(catalog) < 6:
        missing.append("at_least_six_catalog_tools_required")
    else:
        for tool in catalog:
            if not isinstance(tool, dict):
                missing.append("tool_catalog_item_must_be_object")
                continue
            tool_name = tool.get("tool_name")
            server_label = tool.get("server_label")
            if isinstance(tool_name, str):
                catalog_names.add(tool_name)
            key = _tool_key(tool)
            if key in catalog_keys:
                missing.append(f"duplicate_tool_within_server:{key[0]}:{key[1]}")
            catalog_keys.add(key)
            for field in sorted(REQUIRED_DIMENSIONS | {"title", "human_approval_required"}):
                if field not in tool:
                    missing.append(f"tool_catalog_missing_field:{field}:{tool_name}")
            if not isinstance(tool_name, str) or not tool_name:
                missing.append(f"tool_name_required:{server_label}")
            elif len(tool_name) > 128:
                missing.append(f"tool_name_too_long:{tool_name}")
            elif not tool_pattern.match(tool_name):
                missing.append(f"tool_name_invalid:{tool_name}")
            if server_label not in allowed_server_labels:
                missing.append(f"tool_server_not_allowed:{tool_name}:{server_label}")
            if tool.get("side_effect_level") not in VALID_SIDE_EFFECTS:
                missing.append(f"unexpected_side_effect_level:{tool_name}")
            if tool.get("approval_policy") not in VALID_APPROVAL_POLICIES:
                missing.append(f"unexpected_approval_policy:{tool_name}")
            if tool.get("status") not in VALID_STATUSES:
                missing.append(f"unexpected_status:{tool_name}")
            if not isinstance(tool.get("allowed_routes"), list):
                missing.append(f"allowed_routes_must_be_list:{tool_name}")
            else:
                for route_id in tool["allowed_routes"]:
                    if route_id not in VALID_ROUTE_IDS:
                        missing.append(f"unexpected_allowed_route:{tool_name}:{route_id}")
            if not isinstance(tool.get("allowed_decisions"), list):
                missing.append(f"allowed_decisions_must_be_list:{tool_name}")
            else:
                for decision in tool["allowed_decisions"]:
                    if decision not in VALID_ROUTE_DECISIONS:
                        missing.append(f"unexpected_allowed_decision:{tool_name}:{decision}")
            if not tool.get("owner"):
                missing.append(f"owner_required:{tool_name}")
            if not tool.get("input_schema_ref"):
                missing.append(f"input_schema_ref_required:{tool_name}")
            if not tool.get("output_schema_ref"):
                missing.append(f"output_schema_ref_required:{tool_name}")
            if not tool.get("audit_event"):
                missing.append(f"audit_event_required:{tool_name}")

            side_effect = tool.get("side_effect_level")
            if side_effect in {"sensitive_read", "write_effect", "privileged_execution"}:
                if tool.get("human_approval_required") is not True:
                    missing.append(f"human_approval_required_for_sensitive_tool:{tool_name}")
            if side_effect in {"write_effect", "privileged_execution"}:
                if tool.get("default_enabled") is not False:
                    missing.append(f"side_effecting_tool_default_enabled_must_be_false:{tool_name}")
                if tool.get("allowed_routes") != []:
                    missing.append(f"side_effecting_tool_allowed_routes_must_be_empty:{tool_name}")
            if tool.get("status") == "disabled" and tool.get("approval_policy") != "blocked":
                missing.append(f"disabled_tool_policy_must_be_blocked:{tool_name}")

        for tool_name in sorted(REQUIRED_TOOL_NAMES):
            if tool_name not in catalog_names:
                missing.append(f"missing_catalog_tool:{tool_name}")

    cases = plan.get("registry_cases", [])
    if not isinstance(cases, list) or len(cases) < 7:
        missing.append("at_least_seven_registry_cases_required")
    else:
        observed_decisions = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("registry_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "name",
                "incident_id",
                "route_decision",
                "route_id",
                "severity",
                "requested_server_label",
                "requested_tools",
                "expected_decision",
                "expected_tools",
                "expected_approvals",
                "expected_blocks",
                "expected_next_action",
            ]:
                if field not in case:
                    missing.append(f"registry_case_missing_field:{field}:{name}")
            if case.get("route_id") not in VALID_ROUTE_IDS:
                missing.append(f"unexpected_case_route:{name}")
            if case.get("route_decision") not in VALID_ROUTE_DECISIONS:
                missing.append(f"unexpected_case_route_decision:{name}")
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_case_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)
            for list_field in ["requested_tools", "expected_tools", "expected_approvals", "expected_blocks"]:
                if not isinstance(case.get(list_field), list):
                    missing.append(f"case_{list_field}_must_be_list:{name}")
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_mcp", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "governed_tool_registry_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "mcp_server_started": False,
        "tool_registry_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_governed_tool_registry_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
