# v17 Runbook

Authoring status: authored

## Purpose

This runbook restores the v17 event streaming lesson to its safe local-only
state. It is used when the validator fails or when a learner accidentally turns
the design into a runtime deployment plan.

## Primary Checks

Check the event streaming plan:

```bash
python3 examples/validate_event_streaming_plan.py
```

The safe state is:

- `stream_runtime_started` is `false`.
- `broker_started` is `false`.
- `kafka_started` is `false`.
- `redis_stream_started` is `false`.
- `nats_started` is `false`.
- `producer_started` is `false`.
- `consumer_started` is `false`.
- All runtime limits are `0`.
- The stream name begins with `aois-p-`.
- The topic begins with `aois-p.`.
- Required event fields, producer controls, consumer controls, and durability
  controls are present.

## Recovery Steps

1. Restore all runtime flags to `false`.
2. Restore the required event fields: `event_id`, `event_type`,
   `schema_version`, `trace_id`, `incident_id`, `producer`, `created_at`, and
   `payload`.
3. Restore the producer controls: idempotency key, delivery acknowledgement,
   retry policy, and schema validation.
4. Restore the consumer controls: offset tracking, lag measurement,
   idempotent processing, dead-letter stream, and replay runbook.
5. Restore durability controls: retention policy, dead-letter stream, replay
   policy, schema compatibility, backpressure policy, and poison-event policy.
6. Keep runtime limits at zero until a live broker is explicitly approved.
7. Rerun the validator and simulator.

If a real broker was started outside this lesson, stop it only after confirming
it is not part of the primary AOIS project. This curriculum must not interfere
with the primary server workload.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17 Lab](lab.md)
- Next: [v17 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
