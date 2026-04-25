#!/usr/bin/env python3
"""Simulate Phase 6 v16.5 incident trace output without agent runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("telemetry/aois-p/agent-incident-tracing.plan.json")


def simulate_agent_incident_trace() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    trace_id = "trace-v16-5-local-sim"
    incident_id = "incident-v16-5-local-sim"
    request_id = "req-v16-5-local-sim"
    agent_run_id = "agent-run-placeholder-none"
    route_id = "route-local-deterministic"

    steps = [
        {
            "step_id": "step-001",
            "parent_step_id": None,
            "name": "incident.ingest",
            "status": "ok",
            "duration_ms": 3,
            "input_summary": "raw incident signal received",
            "output_summary": "incident envelope created",
            "decision_reason": "preserve raw signal before enrichment",
        },
        {
            "step_id": "step-002",
            "parent_step_id": "step-001",
            "name": "incident.security_inspect",
            "status": "ok",
            "duration_ms": 5,
            "input_summary": "incident message inspected",
            "output_summary": "no secret-like content found",
            "decision_reason": "provider and tool execution remain disabled",
        },
        {
            "step_id": "step-003",
            "parent_step_id": "step-002",
            "name": "incident.classify",
            "status": "ok",
            "duration_ms": 11,
            "input_summary": "deterministic classification requested",
            "output_summary": "category=memory-pressure severity=high",
            "decision_reason": "message matched OOMKilled/exit 137 rule",
        },
        {
            "step_id": "step-004",
            "parent_step_id": "step-003",
            "name": "incident.route_decision",
            "status": "ok",
            "duration_ms": 6,
            "input_summary": "high-severity local route considered",
            "output_summary": "provider_call_made=false",
            "decision_reason": "no provider budget or approval exists",
        },
        {
            "step_id": "step-005",
            "parent_step_id": "step-004",
            "name": "incident.recommendation",
            "status": "ok",
            "duration_ms": 9,
            "input_summary": "classified incident converted to action",
            "output_summary": "inspect memory usage and limits",
            "decision_reason": "local deterministic recommendation path",
        },
        {
            "step_id": "step-006",
            "parent_step_id": "step-005",
            "name": "incident.response",
            "status": "ok",
            "duration_ms": 4,
            "input_summary": "response assembled",
            "output_summary": "structured response emitted",
            "decision_reason": "complete local trace simulation",
        },
    ]

    for step in steps:
        step.update(
            {
                "trace_id": trace_id,
                "incident_id": incident_id,
                "request_id": request_id,
                "agent_run_id": agent_run_id,
                "route_id": route_id,
                "tool_call_id": None,
                "secret_redacted": True,
            }
        )

    return {
        "mode": "agent_incident_trace_simulation_no_runtime",
        "telemetry_runtime_started": False,
        "agent_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "trace": {
            "trace_id": trace_id,
            "incident_id": incident_id,
            "request_id": request_id,
            "agent_run_id": agent_run_id,
            "root_trace": plan["trace_model"]["root_trace"],
            "steps": steps,
        },
        "step_metrics": [
            {
                "trace_id": trace_id,
                "incident_id": incident_id,
                "name": "aois_incident_trace_steps_total",
                "value": len(steps),
            },
            {
                "trace_id": trace_id,
                "incident_id": incident_id,
                "name": "aois_agent_tool_calls_total",
                "value": 0,
            },
        ],
        "status": "pass",
    }


def main() -> int:
    print(json.dumps(simulate_agent_incident_trace(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
