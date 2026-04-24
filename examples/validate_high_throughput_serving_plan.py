#!/usr/bin/env python3
"""Validate Phase 5 v14 high-throughput serving plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/high-throughput-serving.plan.json")

REQUIRED_MODES = {
    "serial-baseline",
    "continuous-batching-placeholder",
    "cache-aware-placeholder",
}

REQUIRED_CONTROLS = {
    "latency_budget_required",
    "throughput_budget_required",
    "token_budget_required",
    "batching_policy_required",
    "concurrency_limit_required",
    "cache_policy_required",
    "speculative_decoding_review_required",
    "fallback_route_required",
    "observability_required",
    "resource_usage_record_required",
}

REQUIRED_LIVE_CHECKS = {
    "gpu_or_cpu_capacity_approval",
    "model_download_approval",
    "serving_runtime_selection",
    "batching_policy_review",
    "concurrency_limit_review",
    "latency_slo_review",
    "throughput_slo_review",
    "cache_policy_review",
    "fallback_route_plan",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_high_throughput_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "high_throughput_serving_plan_no_runtime":
        missing.append("mode_must_be_no_runtime")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    for field in [
        "inference_runtime_started",
        "gpu_runtime_started",
        "model_downloaded",
        "container_image_built",
        "external_network_required_for_this_lesson",
        "approved_for_live_serving",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    service = plan.get("service", {})
    if not isinstance(service, dict):
        missing.append("service_must_be_object")
    else:
        for field in ["name", "scheduler"]:
            value = service.get(field)
            if not isinstance(value, str) or not value.startswith("aois-p-"):
                missing.append(f"service_field_must_use_aois_p_prefix:{field}")

    modes = plan.get("serving_modes", [])
    if not isinstance(modes, list) or len(modes) < 3:
        missing.append("serving_modes_must_include_three_modes")
    else:
        names = {mode.get("name") for mode in modes if isinstance(mode, dict)}
        for name in sorted(REQUIRED_MODES):
            if name not in names:
                missing.append(f"missing_serving_mode:{name}")
        for mode in modes:
            if not isinstance(mode, dict):
                continue
            if mode.get("live_use_approved") is not False:
                missing.append(f"serving_mode_live_use_must_be_false:{mode.get('name')}")
            for field in [
                "batch_size",
                "max_concurrency",
                "simulated_tokens_per_second",
                "simulated_p95_latency_ms",
            ]:
                value = mode.get(field)
                if not isinstance(value, int) or value <= 0:
                    missing.append(f"mode_field_must_be_positive:{mode.get('name')}:{field}")

    queue = plan.get("queue_policy", {})
    if not isinstance(queue, dict):
        missing.append("queue_policy_must_be_object")
    else:
        if queue.get("max_queue_depth_for_lesson") != 0:
            missing.append("max_queue_depth_for_lesson_must_be_zero")
        if queue.get("backpressure_required") is not True:
            missing.append("backpressure_required_must_be_true")
        if queue.get("shed_load_policy_required") is not True:
            missing.append("shed_load_policy_required_must_be_true")

    controls = plan.get("performance_controls", {})
    if not isinstance(controls, dict):
        missing.append("performance_controls_must_be_object")
    else:
        for control in sorted(REQUIRED_CONTROLS):
            if controls.get(control) is not True:
                missing.append(f"missing_control:{control}")

    live_checks = set(plan.get("required_before_live_serving", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "high_throughput_serving_validation_no_runtime",
        "inference_runtime_started": False,
        "gpu_runtime_started": False,
        "model_downloaded": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_high_throughput_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
