#!/usr/bin/env python3
"""Validate Phase 7 v23.5 agent evaluation plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/agent-evaluation.plan.json")

REQUIRED_SCOPE_CONTROLS = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v20_2_route_decisions",
    "uses_v21_tool_registry_results",
    "uses_v22_workflow_state",
    "uses_v23_orchestration_decisions",
    "dataset_required",
    "expected_outputs_required",
    "observed_outputs_required",
    "dimension_grading_required",
    "weighted_score_required",
    "critical_safety_gate_required",
    "regression_thresholds_required",
    "trace_context_required",
    "local_simulation_only",
    "no_live_eval_service",
    "no_provider_call",
    "no_tool_execution",
}

REQUIRED_CONTROLS = {
    "case_ids_required",
    "case_types_required",
    "expected_route_required",
    "expected_registry_required",
    "expected_workflow_required",
    "expected_orchestration_required",
    "observed_outputs_required",
    "metric_catalog_required",
    "metric_weights_required",
    "pass_threshold_required",
    "critical_metrics_required",
    "safety_block_cases_required",
    "approval_cases_required",
    "budget_cases_required",
    "loop_guard_cases_required",
    "trace_id_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "case_type",
    "incident_id",
    "trace_id",
    "route_decision",
    "registry_decision",
    "workflow_decision",
    "workflow_state",
    "orchestration_decision",
    "next_action",
    "safety_gate",
    "budget_guard",
    "weighted_score",
    "critical_pass",
    "regression_status",
}

REQUIRED_METRIC_FIELDS = {
    "route_decision",
    "registry_decision",
    "workflow_decision",
    "workflow_state",
    "orchestration_decision",
    "next_action",
    "safety_gate",
    "budget_guard",
}

REQUIRED_CASE_TYPES = {
    "happy_path",
    "approval",
    "safety_block",
    "budget_guard",
    "loop_guard",
    "timeout",
}

REQUIRED_LIVE_CHECKS = {
    "official_eval_tooling_review",
    "dataset_ownership_review",
    "golden_case_review",
    "metric_weight_review",
    "critical_safety_metric_review",
    "trace_grading_review",
    "human_feedback_workflow",
    "regression_dashboard",
    "eval_data_retention_review",
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
        "evaluation_runtime_started",
        "orchestration_runtime_started",
        "workflow_runtime_started",
        "mcp_server_started",
        "tool_calls_executed",
        "provider_call_made",
        "external_eval_service_called",
        "durable_store_created",
        "persistent_storage_created",
        "external_network_required_for_this_lesson",
        "approved_for_live_evaluation",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")


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
        if isinstance(note.get("url"), str):
            urls.add(str(note["url"]))
        if note.get("date_checked") != "2026-04-30":
            missing.append(f"source_note_date_must_be_2026_04_30:{note.get('source')}")
    for url in [
        "https://platform.openai.com/docs/guides/agent-evals",
        "https://platform.openai.com/docs/api-reference/evals",
        "https://docs.smith.langchain.com/",
    ]:
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_non_negative_number(value: object, label: str, missing: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        missing.append(f"{label}_must_be_numeric")
    elif value < 0:
        missing.append(f"{label}_must_be_non_negative")


def validate_agent_evaluation_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "agent_evaluation_plan_no_runtime":
        missing.append("mode_must_be_agent_evaluation_plan_no_runtime")
    if plan.get("version") != "v23.5":
        missing.append("version_must_be_v23_5")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("evaluation_scope"), REQUIRED_SCOPE_CONTROLS, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("evaluation_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_evaluation_dimension:{dimension}")

    thresholds = plan.get("thresholds", {})
    if not isinstance(thresholds, dict):
        missing.append("thresholds_must_be_object")
    else:
        for field in [
            "min_case_score",
            "min_overall_score",
            "min_safety_score",
            "min_critical_pass_rate",
            "max_provider_calls",
            "max_tool_calls",
            "max_external_eval_service_calls",
        ]:
            _require_non_negative_number(thresholds.get(field), f"threshold:{field}", missing)
        for field in ["max_provider_calls", "max_tool_calls", "max_external_eval_service_calls"]:
            if thresholds.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    metrics = plan.get("metric_catalog", [])
    metric_fields: set[str] = set()
    critical_fields: set[str] = set()
    total_weight = 0.0
    if not isinstance(metrics, list) or len(metrics) < 8:
        missing.append("at_least_eight_metrics_required")
    else:
        for metric in metrics:
            if not isinstance(metric, dict):
                missing.append("metric_must_be_object")
                continue
            metric_id = metric.get("metric_id")
            for field in ["metric_id", "field", "weight", "critical"]:
                if field not in metric:
                    missing.append(f"metric_missing_field:{field}:{metric_id}")
            field_name = metric.get("field")
            if isinstance(field_name, str):
                metric_fields.add(field_name)
                if metric.get("critical") is True:
                    critical_fields.add(field_name)
            weight = metric.get("weight")
            if not isinstance(weight, (int, float)) or isinstance(weight, bool):
                missing.append(f"metric_weight_must_be_numeric:{metric_id}")
            elif weight <= 0:
                missing.append(f"metric_weight_must_be_positive:{metric_id}")
            else:
                total_weight += float(weight)
            if not isinstance(metric.get("critical"), bool):
                missing.append(f"metric_critical_must_be_boolean:{metric_id}")
        if round(total_weight, 6) != 1.0:
            missing.append("metric_weights_must_sum_to_1_0")
        for field in sorted(REQUIRED_METRIC_FIELDS):
            if field not in metric_fields:
                missing.append(f"missing_metric_field:{field}")
        for field in ["registry_decision", "safety_gate"]:
            if field not in critical_fields:
                missing.append(f"missing_critical_metric_field:{field}")

    required_case_types = set(plan.get("required_case_types", []))
    for case_type in sorted(REQUIRED_CASE_TYPES):
        if case_type not in required_case_types:
            missing.append(f"missing_required_case_type:{case_type}")

    cases = plan.get("eval_cases", [])
    if not isinstance(cases, list) or len(cases) < 10:
        missing.append("at_least_ten_eval_cases_required")
    else:
        observed_case_types = set()
        case_ids = set()
        for case in cases:
            if not isinstance(case, dict):
                missing.append("eval_case_must_be_object")
                continue
            name = case.get("name")
            case_id = case.get("case_id")
            if case_id in case_ids:
                missing.append(f"duplicate_case_id:{case_id}")
            case_ids.add(case_id)
            for field in ["case_id", "name", "case_type", "incident_id", "trace_id", "expected", "observed"]:
                if field not in case:
                    missing.append(f"eval_case_missing_field:{field}:{name}")
            case_type = case.get("case_type")
            if case_type not in REQUIRED_CASE_TYPES:
                missing.append(f"unexpected_case_type:{name}")
            elif isinstance(case_type, str):
                observed_case_types.add(case_type)
            expected = case.get("expected", {})
            observed = case.get("observed", {})
            if not isinstance(expected, dict):
                missing.append(f"expected_must_be_object:{name}")
                expected = {}
            if not isinstance(observed, dict):
                missing.append(f"observed_must_be_object:{name}")
                observed = {}
            for field in sorted(REQUIRED_METRIC_FIELDS):
                if field not in expected:
                    missing.append(f"expected_missing_field:{field}:{name}")
                if field not in observed:
                    missing.append(f"observed_missing_field:{field}:{name}")
        for case_type in sorted(REQUIRED_CASE_TYPES):
            if case_type not in observed_case_types:
                missing.append(f"missing_eval_case_type:{case_type}")

    live_checks = set(plan.get("required_before_live_evaluation", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "agent_evaluation_validation_no_runtime",
        "namespace": plan.get("namespace"),
        "agent_runtime_started": False,
        "evaluation_runtime_started": False,
        "provider_call_made": False,
        "external_eval_service_called": False,
        "tool_calls_executed": False,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_agent_evaluation_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
