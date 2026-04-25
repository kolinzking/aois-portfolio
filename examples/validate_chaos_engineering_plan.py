#!/usr/bin/env python3
"""Validate Phase 6 v19 chaos engineering plan without fault injection."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("chaos/aois-p/chaos-engineering.plan.json")

REQUIRED_EXPERIMENTS = {
    "aois-p-api-latency-game-day",
    "aois-p-stream-lag-game-day",
    "aois-p-agent-bad-recommendation-game-day",
}

REQUIRED_PRINCIPLES = {
    "steady_state_required",
    "hypothesis_required",
    "blast_radius_required",
    "abort_condition_required",
    "rollback_required",
    "observer_required",
    "communication_required",
    "primary_aois_protection_required",
}

REQUIRED_GAME_DAY_POLICY = {
    "owner_required",
    "observer_required",
    "scribe_required",
    "pre_brief_required",
    "post_review_required",
    "abort_word_required",
    "timebox_required",
    "primary_project_exclusion_required",
}

REQUIRED_SAFETY_CONTROLS = {
    "no_live_faults_in_this_lesson",
    "no_primary_aois_targeting",
    "no_destructive_actions",
    "no_unbounded_load",
    "no_cloud_resource_mutation",
    "no_secret_access",
    "human_approval_required_before_live_chaos",
    "resource_usage_record_required",
}

REQUIRED_LIVE_CHECKS = {
    "production_service_inventory",
    "primary_aois_exclusion_review",
    "steady_state_metric_review",
    "slo_error_budget_review",
    "blast_radius_approval",
    "abort_condition_approval",
    "rollback_runbook",
    "incident_commander_assigned",
    "communications_plan",
    "resource_limit_review",
    "agent_safety_policy",
    "post_game_day_review_template",
}


def _require_true_fields(section: object, required: set[str], label: str, missing: list[str]) -> None:
    if not isinstance(section, dict):
        missing.append(f"{label}_must_be_object")
        return
    for field in sorted(required):
        if section.get(field) is not True:
            missing.append(f"missing_{label}:{field}")


def validate_chaos_engineering_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "chaos_engineering_plan_no_fault_injection":
        missing.append("mode_must_be_no_fault_injection")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")

    for field in [
        "chaos_runtime_started",
        "fault_injection_executed",
        "load_test_started",
        "network_fault_started",
        "cpu_stress_started",
        "memory_stress_started",
        "pod_delete_executed",
        "agent_runtime_started",
        "provider_call_made",
        "external_network_required_for_this_lesson",
        "approved_for_live_chaos",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    _require_true_fields(plan.get("principles"), REQUIRED_PRINCIPLES, "principle", missing)
    _require_true_fields(plan.get("game_day_policy"), REQUIRED_GAME_DAY_POLICY, "game_day_policy", missing)
    _require_true_fields(plan.get("safety_controls"), REQUIRED_SAFETY_CONTROLS, "safety_control", missing)

    experiments = plan.get("experiments", [])
    if not isinstance(experiments, list):
        missing.append("experiments_must_be_list")
        experiment_names: set[str] = set()
    else:
        experiment_names = set()
        for item in experiments:
            if not isinstance(item, dict):
                missing.append("experiment_entry_must_be_object")
                continue
            name = item.get("name")
            if isinstance(name, str):
                experiment_names.add(name)
            if not isinstance(name, str) or not name.startswith("aois-p-"):
                missing.append("experiment_name_must_use_aois_p_prefix")
            for field in [
                "target",
                "failure_mode",
                "hypothesis",
                "steady_state",
                "blast_radius",
                "abort_condition",
                "rollback",
                "slo_guardrail",
                "agent_guardrail",
            ]:
                if not isinstance(item.get(field), str) or not item[field]:
                    missing.append(f"experiment_missing_field:{field}:{name}")
            if item.get("approved_for_live_execution") is not False:
                missing.append(f"experiment_must_not_be_live:{name}")
    for experiment in sorted(REQUIRED_EXPERIMENTS):
        if experiment not in experiment_names:
            missing.append(f"missing_experiment:{experiment}")

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in [
            "max_fault_injections_for_lesson",
            "max_load_tests_for_lesson",
            "max_network_faults_for_lesson",
            "max_cpu_stressors_for_lesson",
            "max_memory_stressors_for_lesson",
            "max_pod_deletes_for_lesson",
            "max_agent_runs_for_lesson",
            "max_provider_calls_for_lesson",
            "max_persistent_storage_mb",
            "max_spend_usd",
        ]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    live_checks = set(plan.get("required_before_live_chaos", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "chaos_engineering_validation_no_fault_injection",
        "chaos_runtime_started": False,
        "fault_injection_executed": False,
        "load_test_started": False,
        "network_fault_started": False,
        "cpu_stress_started": False,
        "memory_stress_started": False,
        "pod_delete_executed": False,
        "agent_runtime_started": False,
        "provider_call_made": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_chaos_engineering_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
