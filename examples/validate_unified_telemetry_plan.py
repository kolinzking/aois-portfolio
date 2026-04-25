#!/usr/bin/env python3
"""Validate Phase 6 v16 unified telemetry plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("telemetry/aois-p/unified-telemetry.plan.json")

REQUIRED_COMPONENTS = {
    "instrumentation",
    "collector",
    "metrics_backend",
    "logs_backend",
    "traces_backend",
    "dashboard",
}

REQUIRED_CORRELATION_FIELDS = {
    "trace_id",
    "span_id",
    "request_id",
    "incident_id",
    "route_id",
}

REQUIRED_CHILD_SPANS = {
    "aois.security_inspect",
    "aois.route_decision",
    "aois.analysis",
    "aois.response",
}

REQUIRED_CONTROLS = {
    "official_docs_review_required",
    "sampling_policy_required",
    "cardinality_budget_required",
    "retention_policy_required",
    "dashboard_required",
    "alert_policy_required",
    "resource_usage_record_required",
    "primary_aois_separation_required",
}

REQUIRED_LIVE_CHECKS = {
    "official_opentelemetry_docs_review",
    "instrumentation_design",
    "sampling_policy",
    "cardinality_budget",
    "retention_policy",
    "secret_redaction_test",
    "dashboard_plan",
    "alert_policy",
    "storage_budget",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_unified_telemetry_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "unified_telemetry_plan_no_runtime":
        missing.append("mode_must_be_no_runtime")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    for field in [
        "telemetry_runtime_started",
        "otel_sdk_installed",
        "collector_started",
        "prometheus_started",
        "loki_started",
        "tempo_started",
        "external_network_required_for_this_lesson",
        "approved_for_live_telemetry",
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

    signals = plan.get("signals", {})
    if not isinstance(signals, dict):
        missing.append("signals_must_be_object")
    else:
        for field in [
            "traces_required",
            "metrics_required",
            "logs_required",
            "correlation_required",
        ]:
            if signals.get(field) is not True:
                missing.append(f"missing_signal:{field}")

    correlation_fields = set(plan.get("correlation_fields", []))
    for field in sorted(REQUIRED_CORRELATION_FIELDS):
        if field not in correlation_fields:
            missing.append(f"missing_correlation_field:{field}")

    span_plan = plan.get("span_plan", {})
    if not isinstance(span_plan, dict):
        missing.append("span_plan_must_be_object")
    else:
        if span_plan.get("root_span") != "aois.request":
            missing.append("root_span_must_be_aois_request")
        child_spans = set(span_plan.get("child_spans", []))
        for span in sorted(REQUIRED_CHILD_SPANS):
            if span not in child_spans:
                missing.append(f"missing_child_span:{span}")
        for field in ["error_status_required", "duration_ms_required"]:
            if span_plan.get(field) is not True:
                missing.append(f"missing_span_control:{field}")

    metric_plan = plan.get("metric_plan", {})
    if not isinstance(metric_plan, dict):
        missing.append("metric_plan_must_be_object")
    else:
        for field, value in metric_plan.items():
            if value is not True:
                missing.append(f"missing_metric:{field}")

    log_plan = plan.get("log_plan", {})
    if not isinstance(log_plan, dict):
        missing.append("log_plan_must_be_object")
    else:
        for field, value in log_plan.items():
            if value is not True:
                missing.append(f"missing_log_control:{field}")

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
        for field in ["max_collectors_for_lesson", "max_backends_for_lesson", "max_persistent_storage_mb", "max_spend_usd"]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    live_checks = set(plan.get("required_before_live_telemetry", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "unified_telemetry_validation_no_runtime",
        "telemetry_runtime_started": False,
        "collector_started": False,
        "prometheus_started": False,
        "loki_started": False,
        "tempo_started": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_unified_telemetry_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
