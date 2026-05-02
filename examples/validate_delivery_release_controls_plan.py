#!/usr/bin/env python3
"""Validate Phase 9 v28 delivery release controls without CI/runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("release-safety/aois-p/delivery-release-controls.plan.json")

REQUIRED_FALSE_FLAGS = {
    "ci_runtime_started",
    "workflow_started",
    "build_started",
    "test_runner_started",
    "container_build_started",
    "image_pushed",
    "image_signed",
    "signature_verified",
    "deployment_started",
    "kubernetes_applied",
    "rollout_started",
    "traffic_shifted",
    "feature_flag_service_called",
    "model_endpoint_changed",
    "network_call_made",
    "provider_call_made",
    "tool_calls_executed",
    "command_executed",
    "file_write_performed",
    "external_network_required_for_this_lesson",
    "persistent_storage_created",
    "approved_for_live_release",
}

REQUIRED_SCOPE = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_phase8_visibility_and_access_contracts",
    "local_simulation_only",
    "delivery_contract_only",
    "no_live_ci_runtime",
    "no_live_container_build",
    "no_live_registry_push",
    "no_live_signature_action",
    "no_live_cluster_deploy",
    "no_live_traffic_shift",
    "no_live_feature_flag_change",
    "no_live_model_change",
    "no_network_call",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "source_revision_required",
    "branch_policy_required",
    "workflow_permissions_required",
    "dependency_review_required",
    "unit_tests_required",
    "integration_tests_required",
    "policy_tests_required",
    "security_scan_required",
    "artifact_digest_required",
    "build_provenance_required",
    "image_signature_required",
    "signature_verification_required",
    "release_gate_required",
    "environment_approval_required",
    "rollout_strategy_required",
    "health_check_required",
    "rollback_plan_required",
    "model_rollout_control_required",
    "feature_flag_control_required",
    "access_policy_regression_required",
    "dashboard_visibility_regression_required",
    "release_evidence_required",
    "primary_aois_separation_required",
    "resource_usage_record_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "change_id",
    "source_revision",
    "branch_status",
    "workflow_permissions",
    "dependency_review",
    "test_status",
    "policy_test_status",
    "security_scan_status",
    "artifact_digest",
    "provenance_status",
    "signature_status",
    "environment_approval",
    "rollout_strategy",
    "health_status",
    "rollback_ready",
    "model_rollout_status",
    "feature_flag_status",
    "release_decision",
    "operator_action",
    "release_evidence",
}

REQUIRED_STAGES = {
    "source_control",
    "build_test",
    "package_attest",
    "release_gate",
    "rollout_control",
}

REQUIRED_DECISIONS = {
    "allow_release_candidate",
    "block_unreviewed_branch",
    "block_workflow_overprivileged",
    "block_dependency_review_failed",
    "block_tests_failed",
    "block_policy_tests_failed",
    "block_security_scan_failed",
    "block_missing_digest",
    "block_missing_provenance",
    "block_unsigned_artifact",
    "block_signature_unverified",
    "block_missing_environment_approval",
    "hold_rollout_health",
    "block_no_rollback",
    "hold_model_rollout",
    "hold_feature_flag",
}

REQUIRED_SOURCES = {
    "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax",
    "https://slsa.dev/spec/v1.2/",
    "https://docs.sigstore.dev/cosign/signing/overview/",
    "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/",
    "https://openfeature.dev/specification/",
}

REQUIRED_LIVE_CHECKS = {
    "workflow_yaml_review",
    "workflow_permission_review",
    "branch_protection_review",
    "dependency_review_configuration",
    "test_matrix_review",
    "policy_regression_review",
    "security_scan_review",
    "provenance_attestation_review",
    "signature_identity_review",
    "signature_verification_review",
    "environment_approval_review",
    "rollout_strategy_review",
    "health_gate_review",
    "rollback_drill",
    "model_rollout_review",
    "feature_flag_review",
    "primary_aois_separation_review",
    "resource_usage_record",
}

REQUIRED_DEFAULTS = {
    "branch_status": "reviewed",
    "workflow_permissions": "least_privilege",
    "dependency_review": "pass",
    "test_status": "pass",
    "policy_test_status": "pass",
    "security_scan_status": "pass",
    "provenance_status": "present",
    "signature_status": "verified",
    "environment_approval": "approved",
    "rollout_strategy": "canary",
    "health_status": "healthy",
    "rollback_ready": True,
    "model_rollout_status": "staged",
    "feature_flag_status": "guarded",
    "release_evidence": "complete",
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


def _require_pipeline(plan: dict[str, object], missing: list[str]) -> None:
    stages = plan.get("pipeline_stages", [])
    observed: set[str] = set()
    if not isinstance(stages, list) or len(stages) < len(REQUIRED_STAGES):
        missing.append("complete_pipeline_stage_catalog_required")
        return
    for stage in stages:
        if not isinstance(stage, dict):
            missing.append("pipeline_stage_must_be_object")
            continue
        stage_id = stage.get("stage_id")
        if isinstance(stage_id, str):
            observed.add(stage_id)
        for field in ["stage_id", "description", "required_inputs", "blocks_on_failure"]:
            if field not in stage:
                missing.append(f"pipeline_stage_missing_field:{field}")
        if stage.get("blocks_on_failure") is not True:
            missing.append(f"pipeline_stage_must_block_on_failure:{stage_id}")
        if not isinstance(stage.get("required_inputs"), list) or not stage["required_inputs"]:
            missing.append(f"pipeline_stage_required_inputs_missing:{stage_id}")

    for stage_id in sorted(REQUIRED_STAGES):
        if stage_id not in observed:
            missing.append(f"missing_pipeline_stage:{stage_id}")


def _require_defaults(defaults: object, missing: list[str]) -> None:
    if not isinstance(defaults, dict):
        missing.append("case_defaults_must_be_object")
        return
    for field, expected in REQUIRED_DEFAULTS.items():
        if defaults.get(field) != expected:
            missing.append(f"case_default_mismatch:{field}")
    digest = defaults.get("artifact_digest")
    if not isinstance(digest, str) or not digest.startswith("sha256:"):
        missing.append("case_default_artifact_digest_must_be_sha256")


def _require_cases(plan: dict[str, object], missing: list[str]) -> None:
    cases = plan.get("release_cases", [])
    observed_decisions: set[str] = set()
    required_case_fields = {
        "case_id",
        "name",
        "expected_decision",
        "expected_operator_action",
        "expected_release_state",
    }
    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("release_case_for_each_decision_required")
        return

    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            missing.append("release_case_must_be_object")
            continue
        case_id = str(case.get("case_id", ""))
        if not case_id:
            missing.append("release_case_id_required")
        elif case_id in case_ids:
            missing.append(f"duplicate_release_case_id:{case_id}")
        case_ids.add(case_id)

        for field in sorted(required_case_fields):
            if field not in case:
                missing.append(f"release_case_missing_field:{case_id}:{field}")
        decision = case.get("expected_decision")
        if isinstance(decision, str):
            observed_decisions.add(decision)
        if decision not in REQUIRED_DECISIONS:
            missing.append(f"unexpected_expected_decision:{case_id}:{decision}")
        if "overrides" in case and not isinstance(case["overrides"], dict):
            missing.append(f"release_case_overrides_must_be_object:{case_id}")

    for decision in sorted(REQUIRED_DECISIONS):
        if decision not in observed_decisions:
            missing.append(f"missing_release_case_for_decision:{decision}")


def validate_delivery_release_controls_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "delivery_release_controls_plan_no_runtime":
        missing.append("mode_must_be_delivery_release_controls_plan_no_runtime")
    if plan.get("version") != "v28":
        missing.append("version_must_be_v28")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("release_scope"), REQUIRED_SCOPE, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("release_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_release_dimension:{dimension}")

    decision_gates = plan.get("decision_gates", {})
    if not isinstance(decision_gates, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if not decision_gates.get(decision):
                missing.append(f"missing_decision_gate:{decision}")

    _require_pipeline(plan, missing)
    _require_defaults(plan.get("case_defaults"), missing)
    _require_cases(plan, missing)

    live_checks = set(plan.get("required_before_live_release", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_release_check:{check}")

    return {
        "plan": str(PLAN_PATH),
        "mode": plan.get("mode"),
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_delivery_release_controls_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
