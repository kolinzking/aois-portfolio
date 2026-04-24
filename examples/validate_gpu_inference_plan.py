#!/usr/bin/env python3
"""Validate Phase 5 v13 GPU inference service plan without GPU runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/gpu-inference-service.plan.json")

REQUIRED_REQUEST_FIELDS = {
    "trace_id",
    "model_route",
    "prompt",
    "max_tokens",
    "temperature",
}

REQUIRED_RESPONSE_FIELDS = {
    "trace_id",
    "model_route",
    "output",
    "latency_ms",
    "tokens_in",
    "tokens_out",
    "backend_metadata",
}

REQUIRED_CONTROLS = {
    "model_license_review_required",
    "model_size_review_required",
    "cost_gate_required",
    "memory_budget_required",
    "latency_measurement_required",
    "throughput_measurement_required",
    "fallback_route_required",
    "observability_required",
    "resource_usage_record_required",
    "primary_aois_separation_required",
}

REQUIRED_LIVE_CHECKS = {
    "gpu_hardware_or_cloud_approval",
    "driver_and_cuda_plan",
    "container_image_plan",
    "model_license_review",
    "model_download_approval",
    "memory_budget",
    "cost_budget",
    "observability_plan",
    "fallback_route_plan",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_gpu_inference_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "gpu_inference_service_plan_no_runtime":
        missing.append("mode_must_be_no_runtime")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("gpu_runtime_started") is not False:
        missing.append("gpu_runtime_started_must_be_false")
    if plan.get("gpu_required_for_this_lesson") is not False:
        missing.append("gpu_required_for_this_lesson_must_be_false")
    if plan.get("model_downloaded") is not False:
        missing.append("model_downloaded_must_be_false")
    if plan.get("external_network_required_for_this_lesson") is not False:
        missing.append("network_must_not_be_required")
    if plan.get("approved_for_live_gpu") is not False:
        missing.append("live_gpu_must_not_be_approved")

    service = plan.get("service", {})
    if not isinstance(service, dict):
        missing.append("service_must_be_object")
    else:
        name = service.get("name")
        if not isinstance(name, str) or not name.startswith("aois-p-"):
            missing.append("service_name_must_use_aois_p_prefix")
        request_fields = set(service.get("request_contract", []))
        response_fields = set(service.get("response_contract", []))
        for field in sorted(REQUIRED_REQUEST_FIELDS):
            if field not in request_fields:
                missing.append(f"missing_request_field:{field}")
        for field in sorted(REQUIRED_RESPONSE_FIELDS):
            if field not in response_fields:
                missing.append(f"missing_response_field:{field}")

    serving_options = plan.get("serving_options", [])
    if not isinstance(serving_options, list) or len(serving_options) < 3:
        missing.append("serving_options_must_include_three_paths")
    else:
        names = {option.get("name") for option in serving_options if isinstance(option, dict)}
        for name in ["nvidia-nim-placeholder", "triton-style-placeholder", "vllm-placeholder"]:
            if name not in names:
                missing.append(f"missing_serving_option:{name}")
        for option in serving_options:
            if isinstance(option, dict) and option.get("live_use_approved") is not False:
                missing.append(f"serving_option_live_use_must_be_false:{option.get('name')}")

    perf = plan.get("performance_budget", {})
    if not isinstance(perf, dict):
        missing.append("performance_budget_must_be_object")
    else:
        if perf.get("max_concurrent_requests_for_lesson") != 0:
            missing.append("max_concurrent_requests_for_lesson_must_be_zero")
        for field in ["target_p50_latency_ms", "target_p95_latency_ms", "target_tokens_per_second"]:
            value = perf.get(field)
            if not isinstance(value, int) or value <= 0:
                missing.append(f"performance_target_must_be_positive:{field}")

    gpu = plan.get("gpu_capacity_plan", {})
    if not isinstance(gpu, dict):
        missing.append("gpu_capacity_plan_must_be_object")
    else:
        for field in ["gpu_count", "gpu_memory_gb"]:
            if gpu.get(field) != 0:
                missing.append(f"{field}_must_be_zero")
        for field in [
            "cuda_required_for_this_lesson",
            "driver_install_required_for_this_lesson",
            "container_image_built",
        ]:
            if gpu.get(field) is not False:
                missing.append(f"{field}_must_be_false")

    controls = plan.get("controls", {})
    if not isinstance(controls, dict):
        missing.append("controls_must_be_object")
    else:
        for control in sorted(REQUIRED_CONTROLS):
            if controls.get(control) is not True:
                missing.append(f"missing_control:{control}")

    live_checks = set(plan.get("required_before_live_gpu", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "gpu_inference_plan_validation_no_runtime",
        "gpu_runtime_started": False,
        "gpu_required_for_this_lesson": False,
        "model_downloaded": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_gpu_inference_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
