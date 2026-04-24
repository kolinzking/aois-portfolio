#!/usr/bin/env python3
"""Validate Phase 5 v13.5 GPU infrastructure plan without applying resources."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/gpu-infrastructure-operations.plan.json")

REQUIRED_COMPONENTS = {
    "gpu_operator",
    "device_plugin",
    "gpu_node_pool",
    "scheduler_policy",
    "metrics_exporter",
    "dashboard",
}

REQUIRED_OBSERVABILITY = {
    "gpu_utilization_required",
    "gpu_memory_required",
    "temperature_required",
    "power_required",
    "pod_to_gpu_mapping_required",
    "scheduling_events_required",
    "dashboard_required",
    "alerts_required",
}

REQUIRED_CONTROLS = {
    "driver_plan_required",
    "cuda_plan_required",
    "node_capacity_plan_required",
    "cost_gate_required",
    "rollback_plan_required",
    "resource_usage_record_required",
    "primary_aois_separation_required",
}

REQUIRED_LIVE_CHECKS = {
    "gpu_hardware_or_cloud_approval",
    "driver_and_cuda_plan",
    "gpu_operator_docs_review",
    "device_plugin_plan",
    "node_pool_budget",
    "scheduling_policy_review",
    "mig_strategy_review",
    "gpu_observability_plan",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_gpu_infrastructure_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "gpu_infrastructure_operations_plan_no_apply":
        missing.append("mode_must_be_no_apply")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    for field in [
        "kubectl_apply_ran",
        "gpu_operator_installed",
        "device_plugin_installed",
        "gpu_runtime_started",
        "gpu_required_for_this_lesson",
        "external_network_required_for_this_lesson",
        "approved_for_live_gpu_infra",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    components = plan.get("components", {})
    if not isinstance(components, dict):
        missing.append("components_must_be_object")
    else:
        for field in sorted(REQUIRED_COMPONENTS):
            value = components.get(field)
            if not isinstance(value, str) or not value.startswith("aois-p-"):
                missing.append(f"component_must_use_aois_p_prefix:{field}")

    scheduling = plan.get("scheduling", {})
    if not isinstance(scheduling, dict):
        missing.append("scheduling_must_be_object")
    else:
        if scheduling.get("gpu_resource_name") != "nvidia.com/gpu":
            missing.append("gpu_resource_name_must_be_nvidia_com_gpu")
        if scheduling.get("requested_gpus_for_lesson") != 0:
            missing.append("requested_gpus_for_lesson_must_be_zero")
        for field in [
            "node_selector_required",
            "taint_toleration_required",
            "resource_limits_required",
            "priority_class_review_required",
        ]:
            if scheduling.get(field) is not True:
                missing.append(f"missing_scheduling_control:{field}")

    mig = plan.get("mig_awareness", {})
    if not isinstance(mig, dict):
        missing.append("mig_awareness_must_be_object")
    else:
        if mig.get("mig_configured") is not False:
            missing.append("mig_configured_must_be_false")
        if mig.get("mig_required_for_this_lesson") is not False:
            missing.append("mig_required_for_this_lesson_must_be_false")
        for field in ["mig_strategy_review_required", "profile_selection_required_before_live"]:
            if mig.get(field) is not True:
                missing.append(f"missing_mig_control:{field}")

    observability = plan.get("observability", {})
    if not isinstance(observability, dict):
        missing.append("observability_must_be_object")
    else:
        for field in sorted(REQUIRED_OBSERVABILITY):
            if observability.get(field) is not True:
                missing.append(f"missing_observability:{field}")

    controls = plan.get("controls", {})
    if not isinstance(controls, dict):
        missing.append("controls_must_be_object")
    else:
        for field in sorted(REQUIRED_CONTROLS):
            if controls.get(field) is not True:
                missing.append(f"missing_control:{field}")

    live_checks = set(plan.get("required_before_live_gpu_infra", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "gpu_infrastructure_plan_validation_no_apply",
        "kubectl_apply_ran": False,
        "gpu_operator_installed": False,
        "device_plugin_installed": False,
        "gpu_runtime_started": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_gpu_infrastructure_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
