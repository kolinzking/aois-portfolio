# v17 - Event Streaming Without Broker Runtime

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: streaming plan and simulation only, no Kafka, no Redis Streams, no NATS, no broker, no producer/consumer runtime

## What This Builds

This version builds an event streaming plan:

- `streaming/aois-p/event-streaming.plan.json`
- `examples/validate_event_streaming_plan.py`
- `examples/simulate_event_streaming.py`

It teaches:

- event streams
- producers
- consumers
- event contracts
- offsets
- lag
- durability
- replay
- dead-letter streams
- why streaming changes architecture

## Why This Exists

AOIS now has traces for incident steps.

The next architectural move is durable movement of incident and telemetry events.

Streaming lets AOIS decouple event production from event consumption, but it introduces new responsibilities:

- schemas
- offsets
- replay
- lag
- retention
- poison events
- idempotent processing
- dead-letter streams

## AOIS Connection

The AOIS path is now:

`incident tracing -> event streaming -> SLOs and reliability`

`v17` does not start a broker. It teaches the event model before runtime systems exist.

## Learning Goals

By the end of this version you should be able to:

- explain event streams
- explain producer and consumer roles
- explain event contracts and schema versions
- explain offsets and replay
- explain lag
- explain dead-letter streams
- explain why idempotency matters
- validate a streaming plan locally
- run a local publish/consume/replay simulation

## Prerequisites

You should have completed:

- `v16` unified telemetry
- `v16.5` incident tracing

Required checks:

```bash
python3 -m py_compile examples/validate_event_streaming_plan.py examples/simulate_event_streaming.py
python3 examples/validate_event_streaming_plan.py
python3 examples/simulate_event_streaming.py
```

## Core Concepts

## Event Stream

An event stream is an ordered or partitioned sequence of events.

AOIS uses it to represent incident lifecycle events.

## Producer

A producer writes events to a stream.

It needs idempotency, retry policy, delivery acknowledgement, and schema validation.

## Consumer

A consumer reads events from a stream.

It needs offset tracking, lag measurement, idempotent processing, and replay discipline.

## Offset

An offset identifies a position in a stream.

Replay starts from an offset.

## Lag

Lag is how far a consumer is behind the stream.

Lag can indicate slow processing, overload, or broken consumers.

## Dead-Letter Stream

A dead-letter stream stores events that cannot be processed safely.

It prevents poison events from blocking the main stream forever.

## Replay

Replay means processing older events again from a known position.

Replay requires idempotency.

## Build

Inspect:

```bash
sed -n '1,280p' streaming/aois-p/event-streaming.plan.json
sed -n '1,320p' examples/validate_event_streaming_plan.py
sed -n '1,260p' examples/simulate_event_streaming.py
```

Compile:

```bash
python3 -m py_compile examples/validate_event_streaming_plan.py examples/simulate_event_streaming.py
```

Validate:

```bash
python3 examples/validate_event_streaming_plan.py
```

Simulate:

```bash
python3 examples/simulate_event_streaming.py
```

Expected validation:

```json
{
  "stream_runtime_started": false,
  "broker_started": false,
  "producer_started": false,
  "consumer_started": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer from the plan and simulator:

1. Which topic is planned?
2. Which field proves no broker started?
3. Which field proves no producer started?
4. Which field proves no consumer started?
5. Which event type represents recommendation output?
6. Which offset does replay start from?
7. What is the simulated lag?

Answer key:

1. `aois-p.incident.events`
2. `broker_started=false`
3. `producer_started=false`
4. `consumer_started=false`
5. `incident.recommended`
6. `1`
7. `0`

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Start Broker Too Early

Set:

```json
"broker_started": true
```

Expected risk:

- a planning lesson can be mistaken for live broker deployment

### Option B - Remove Offset Tracking

Set:

```json
"offset_tracking_required": false
```

Expected risk:

- consumers cannot resume or replay safely

### Option C - Remove Dead-Letter Stream

Set:

```json
"dead_letter_stream_required": false
```

Expected risk:

- poison events can block or disappear without controlled handling

## Testing

The version passes when:

1. both scripts compile
2. validator returns `status=pass`
3. simulator returns `status=pass`
4. no broker starts
5. no producer starts
6. no consumer starts
7. event contract includes required fields
8. producer and consumer controls remain true
9. durability controls remain true
10. limits remain zero

## Common Mistakes

- treating streaming as just a queue
- ignoring schema versions
- missing idempotency
- ignoring consumer lag
- replaying events without safe processing
- omitting dead-letter stream
- starting Kafka or another broker before resource budget exists

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_event_streaming_plan.py
```

Read `missing`, inspect the plan, and restore required fields.

Common fixes:

- restore runtime flags to `false`
- restore `aois-p` names
- restore required event fields and event types
- restore producer controls
- restore consumer controls
- restore durability controls
- restore limits to zero
- restore live checks

## Benchmark

Measure:

- validator compile result
- validator status
- simulator status
- event count
- consumed offsets
- replay offset
- lag
- dead-letter event count
- repo disk footprint
- memory snapshot

## Architecture Defense

Why not start Kafka or another broker now?

Because streaming systems consume memory and disk and require retention, replay, schema, and operations design before live use.

Why require schema version?

Because event producers and consumers evolve independently.

Why require replay runbook?

Because replay can duplicate side effects if idempotency is missing.

## 4-Layer Tool Drill

Tool: event stream

1. Plain English
It is a durable line of events that consumers can read.

2. System Role
It decouples producers and consumers.

3. Minimal Technical Definition
It is an ordered or partitioned event log with offsets, retention, producers, and consumers.

4. Hands-on Proof
The simulator publishes four local events, consumes offsets, and replays from offset `1` without starting a broker.

## 4-Level System Explanation Drill

1. Simple English
AOIS plans event streaming without running a broker.

2. Practical Explanation
I can inspect event fields, producers, consumers, offsets, lag, DLQ, and replay.

3. Technical Explanation
`v17` adds an event streaming plan, validator, and local publish/consume/replay simulator.

4. Engineer-Level Explanation
AOIS now separates streaming design from broker deployment, requiring schema strategy, producer retries, consumer offsets, idempotent processing, dead-letter streams, retention, lag dashboards, replay runbooks, storage budget, rollback, and primary-project separation before live streaming.

## Failure Story

Representative failure:

- Symptom: a consumer crashes on one malformed event and stops processing future incidents
- Root cause: no dead-letter stream or poison-event policy existed
- Fix: route poison events to a DLQ, alert, and replay after correction
- Prevention: validate durability controls before live broker use
- What this taught me: streaming failure is often event-shape failure

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v17` solve in AOIS?
2. What is an event stream?
3. What is a producer?
4. What is a consumer?
5. What is an offset?
6. What is lag?
7. Why is schema version required?
8. Why is idempotency required?
9. Why is a dead-letter stream required?
10. Explain event stream using the 4-layer tool rule.
11. Explain `v17` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v17` solve in AOIS?

It defines how incident and telemetry events can move asynchronously before a broker is deployed.

2. What is an event stream?

A durable sequence of events that producers write and consumers read.

3. What is a producer?

A component that writes events to a stream.

4. What is a consumer?

A component that reads and processes events from a stream.

5. What is an offset?

A position in the stream.

6. What is lag?

How far a consumer is behind the latest available event.

7. Why is schema version required?

It lets producers and consumers evolve while preserving compatibility.

8. Why is idempotency required?

Replay and retries can process the same event more than once.

9. Why is a dead-letter stream required?

It isolates events that fail processing so the main stream can continue.

10. Explain event stream using the 4-layer tool rule.

- Plain English: it is a durable line of events.
- System Role: it decouples producers and consumers.
- Minimal Technical Definition: it is an event log with offsets, retention, producers, and consumers.
- Hands-on Proof: the simulator publishes, consumes, and replays events locally.

11. Explain `v17` using the 4-level system explanation rule.

- Simple English: AOIS plans event streaming without running a broker.
- Practical explanation: I can inspect events, offsets, lag, DLQ, and replay.
- Technical explanation: `v17` adds a streaming plan, validator, and simulator.
- Engineer-level explanation: AOIS gates broker deployment behind schema, retries, offsets, idempotency, DLQ, retention, lag dashboards, replay, storage budget, rollback, and primary separation.

## Connection Forward

`v17` defines the streaming path.

`v17.5` defines SLOs and error budgets for services, agents, cost, and quality.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17 Introduction](introduction.md)
- Next: [v17 Lab](lab.md)
<!-- AOIS-NAV-END -->
