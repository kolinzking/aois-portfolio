# v17 Contents

Authoring status: authored

Topic: Event streaming for AI infrastructure control planes

Safety mode: local plan and simulation only. This version does not start Kafka,
Redis Streams, NATS, producers, consumers, containers, cloud services, or
persistent runtime storage.

## Start Here

1. Read [02-introduction.md](02-introduction.md) to understand why event streaming
   exists in AOIS before any broker is deployed.
2. Read [03-notes.md](03-notes.md) for the full model: producers, consumers, event
   contracts, offsets, lag, replay, durability, and dead-letter streams.
3. Inspect `streaming/aois-p/event-streaming.plan.json` as the source of truth
   for the proposed `aois-p` streaming design.
4. Run the validator and simulator locally:

```bash
python3 -m py_compile examples/validate_event_streaming_plan.py examples/simulate_event_streaming.py
python3 examples/validate_event_streaming_plan.py
python3 examples/simulate_event_streaming.py
```

Expected result: both scripts report `status: pass` while every runtime flag
remains false.

## Topic Jumps

- Event contract: [03-notes.md](03-notes.md)
- Producer and consumer responsibilities: [03-notes.md](03-notes.md)
- Offset, lag, and replay discipline: [04-lab.md](04-lab.md)
- Safe recovery procedure: [05-runbook.md](05-runbook.md)
- Measurement checklist: [07-benchmark.md](07-benchmark.md)
- Failure mode: [06-failure-story.md](06-failure-story.md)
- Transition to service and agent SLOs: [10-next-version-bridge.md](10-next-version-bridge.md)

## Self-Paced Path

1. Explain what problem a stream solves that a direct HTTP call does not solve.
2. Identify the event topic, partition key, required event fields, and event
   types in the plan.
3. Run the validator and confirm no live broker, producer, or consumer is
   started.
4. Run the simulator and trace the four local events from offset 0 to offset 3.
5. Explain why replay starts from an offset and why consumers must be
   idempotent.
6. Break the plan intentionally in a copy or temporary edit, then use the
   validator output to explain what made the design unsafe.
7. Answer the mastery questions in [03-notes.md](03-notes.md) before moving to v17.5.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17 Start Here](00-start-here.md)
- Next: [v17 Introduction](02-introduction.md)
<!-- AOIS-NAV-END -->
