#!/usr/bin/env python3
"""Validate Phase 7 v20.2 budget-aware routing plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/budget-aware-routing.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "uses_v20_1_cost_units",
    "route_before_spend",
    "per_route_estimates_required",
    "remaining_budget_required",
    "confidence_required",
    "severity_required",
    "evidence_state_required",
    "human_review_for_expensive_branch",
    "no_live_enforcement",
    "local_simulation_only",
}

REQUIRED_CONTROLS = {
    "route_policy_required",
    "budget_threshold_required",
    "confidence_threshold_required",
    "severity_matrix_required",
    "expected_value_check_required",
    "remaining_budget_check_required",
    "tool_skip_rule_required",
    "model_downgrade_rule_required",
    "human_review_gate_required",
    "stop_condition_required",
    "accounting_completeness_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
}

REQUIRED_ROUTING_DIMENSIONS = {
    "incident_severity",
    "evidence_state",
    "confidence",
    "remaining_budget_units",
    "estimated_route_cost_units",
    "expected_value_units",
    "value_to_cost_ratio",
    "model_tier",
    "planned_tools",
    "human_review_required",
    "stop_condition",
}

REQUIRED_THRESHOLDS = {
    "min_confidence_skip_tool",
    "min_confidence_no_more_evidence",
    "max_low_severity_route_cost",
    "max_medium_severity_route_cost",
    "max_high_severity_route_cost",
    "expensive_branch_review_cost",
    "min_remaining_budget_after_route",
    "min_expected_value_to_cost_ratio",
}

REQUIRED_DECISIONS = {
    "route_small_model_no_tool",
    "route_read_only_tool",
    "request_budget_review",
    "stop_budget_exhausted",
    "route_high_severity_full_investigation",
    "block_incomplete_accounting",
}

REQUIRED_ROUTE_IDS = {
    "small_model_no_tool",
    "read_only_evidence",
    "full_investigation",
    "human_budget_review",
}

REQUIRED_LIVE_CHECKS = {
    "official_provider_pricing_review",
    "cost_accounting_reconciliation",
    "route_policy_owner_assigned",
    "severity_budget_review",
    "expected_value_scoring_review",
    "human_budget_review_workflow",
    "tool_execution_approval_boundary",
    "routing_observability_dashboard",
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


def _require_zero_limits(limits: object, missing: list[str]) -> None:
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
        return
    for field in [
        "max_agent_runtimes_for_lesson",
        "max_routing_runtimes_for_lesson",
        "max_tool_calls_for_lesson",
        "max_provider_calls_for_lesson",
        "max_billing_api_calls_for_lesson",
        "max_external_network_calls_for_lesson",
        "max_persistent_storage_mb",
        "max_spend_usd",
    ]:
        if limits.get(field) != 0:
            missing.append(f"{field}_must_be_zero")


def _require_non_negative_number(value: object, label: str, missing: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        missing.append(f"{label}_must_be_numeric")
    elif value < 0:
        missing.append(f"{label}_must_be_non_negative")


def validate_budget_aware_routing_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "budget_aware_routing_plan_no_runtime":
        missing.append("mode_must_be_budget_aware_routing_plan_no_runtime")
    if plan.get("version") != "v20.2":
        missing.append("version_must_be_v20_2")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    for field in [
        "agent_runtime_started",
        "routing_runtime_started",
        "tool_calls_executed",
        "provider_call_made",
        "billing_api_called",
        "external_network_required_for_this_lesson",
        "persistent_storage_created",
        "approved_for_live_budget_routing",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    _require_true_fields(plan.get("routing_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    routing_dimensions = set(plan.get("routing_dimensions", []))
    for dimension in sorted(REQUIRED_ROUTING_DIMENSIONS):
        if dimension not in routing_dimensions:
            missing.append(f"missing_routing_dimension:{dimension}")

    thresholds = plan.get("thresholds", {})
    if not isinstance(thresholds, dict):
        missing.append("thresholds_must_be_object")
    else:
        for field in sorted(REQUIRED_THRESHOLDS):
            value = thresholds.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                missing.append(f"threshold_must_be_numeric:{field}")
            elif value <= 0:
                missing.append(f"threshold_must_be_positive:{field}")
        expected_thresholds = {
            "min_confidence_skip_tool": 0.85,
            "min_confidence_no_more_evidence": 0.75,
            "max_low_severity_route_cost": 1.5,
            "max_medium_severity_route_cost": 3.0,
            "max_high_severity_route_cost": 5.0,
            "expensive_branch_review_cost": 3.5,
            "min_remaining_budget_after_route": 0.5,
            "min_expected_value_to_cost_ratio": 1.2,
        }
        for field, expected in expected_thresholds.items():
            if thresholds.get(field) != expected:
                missing.append(f"{field}_must_be_{str(expected).replace('.', '_')}")

    severity_limits = plan.get("severity_route_limits", {})
    if not isinstance(severity_limits, dict):
        missing.append("severity_route_limits_must_be_object")
    else:
        for severity in ["low", "medium", "high"]:
            if severity not in severity_limits:
                missing.append(f"missing_severity_route_limit:{severity}")
            else:
                _require_non_negative_number(
                    severity_limits[severity],
                    f"severity_route_limit:{severity}",
                    missing,
                )

    _require_zero_limits(plan.get("limits"), missing)

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    route_catalog = plan.get("route_catalog", [])
    if not isinstance(route_catalog, list) or len(route_catalog) < 4:
        missing.append("at_least_four_routes_required")
        catalog_route_ids: set[str] = set()
    else:
        catalog_route_ids = set()
        for route in route_catalog:
            if not isinstance(route, dict):
                missing.append("route_catalog_item_must_be_object")
                continue
            route_id = route.get("route_id")
            if isinstance(route_id, str):
                catalog_route_ids.add(route_id)
            for field in [
                "route_id",
                "model_tier",
                "planned_tools",
                "default_use",
                "read_only",
                "requires_human_review",
            ]:
                if field not in route:
                    missing.append(f"route_catalog_missing_field:{field}:{route_id}")
            if route.get("read_only") is not True:
                missing.append(f"route_must_be_read_only:{route_id}")
            if not isinstance(route.get("planned_tools"), list):
                missing.append(f"planned_tools_must_be_list:{route_id}")
        for route_id in sorted(REQUIRED_ROUTE_IDS):
            if route_id not in catalog_route_ids:
                missing.append(f"missing_catalog_route:{route_id}")

    cases = plan.get("incident_cases", [])
    if not isinstance(cases, list) or len(cases) < 6:
        missing.append("at_least_six_incident_cases_required")
    else:
        observed_decisions = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("incident_case_must_be_object")
                continue
            name = case.get("name")
            for field in [
                "name",
                "incident_id",
                "symptom",
                "severity",
                "evidence_state",
                "confidence",
                "remaining_budget_units",
                "accounting_complete",
                "expected_decision",
                "expected_route",
                "expected_next_action",
                "candidate_routes",
            ]:
                if field not in case:
                    missing.append(f"incident_case_missing_field:{field}:{name}")
            if case.get("severity") not in {"low", "medium", "high"}:
                missing.append(f"unexpected_severity:{name}")
            if case.get("evidence_state") not in {"complete", "partial", "missing"}:
                missing.append(f"unexpected_evidence_state:{name}")
            _require_non_negative_number(case.get("confidence"), f"confidence:{name}", missing)
            _require_non_negative_number(
                case.get("remaining_budget_units"),
                f"remaining_budget_units:{name}",
                missing,
            )
            if not isinstance(case.get("accounting_complete"), bool):
                missing.append(f"accounting_complete_must_be_boolean:{name}")
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_case_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)

            candidate_routes = case.get("candidate_routes", [])
            if not isinstance(candidate_routes, list) or not candidate_routes:
                missing.append(f"candidate_routes_required:{name}")
                continue
            for route in candidate_routes:
                if not isinstance(route, dict):
                    missing.append(f"candidate_route_must_be_object:{name}")
                    continue
                route_id = route.get("route_id")
                for field in [
                    "route_id",
                    "model_tier",
                    "planned_tools",
                    "estimated_cost_units",
                    "expected_value_units",
                ]:
                    if field not in route:
                        missing.append(f"candidate_route_missing_field:{name}:{field}")
                if route_id not in catalog_route_ids:
                    missing.append(f"candidate_route_not_in_catalog:{name}:{route_id}")
                if not isinstance(route.get("planned_tools"), list):
                    missing.append(f"candidate_planned_tools_must_be_list:{name}:{route_id}")
                _require_non_negative_number(
                    route.get("estimated_cost_units"),
                    f"estimated_cost_units:{name}:{route_id}",
                    missing,
                )
                _require_non_negative_number(
                    route.get("expected_value_units"),
                    f"expected_value_units:{name}:{route_id}",
                    missing,
                )

        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_budget_routing", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "budget_aware_routing_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "routing_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "billing_api_called": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_budget_aware_routing_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
