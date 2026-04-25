#!/usr/bin/env python3
"""Simulate Phase 6 v17 event streaming without broker runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("streaming/aois-p/event-streaming.plan.json")


def simulate_event_streaming() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    trace_id = "trace-v17-local-sim"
    incident_id = "incident-v17-local-sim"

    events = [
        {
            "event_id": "evt-001",
            "event_type": "incident.received",
            "schema_version": "v1",
            "trace_id": trace_id,
            "incident_id": incident_id,
            "producer": "aois-p-incident-producer-placeholder",
            "created_at": "2026-04-25T00:00:00Z",
            "offset": 0,
            "payload": {"summary": "raw incident received"},
        },
        {
            "event_id": "evt-002",
            "event_type": "incident.classified",
            "schema_version": "v1",
            "trace_id": trace_id,
            "incident_id": incident_id,
            "producer": "aois-p-incident-producer-placeholder",
            "created_at": "2026-04-25T00:00:01Z",
            "offset": 1,
            "payload": {"category": "memory-pressure", "severity": "high"},
        },
        {
            "event_id": "evt-003",
            "event_type": "incident.routed",
            "schema_version": "v1",
            "trace_id": trace_id,
            "incident_id": incident_id,
            "producer": "aois-p-incident-producer-placeholder",
            "created_at": "2026-04-25T00:00:02Z",
            "offset": 2,
            "payload": {"route": "local-deterministic", "provider_call_made": False},
        },
        {
            "event_id": "evt-004",
            "event_type": "incident.recommended",
            "schema_version": "v1",
            "trace_id": trace_id,
            "incident_id": incident_id,
            "producer": "aois-p-incident-producer-placeholder",
            "created_at": "2026-04-25T00:00:03Z",
            "offset": 3,
            "payload": {"action": "inspect memory usage and limits"},
        },
    ]

    consumed_offsets = [event["offset"] for event in events]
    replay_from_offset = 1
    replayed = [event for event in events if event["offset"] >= replay_from_offset]

    return {
        "mode": "event_streaming_simulation_no_broker",
        "stream_runtime_started": False,
        "broker_started": False,
        "producer_started": False,
        "consumer_started": False,
        "topic": plan["stream"]["topic"],
        "published_events": events,
        "consumed_offsets": consumed_offsets,
        "lag": 0,
        "replay": {
            "from_offset": replay_from_offset,
            "event_ids": [event["event_id"] for event in replayed],
        },
        "dead_letter_events": [],
        "status": "pass",
    }


def main() -> int:
    print(json.dumps(simulate_event_streaming(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
