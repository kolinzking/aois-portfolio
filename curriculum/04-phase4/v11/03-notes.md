# v11 - Event-Driven Workflow Planning Without Cloud Calls

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: event workflow plan and validation only, no cloud resources, no credentials, no provider calls

## What This Builds

This version builds an event-driven workflow plan:

- `cloud/aws/event-workflow.plan.json`
- `examples/validate_event_workflow_plan.py`

It teaches:

- event ingress
- event bus
- queue
- worker or serverless function
- dead-letter queue
- idempotency
- retry and timeout policy
- trace propagation
- why event-driven systems need stronger operational controls

## Why This Exists

AI infrastructure does not stay as one synchronous API forever.

Real systems need to handle:

- slow analysis
- bursty input
- retries
- partial failure
- background processing
- audit trails
- replay

Event-driven architecture lets AOIS decouple "request received" from "work completed."

But event-driven systems can also create duplicate work, hidden queues, runaway cost, and hard-to-debug failures if controls are missing.

## AOIS Connection

The AOIS path is now:

`managed model plan -> agent ownership decision -> event workflow plan -> serverless/queue option`

`v10` planned managed model use.
`v10.5` decided the agent loop remains AOIS-owned for now.
`v11` plans how AOIS work could move through events without creating cloud infrastructure.

## Learning Goals

By the end of this version you should be able to:

- explain event-driven workflow design
- explain why queues decouple API and worker load
- explain why idempotency is mandatory
- explain how retry and DLQ protect reliability
- explain why trace IDs must cross every hop
- validate a cloud event workflow plan locally
- explain why no cloud workflow is created yet

## Prerequisites

You should have completed:

- `v9` autoscaling and event-driven infrastructure planning
- `v10` managed model layer planning
- `v10.5` managed-agent tradeoff planning

Required checks:

```bash
python3 -m py_compile examples/validate_event_workflow_plan.py
python3 examples/validate_event_workflow_plan.py
```

## Core Concepts

## Event Ingress

Event ingress is the entry point that receives a request or signal and turns it into a workflow event.

Examples in real systems can include an API route, webhook receiver, scheduler, object-store notification, message bus, or manual operator action.

In this lesson, ingress is only a placeholder in a JSON plan.

## Event Bus

An event bus routes events between producers and consumers.

It helps systems avoid direct coupling between every sender and receiver.

## Queue

A queue buffers work.

It protects the worker from receiving more work than it can handle at once.

## Worker Or Serverless Function

The worker consumes queued work and performs the actual task.

For AOIS, that task could eventually be:

- inspect an incident
- route to a model
- call an owned agent loop
- write a structured result

## Dead-Letter Queue

A dead-letter queue stores messages that failed after retries.

It is a safety net for investigation and replay.

## Idempotency

Idempotency means the same event can be processed more than once without causing duplicate harmful effects.

Every event needs an `idempotency_key`.

## Trace Propagation

Trace propagation means every hop carries the same `trace_id`.

Without it, distributed debugging becomes guesswork.

## Payload Boundary

Large payloads should not be pushed through every queue hop.

The plan uses `store_pointer_not_blob`, meaning large data should live elsewhere and the event should carry a pointer.

## Build

Inspect:

```bash
sed -n '1,260p' cloud/aws/event-workflow.plan.json
sed -n '1,260p' examples/validate_event_workflow_plan.py
```

Compile:

```bash
python3 -m py_compile examples/validate_event_workflow_plan.py
```

Run:

```bash
python3 examples/validate_event_workflow_plan.py
```

Expected:

```json
{
  "cloud_resources_created": false,
  "credentials_used": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

Do not run provider commands. Do not create a queue, event bus, function, rule, topic, bucket, or scheduler.

## Ops Lab

Answer from the plan:

1. What namespace keeps this portfolio separate from primary AOIS resources?
2. Which field proves no cloud resources were created?
3. Which field proves credentials were not used?
4. Which message field supports distributed debugging?
5. Which message field prevents duplicate side effects?
6. What happens after retry exhaustion?
7. Why is `max_cloud_invocations` set to zero?

Answer key:

1. `aois-p`
2. `cloud_resources_created=false`
3. `credentials_used=false`
4. `trace_id`
5. `idempotency_key`
6. the message goes to a dead-letter queue
7. live cloud execution is not approved in this lesson

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Remove Idempotency

Remove `idempotency_key` from `message_contract.required_fields`.

Expected risk:

- retries or duplicate deliveries can produce duplicate side effects

### Option B - Disable DLQ

Set:

```json
"dead_letter_queue_required": false
```

Expected risk:

- failed messages disappear into logs or endless retries instead of being preserved for inspection

### Option C - Approve Live Cloud Too Early

Set:

```json
"approved_for_live_cloud": true
```

Expected risk:

- a plan-only lesson can be mistaken for permission to create provider resources

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. cloud resources created remains false
4. credentials used remains false
5. namespace remains `aois-p`
6. message contract includes `trace_id` and `idempotency_key`
7. DLQ, retry, timeout, least privilege, observability, cost gate, and rollback controls remain true

## Common Mistakes

- treating a queue as reliability by itself
- forgetting idempotency
- allowing infinite retries
- putting large blobs directly into events
- losing trace IDs between hops
- creating cloud resources before credential, budget, and rollback approval
- mixing `aois-p` portfolio resource names with primary AOIS resource names

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_event_workflow_plan.py
```

Read the `missing` list and restore the plan.

Common fixes:

- restore `namespace` to `aois-p`
- restore `cloud_resources_created` to `false`
- restore `credentials_used` to `false`
- restore `approved_for_live_cloud` to `false`
- restore `trace_id` and `idempotency_key`
- restore all required controls to `true`
- restore live limits to zero

If live event workflow work is requested:

- stop
- check official provider documentation
- define credentials and IAM
- define budget and max invocations
- define event schema and payload limits
- define DLQ replay runbook
- define rollback plan
- get explicit approval before creating resources

## Benchmark

Measure:

- validator compile result
- validator status
- namespace
- cloud resources created status
- credentials used status
- max cloud invocations
- repo disk footprint
- memory snapshot

## Architecture Defense

Why plan events before creating cloud resources?

Because event-driven systems fail differently from synchronous APIs. Duplicates, retries, poison messages, hidden queues, and replay all need design before live resources exist.

Why require `aois-p` names?

Because the portfolio project must stay visibly separate from the primary AOIS project on the same server or provider account.

Why keep cloud invocations at zero?

Because the lesson teaches the architecture and validation controls without spending money, using credentials, or changing provider state.

## 4-Layer Tool Drill

Tool: event queue

1. Plain English
It holds work until a worker is ready.

2. System Role
It decouples request intake from background processing.

3. Minimal Technical Definition
It is a durable message buffer between producers and consumers.

4. Hands-on Proof
The validator confirms the workflow plan includes a queue, retry policy, DLQ, trace ID, and idempotency key without creating cloud resources.

## 4-Level System Explanation Drill

1. Simple English
AOIS can plan background work without creating cloud infrastructure.

2. Practical Explanation
I can show how an event enters the system, waits in a queue, gets processed, and goes to a DLQ if retries fail.

3. Technical Explanation
`v11` adds a local JSON workflow plan and validator for event ingress, event bus, queue, worker, DLQ, message schema, retry policy, and live-cloud gates.

4. Engineer-Level Explanation
AOIS now separates event-driven architecture design from provider execution, requiring idempotency, trace propagation, payload boundaries, retry limits, DLQ replay, least privilege, observability, cost gates, and rollback before any live cloud workflow is created.

## Failure Story

Representative failure:

- Symptom: users submit one incident, but AOIS processes it multiple times and creates conflicting results
- Root cause: the event workflow allowed retries without an idempotency key
- Fix: add idempotency keys, deduplicate by event ID, and send exhausted failures to DLQ
- Prevention: validate the event workflow plan before creating queues/functions
- What this taught me: retries without idempotency can amplify failure

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v11` solve in AOIS?
2. What is event ingress?
3. What is an event bus?
4. What problem does a queue solve?
5. What is a dead-letter queue?
6. Why is idempotency mandatory?
7. Why must trace IDs cross every hop?
8. Why should large payloads use pointers instead of blobs?
9. Why are live cloud limits set to zero?
10. Why does the plan use `aois-p` names?
11. Explain event queue using the 4-layer tool rule.
12. Explain `v11` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v11` solve in AOIS?

It plans how AOIS can move background AI work through events without creating cloud resources.

2. What is event ingress?

The entry point that receives a request or signal and turns it into a workflow event.

3. What is an event bus?

A routing layer that moves events from producers to consumers without direct coupling.

4. What problem does a queue solve?

It buffers work so producers and workers do not need to operate at the same speed.

5. What is a dead-letter queue?

A queue for messages that failed after retry exhaustion.

6. Why is idempotency mandatory?

Because event systems can retry or deliver duplicates, and repeated processing must not create duplicate harmful effects.

7. Why must trace IDs cross every hop?

They connect logs and behavior across ingress, queue, worker, DLQ, and result sink.

8. Why should large payloads use pointers instead of blobs?

Large blobs make queues expensive, slow, and harder to inspect; pointers keep events small and durable.

9. Why are live cloud limits set to zero?

Because this lesson is validation-only and has no approval to create or invoke provider resources.

10. Why does the plan use `aois-p` names?

To keep portfolio resources visibly separate from the primary AOIS project.

11. Explain event queue using the 4-layer tool rule.

- Plain English: it holds work until a worker is ready.
- System Role: it decouples intake from processing.
- Minimal Technical Definition: it is a durable message buffer between producers and consumers.
- Hands-on Proof: the validator checks the queue, retry, DLQ, trace, and idempotency controls.

12. Explain `v11` using the 4-level system explanation rule.

- Simple English: AOIS plans background event processing.
- Practical explanation: I can explain ingress, queue, worker, DLQ, retries, and idempotency.
- Technical explanation: `v11` adds an event workflow JSON plan and no-cloud validator.
- Engineer-level explanation: AOIS can now design event-driven cloud workflows while gating provider execution behind schema, IAM, cost, observability, DLQ replay, idempotency, and rollback controls.

## Connection Forward

`v11` plans event-driven workflow execution.

`v12` moves to cloud observability and cost-control planning, because event-driven systems must be monitored before they are trusted.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v11 Introduction](02-introduction.md)
- Next: [v11 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
