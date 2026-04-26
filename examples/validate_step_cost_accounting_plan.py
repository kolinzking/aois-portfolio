#!/usr/bin/env python3
"""Validate Phase 7 v20.1 cost accounting plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/step-cost-accounting.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "per_incident_required",
    "per_step_required",
    "model_token_estimates_required",
    "tool_cost_estimates_required",
    "approval_wait_cost_recorded",
    "retry_cost_recorded",
    "no_live_billing",
    "local_simulation_only",
}

REQUIRED_CONTROLS = {
    "cost_schema_required",
    "incident_total_required",
    "step_total_required",
    "model_usage_record_required",
    "tool_usage_record_required",
    "retry_count_required",
    "approval_wait_record_required",
    "budget_threshold_required",
    "waste_detection_required",
    "accounting_completeness_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
}

REQUIRED_USAGE_DIMENSIONS = {
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_tokens",
    "tool_call_count",
    "tool_elapsed_ms",
    "approval_wait_minutes",
    "retry_count",
    "cost_units",
}

REQUIRED_USAGE_FIELDS = REQUIRED_USAGE_DIMENSIONS - {"cost_units"}

REQUIRED_UNIT_COSTS = {
    "model_input_per_1k_tokens",
    "model_cached_input_per_1k_tokens",
    "model_output_per_1k_tokens",
    "model_reasoning_per_1k_tokens",
    "read_only_tool_call",
    "approval_wait_minute",
    "retry_penalty",
    "invalid_result_penalty",
}

REQUIRED_THRESHOLDS = {
    "max_total_cost_units_per_incident",
    "max_step_cost_units",
    "max_same_tool_calls_per_incident",
    "max_retries_per_step",
    "max_approval_wait_cost_units",
    "minimum_accounting_coverage",
}

REQUIRED_DECISIONS = {
    "within_budget",
    "step_waste_flagged",
    "incident_budget_exceeded",
    "accounting_incomplete",
    "approval_cost_review",
}

REQUIRED_LIVE_CHECKS = {
    "official_provider_pricing_review",
    "token_accounting_tests",
    "tool_metering_tests",
    "billing_api_reconciliation",
    "budget_owner_assigned",
    "approval_wait_policy",
    "retry_policy",
    "incident_cost_dashboard",
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
        "max_tool_calls_for_lesson",
        "max_provider_calls_for_lesson",
        "max_billing_api_calls_for_lesson",
        "max_external_network_calls_for_lesson",
        "max_persistent_storage_mb",
        "max_spend_usd",
    ]:
        if limits.get(field) != 0:
            missing.append(f"{field}_must_be_zero")


def _require_non_negative_number(
    value: object, label: str, missing: list[str], integer_required: bool = True
) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        missing.append(f"{label}_must_be_numeric")
        return
    if integer_required and not isinstance(value, int):
        missing.append(f"{label}_must_be_integer")
    if value < 0:
        missing.append(f"{label}_must_be_non_negative")


def validate_step_cost_accounting_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "step_cost_accounting_plan_no_runtime":
        missing.append("mode_must_be_step_cost_accounting_plan_no_runtime")
    if plan.get("version") != "v20.1":
        missing.append("version_must_be_v20_1")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("unit_cost_model") != "provider_neutral_training_units":
        missing.append("unit_cost_model_must_be_provider_neutral_training_units")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    for field in [
        "agent_runtime_started",
        "tool_calls_executed",
        "provider_call_made",
        "billing_api_called",
        "external_network_required_for_this_lesson",
        "persistent_storage_created",
        "approved_for_live_cost_enforcement",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    _require_true_fields(
        plan.get("accounting_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing
    )
    _require_true_fields(
        plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing
    )

    usage_dimensions = set(plan.get("usage_dimensions", []))
    for dimension in sorted(REQUIRED_USAGE_DIMENSIONS):
        if dimension not in usage_dimensions:
            missing.append(f"missing_usage_dimension:{dimension}")

    unit_costs = plan.get("unit_costs", {})
    if not isinstance(unit_costs, dict):
        missing.append("unit_costs_must_be_object")
    else:
        for field in sorted(REQUIRED_UNIT_COSTS):
            value = unit_costs.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                missing.append(f"unit_cost_must_be_numeric:{field}")
            elif value <= 0:
                missing.append(f"unit_cost_must_be_positive:{field}")

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
        if thresholds.get("max_total_cost_units_per_incident") != 5.0:
            missing.append("max_total_cost_units_per_incident_must_be_5_0")
        if thresholds.get("max_step_cost_units") != 2.0:
            missing.append("max_step_cost_units_must_be_2_0")
        if thresholds.get("max_same_tool_calls_per_incident") != 1:
            missing.append("max_same_tool_calls_per_incident_must_be_1")
        if thresholds.get("max_retries_per_step") != 1:
            missing.append("max_retries_per_step_must_be_1")
        if thresholds.get("max_approval_wait_cost_units") != 1.0:
            missing.append("max_approval_wait_cost_units_must_be_1_0")
        if thresholds.get("minimum_accounting_coverage") != 1.0:
            missing.append("minimum_accounting_coverage_must_be_1_0")

    _require_zero_limits(plan.get("limits"), missing)

    decisions = plan.get("decision_gates", {})
    if not isinstance(decisions, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in decisions:
                missing.append(f"missing_decision_gate:{decision}")

    cases = plan.get("incident_cases", [])
    if not isinstance(cases, list) or len(cases) < 5:
        missing.append("at_least_five_incident_cases_required")
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
                "expected_decision",
                "expected_next_action",
                "steps",
            ]:
                if field not in case:
                    missing.append(f"incident_case_missing_field:{field}:{name}")
            expected = case.get("expected_decision")
            if expected not in REQUIRED_DECISIONS:
                missing.append(f"unexpected_case_decision:{name}")
            elif isinstance(expected, str):
                observed_decisions.add(expected)

            steps = case.get("steps", [])
            if not isinstance(steps, list) or not steps:
                missing.append(f"steps_required:{name}")
                continue
            for step in steps:
                if not isinstance(step, dict):
                    missing.append(f"step_must_be_object:{name}")
                    continue
                step_id = step.get("step_id")
                for field in ["step_id", "planned_tool", "accounted", "result_valid", "usage"]:
                    if field not in step:
                        missing.append(f"step_missing_field:{name}:{field}:{step_id}")
                if not isinstance(step.get("planned_tool"), str):
                    missing.append(f"planned_tool_must_be_string:{name}:{step_id}")
                if not isinstance(step.get("accounted"), bool):
                    missing.append(f"accounted_must_be_boolean:{name}:{step_id}")
                if not isinstance(step.get("result_valid"), bool):
                    missing.append(f"result_valid_must_be_boolean:{name}:{step_id}")
                usage = step.get("usage", {})
                if not isinstance(usage, dict):
                    missing.append(f"usage_must_be_object:{name}:{step_id}")
                    continue
                for usage_field in sorted(REQUIRED_USAGE_FIELDS):
                    if usage_field not in usage:
                        missing.append(
                            f"usage_missing_field:{name}:{step_id}:{usage_field}"
                        )
                    else:
                        _require_non_negative_number(
                            usage[usage_field],
                            f"usage:{name}:{step_id}:{usage_field}",
                            missing,
                        )

        for decision in sorted(REQUIRED_DECISIONS):
            if decision not in observed_decisions:
                missing.append(f"missing_case_for_decision:{decision}")

    live_checks = set(plan.get("required_before_live_cost_enforcement", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "step_cost_accounting_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "billing_api_called": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_step_cost_accounting_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
