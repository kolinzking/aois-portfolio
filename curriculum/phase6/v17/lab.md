# v17 Lab

Authoring status: authored

## Build Lab

Compile and run the local-only event streaming validator and simulator:

```bash
python3 -m py_compile examples/validate_event_streaming_plan.py examples/simulate_event_streaming.py
python3 examples/validate_event_streaming_plan.py
python3 examples/simulate_event_streaming.py
```

Expected validator result:

- `stream_runtime_started: false`
- `broker_started: false`
- `producer_started: false`
- `consumer_started: false`
- `status: pass`

Expected simulator result:

- Four local incident events are produced as data in memory only.
- Consumed offsets are `[0, 1, 2, 3]`.
- Lag is `0`.
- Replay from offset `1` returns `evt-002`, `evt-003`, and `evt-004`.
- Dead-letter events are empty.

## Ops Lab

Answer these before touching any runtime:

1. What is the stream name and why does it use the `aois-p` prefix?
2. What topic carries incident events?
3. Why is `incident_id` the partition key?
4. Which fields are required on every event?
5. What does the consumer need to store so replay can resume safely?
6. What metric tells you consumers are falling behind?
7. Why is a dead-letter stream safer than endlessly retrying a poison event?
8. What resource budgets must exist before a real broker is approved?

## Break Lab

Use a temporary copy or a reversible local edit. Do not commit the broken plan.

Break 1: set `broker_started` to `true`.

Expected result: the validator fails because v17 is non-runtime by design.

Break 2: remove `offset_tracking` from the consumer controls.

Expected result: the validator fails because a consumer that cannot track
offsets cannot replay or resume safely.

Break 3: disable `dead_letter_stream`.

Expected result: the validator fails because poison events need isolation.

After each break, restore the plan and rerun the validator until it passes.

## Explanation Lab

Explain the design in this order:

1. A producer emits an event with a schema version and idempotency key.
2. The broker persists the event and assigns an offset.
3. A consumer reads from its last committed offset.
4. If processing succeeds, the consumer advances its offset.
5. If processing repeatedly fails, the event moves to a dead-letter stream.
6. Operators inspect lag, replay from known offsets, and fix contract mistakes.

Then explain why this lesson simulates the model instead of starting Kafka.

## Defense Lab

Defend these decisions:

1. No broker is started in v17 because the shared server has constrained memory
   and the curriculum can teach the core model without persistent runtime cost.
2. The plan requires schema validation because AI event payloads can drift as
   prompts, tools, and agent workflows change.
3. Consumers must be idempotent because replay can deliver an event more than
   once.
4. Dead-letter streams are required because one malformed event must not block
   the whole incident pipeline.
5. A live deployment is not approved until retention, lag dashboards, storage
   budget, rollback, and primary-project separation are all documented.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17 - Event Streaming Without Broker Runtime](notes.md)
- Next: [v17 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
