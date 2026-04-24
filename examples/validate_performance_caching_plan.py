#!/usr/bin/env python3
"""Validate Phase 5 v14.5 performance caching plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/performance-caching.plan.json")

REQUIRED_LAYERS = {
    "no-cache-baseline",
    "prompt-cache-placeholder",
    "prefix-reuse-placeholder",
    "response-cache-placeholder",
}

REQUIRED_CACHE_POLICY = {
    "cache_key_design_required",
    "ttl_required",
    "invalidation_required",
    "privacy_boundary_required",
    "freshness_policy_required",
    "tenant_isolation_required",
    "hit_rate_measurement_required",
    "cost_savings_measurement_required",
}

REQUIRED_BATCHING = {
    "batch_size_review_required",
    "tail_latency_review_required",
    "throughput_review_required",
    "quality_regression_review_required",
}

REQUIRED_CONTROLS = {
    "redis_live_install_disallowed",
    "cache_state_live_write_disallowed",
    "fallback_route_required",
    "observability_required",
    "rollback_plan_required",
    "resource_usage_record_required",
    "primary_aois_separation_required",
}

REQUIRED_LIVE_CHECKS = {
    "cache_backend_approval",
    "redis_or_cache_service_plan",
    "cache_key_review",
    "ttl_and_invalidation_review",
    "privacy_boundary_review",
    "tenant_isolation_review",
    "hit_rate_baseline",
    "cost_savings_baseline",
    "fallback_route_plan",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_performance_caching_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "performance_caching_plan_no_runtime":
        missing.append("mode_must_be_no_runtime")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    for field in [
        "cache_service_started",
        "redis_installed",
        "cache_entries_created",
        "inference_runtime_started",
        "external_network_required_for_this_lesson",
        "approved_for_live_caching",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    layers = plan.get("cache_layers", [])
    if not isinstance(layers, list) or len(layers) < 4:
        missing.append("cache_layers_must_include_four_layers")
    else:
        names = {layer.get("name") for layer in layers if isinstance(layer, dict)}
        for name in sorted(REQUIRED_LAYERS):
            if name not in names:
                missing.append(f"missing_cache_layer:{name}")
        for layer in layers:
            if not isinstance(layer, dict):
                continue
            if layer.get("live_use_approved") is not False:
                missing.append(f"cache_layer_live_use_must_be_false:{layer.get('name')}")
            hit_rate = layer.get("simulated_hit_rate")
            if not isinstance(hit_rate, (float, int)) or not 0 <= hit_rate <= 1:
                missing.append(f"hit_rate_out_of_range:{layer.get('name')}")

    cache_policy = plan.get("cache_policy", {})
    if not isinstance(cache_policy, dict):
        missing.append("cache_policy_must_be_object")
    else:
        for field in sorted(REQUIRED_CACHE_POLICY):
            if cache_policy.get(field) is not True:
                missing.append(f"missing_cache_policy:{field}")

    batching = plan.get("batching_tradeoffs", {})
    if not isinstance(batching, dict):
        missing.append("batching_tradeoffs_must_be_object")
    else:
        for field in sorted(REQUIRED_BATCHING):
            if batching.get(field) is not True:
                missing.append(f"missing_batching_control:{field}")

    controls = plan.get("controls", {})
    if not isinstance(controls, dict):
        missing.append("controls_must_be_object")
    else:
        for field in sorted(REQUIRED_CONTROLS):
            if controls.get(field) is not True:
                missing.append(f"missing_control:{field}")

    live_checks = set(plan.get("required_before_live_caching", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "performance_caching_validation_no_runtime",
        "cache_service_started": False,
        "redis_installed": False,
        "cache_entries_created": False,
        "inference_runtime_started": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_performance_caching_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
