#!/usr/bin/env python3
"""Simulate Phase 6 v16 unified telemetry output without telemetry runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("telemetry/aois-p/unified-telemetry.plan.json")


def simulate_telemetry() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    trace_id = "trace-v16-local-sim"
    request_id = "req-v16-local-sim"
    incident_id = "incident-v16-local-sim"
    route_id = "route-local-deterministic"

    spans = [
        {
            "name": "aois.request",
            "span_id": "span-root",
            "parent_span_id": None,
            "duration_ms": 42,
            "status": "ok",
        },
        {
            "name": "aois.security_inspect",
            "span_id": "span-security",
            "parent_span_id": "span-root",
            "duration_ms": 5,
            "status": "ok",
        },
        {
            "name": "aois.route_decision",
            "span_id": "span-route",
            "parent_span_id": "span-root",
            "duration_ms": 8,
            "status": "ok",
        },
        {
            "name": "aois.analysis",
            "span_id": "span-analysis",
            "parent_span_id": "span-root",
            "duration_ms": 18,
            "status": "ok",
        },
        {
            "name": "aois.response",
            "span_id": "span-response",
            "parent_span_id": "span-root",
            "duration_ms": 4,
            "status": "ok",
        },
    ]

    common = {
        "trace_id": trace_id,
        "request_id": request_id,
        "incident_id": incident_id,
        "route_id": route_id,
    }

    return {
        "mode": "unified_telemetry_simulation_no_runtime",
        "telemetry_runtime_started": False,
        "collector_started": False,
        "signals": {
            "traces": [{"trace_id": trace_id, "spans": spans}],
            "metrics": [
                {**common, "name": "aois_request_count", "value": 1},
                {**common, "name": "aois_request_latency_ms", "value": 42},
                {**common, "name": "aois_provider_call_count", "value": 0},
            ],
            "logs": [
                {
                    **common,
                    "span_id": "span-root",
                    "severity": "info",
                    "message": "local telemetry simulation completed",
                    "secret_redacted": True,
                }
            ],
        },
        "planned_components": plan["components"],
        "status": "pass",
    }


def main() -> int:
    print(json.dumps(simulate_telemetry(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
