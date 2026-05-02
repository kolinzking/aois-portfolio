#!/usr/bin/env python3
"""Validate Phase 9 v29 experiment/model delivery tracking without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("release-safety/aois-p/experiment-model-delivery.plan.json")

REQUIRED_FALSE_FLAGS = {
    "experiment_tracker_started",
    "model_registry_started",
    "training_job_started",
    "eval_job_started",
    "model_downloaded",
    "model_uploaded",
    "model_promoted",
    "traffic_shifted",
    "feature_flag_service_called",
    "rollout_controller_started",
    "database_started",
    "network_call_made",
    "provider_call_made",
    "tool_calls_executed",
    "command_executed",
    "file_write_performed",
    "external_network_required_for_this_lesson",
    "persistent_storage_created",
    "approved_for_live_model_delivery",
}

REQUIRED_SCOPE = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v28_release_controls",
    "local_simulation_only",
    "tracking_contract_only",
    "no_live_tracking_server",
    "no_live_model_registry",
    "no_training_job",
    "no_model_upload",
    "no_model_download",
    "no_live_rollout",
    "no_live_feature_flag_change",
    "no_network_call",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "experiment_id_required",
    "hypothesis_required",
    "baseline_version_required",
    "candidate_version_required",
    "dataset_version_required",
    "metric_catalog_required",
    "guardrail_metric_required",
    "offline_eval_required",
    "online_rollout_evidence_required",
    "version_comparison_required",
    "champion_challenger_required",
    "model_registry_record_required",
    "release_candidate_link_required",
    "feature_flag_link_required",
    "rollback_target_required",
    "approval_record_required",
    "audit_event_required",
    "risk_review_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "experiment_id",
    "change_id",
    "baseline_model_version",
    "candidate_model_version",
    "dataset_version",
    "hypothesis_status",
    "offline_eval_status",
    "metric_delta",
    "guardrail_status",
    "sample_size_status",
    "rollout_evidence_status",
    "model_registry_status",
    "release_gate_status",
    "feature_flag_status",
    "rollback_ready",
    "approval_status",
    "risk_status",
    "delivery_decision",
    "operator_action",
}

REQUIRED_METRICS = {
    "quality_score",
    "latency_p95_ms",
    "cost_per_1k_tokens",
    "safety_violation_rate",
    "policy_regression_count",
    "tenant_isolation_failures",
}

REQUIRED_STAGES = {
    "experiment_design",
    "offline_evaluation",
    "version_comparison",
    "registry_link",
    "rollout_evidence",
    "delivery_decision",
}

REQUIRED_DECISIONS = {
    "allow_model_delivery_candidate",
    "block_missing_hypothesis",
    "block_missing_baseline",
    "block_missing_candidate_version",
    "block_missing_dataset_version",
    "block_offline_eval_failed",
    "block_metric_regression",
    "block_guardrail_regression",
    "hold_sample_size_insufficient",
    "hold_missing_rollout_evidence",
    "block_registry_incomplete",
    "block_release_gate_failed",
    "hold_feature_flag_not_ready",
    "block_no_rollback",
    "block_missing_approval",
    "hold_risk_review",
}

REQUIRED_SOURCES = {
    "https://mlflow.org/docs/latest/ml/tracking/",
    "https://mlflow.org/docs/latest/ml/model-registry/",
    "https://openfeature.dev/specification/",
    "https://argo-rollouts.readthedocs.io/en/stable/features/analysis/",
    "https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook",
}

REQUIRED_LIVE_CHECKS = {
    "experiment_tracking_review",
    "model_registry_review",
    "dataset_version_review",
    "metric_catalog_review",
    "offline_eval_review",
    "guardrail_review",
    "sample_size_review",
    "rollout_evidence_review",
    "release_gate_review",
    "feature_flag_review",
    "rollback_review",
    "approval_record_review",
    "risk_review",
    "primary_aois_separation_review",
    "resource_usage_record",
}

REQUIRED_DEFAULTS = {
    "hypothesis_status": "documented",
    "offline_eval_status": "pass",
    "guardrail_status": "pass",
    "sample_size_status": "sufficient",
    "rollout_evidence_status": "complete",
    "model_registry_status": "complete",
    "release_gate_status": "pass",
    "feature_flag_status": "guarded",
    "rollback_ready": True,
    "approval_status": "approved",
    "risk_status": "accepted",
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


def _require_metric_catalog(plan: dict[str, object], missing: list[str]) -> None:
    metrics = plan.get("metric_catalog", [])
    observed: set[str] = set()
    if not isinstance(metrics, list) or len(metrics) < len(REQUIRED_METRICS):
        missing.append("complete_metric_catalog_required")
        return
    for metric in metrics:
        if not isinstance(metric, dict):
            missing.append("metric_catalog_entry_must_be_object")
            continue
        metric_id = metric.get("metric_id")
        if isinstance(metric_id, str):
            observed.add(metric_id)
        for field in ["metric_id", "direction", "blocks_on_regression"]:
            if field not in metric:
                missing.append(f"metric_missing_field:{field}")
        if metric.get("blocks_on_regression") is not True:
            missing.append(f"metric_must_block_on_regression:{metric_id}")

    for metric_id in sorted(REQUIRED_METRICS):
        if metric_id not in observed:
            missing.append(f"missing_metric:{metric_id}")


def _require_evidence_stages(plan: dict[str, object], missing: list[str]) -> None:
    stages = plan.get("evidence_stages", [])
    observed: set[str] = set()
    if not isinstance(stages, list) or len(stages) < len(REQUIRED_STAGES):
        missing.append("complete_evidence_stage_catalog_required")
        return
    for stage in stages:
        if not isinstance(stage, dict):
            missing.append("evidence_stage_must_be_object")
            continue
        stage_id = stage.get("stage_id")
        if isinstance(stage_id, str):
            observed.add(stage_id)
        for field in ["stage_id", "required_fields", "blocks_on_missing"]:
            if field not in stage:
                missing.append(f"evidence_stage_missing_field:{field}")
        if stage.get("blocks_on_missing") is not True:
            missing.append(f"evidence_stage_must_block_on_missing:{stage_id}")
        if not isinstance(stage.get("required_fields"), list) or not stage["required_fields"]:
            missing.append(f"evidence_stage_required_fields_missing:{stage_id}")

    for stage_id in sorted(REQUIRED_STAGES):
        if stage_id not in observed:
            missing.append(f"missing_evidence_stage:{stage_id}")


def _require_defaults(defaults: object, missing: list[str]) -> None:
    if not isinstance(defaults, dict):
        missing.append("case_defaults_must_be_object")
        return
    for field, expected in REQUIRED_DEFAULTS.items():
        if defaults.get(field) != expected:
            missing.append(f"case_default_mismatch:{field}")
    for field in ["experiment_id", "change_id", "baseline_model_version", "candidate_model_version", "dataset_version"]:
        if not defaults.get(field):
            missing.append(f"case_default_required:{field}")
    metric_delta = defaults.get("metric_delta")
    if not isinstance(metric_delta, dict):
        missing.append("case_default_metric_delta_must_be_object")
    else:
        for metric_id in sorted(REQUIRED_METRICS):
            if metric_id not in metric_delta:
                missing.append(f"case_default_metric_missing:{metric_id}")


def _require_cases(plan: dict[str, object], missing: list[str]) -> None:
    cases = plan.get("delivery_cases", [])
    observed_decisions: set[str] = set()
    required_case_fields = {
        "case_id",
        "name",
        "expected_decision",
        "expected_operator_action",
        "expected_delivery_state",
    }
    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("delivery_case_for_each_decision_required")
        return

    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            missing.append("delivery_case_must_be_object")
            continue
        case_id = str(case.get("case_id", ""))
        if not case_id:
            missing.append("delivery_case_id_required")
        elif case_id in case_ids:
            missing.append(f"duplicate_delivery_case_id:{case_id}")
        case_ids.add(case_id)

        for field in sorted(required_case_fields):
            if field not in case:
                missing.append(f"delivery_case_missing_field:{case_id}:{field}")
        decision = case.get("expected_decision")
        if isinstance(decision, str):
            observed_decisions.add(decision)
        if decision not in REQUIRED_DECISIONS:
            missing.append(f"unexpected_expected_decision:{case_id}:{decision}")
        if "overrides" in case and not isinstance(case["overrides"], dict):
            missing.append(f"delivery_case_overrides_must_be_object:{case_id}")

    for decision in sorted(REQUIRED_DECISIONS):
        if decision not in observed_decisions:
            missing.append(f"missing_delivery_case_for_decision:{decision}")


def validate_experiment_model_delivery_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "experiment_model_delivery_tracking_plan_no_runtime":
        missing.append("mode_must_be_experiment_model_delivery_tracking_plan_no_runtime")
    if plan.get("version") != "v29":
        missing.append("version_must_be_v29")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("tracking_scope"), REQUIRED_SCOPE, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("delivery_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_delivery_dimension:{dimension}")

    decision_gates = plan.get("decision_gates", {})
    if not isinstance(decision_gates, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if not decision_gates.get(decision):
                missing.append(f"missing_decision_gate:{decision}")

    _require_metric_catalog(plan, missing)
    _require_evidence_stages(plan, missing)
    _require_defaults(plan.get("case_defaults"), missing)
    _require_cases(plan, missing)

    live_checks = set(plan.get("required_before_live_model_delivery", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_model_delivery_check:{check}")

    return {
        "plan": str(PLAN_PATH),
        "mode": plan.get("mode"),
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_experiment_model_delivery_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
