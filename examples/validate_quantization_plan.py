#!/usr/bin/env python3
"""Validate Phase 5 v15.5 quantization plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/quantization-memory.plan.json")

REQUIRED_OPTIONS = {"fp16-baseline", "int8-placeholder", "int4-placeholder"}

REQUIRED_CONTROLS = {
    "quality_eval_required",
    "memory_measurement_required",
    "latency_measurement_required",
    "throughput_measurement_required",
    "calibration_data_review_required",
    "task_regression_eval_required",
    "fallback_precision_required",
    "rollback_plan_required",
    "resource_usage_record_required",
    "primary_aois_separation_required",
}

REQUIRED_LIVE_CHECKS = {
    "model_artifact_approval",
    "quantization_method_review",
    "calibration_data_review",
    "quality_eval_baseline",
    "task_regression_eval",
    "memory_benchmark",
    "latency_benchmark",
    "fallback_precision_plan",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_quantization_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "quantization_memory_plan_no_runtime":
        missing.append("mode_must_be_no_runtime")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    for field in [
        "quantization_job_started",
        "model_downloaded",
        "gpu_runtime_started",
        "inference_runtime_started",
        "external_network_required_for_this_lesson",
        "approved_for_live_quantization",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    options = plan.get("precision_options", [])
    if not isinstance(options, list) or len(options) < 3:
        missing.append("precision_options_must_include_three_paths")
    else:
        names = {option.get("name") for option in options if isinstance(option, dict)}
        for name in sorted(REQUIRED_OPTIONS):
            if name not in names:
                missing.append(f"missing_precision_option:{name}")
        for option in options:
            if not isinstance(option, dict):
                continue
            if option.get("live_use_approved") is not False:
                missing.append(f"precision_option_live_use_must_be_false:{option.get('name')}")
            for field in ["weight_bits", "simulated_memory_gb", "simulated_speed_index", "simulated_quality_score"]:
                value = option.get(field)
                if not isinstance(value, (float, int)) or value <= 0:
                    missing.append(f"precision_field_must_be_positive:{option.get('name')}:{field}")

    controls = plan.get("controls", {})
    if not isinstance(controls, dict):
        missing.append("controls_must_be_object")
    else:
        for control in sorted(REQUIRED_CONTROLS):
            if controls.get(control) is not True:
                missing.append(f"missing_control:{control}")

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in ["max_quantization_jobs_for_lesson", "max_model_artifact_mb", "max_spend_usd"]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    live_checks = set(plan.get("required_before_live_quantization", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "quantization_plan_validation_no_runtime",
        "quantization_job_started": False,
        "model_downloaded": False,
        "gpu_runtime_started": False,
        "inference_runtime_started": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_quantization_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
