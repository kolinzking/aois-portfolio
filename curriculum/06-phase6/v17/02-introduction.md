# v17 Introduction

Authoring status: authored

## What This Version Is About

v17 introduces event streaming as a control-plane pattern for AI
infrastructure. The goal is not to run Kafka, Redis Streams, NATS, or any other
broker yet. The goal is to learn the shape of a safe stream before creating a
runtime dependency on a shared server.

In AOIS, event streaming becomes useful when incident signals, agent actions,
evaluation events, routing decisions, and remediation recommendations need to
move between services without requiring every service to be online at exactly
the same time.

## Why It Matters In AOIS

Direct calls are simple, but they couple systems tightly. If an incident
classifier calls a remediation worker directly, the worker must be healthy at
that moment. A stream creates a durable handoff point: producers write events,
consumers process them at their own pace, and operators can inspect lag,
replay history, and dead-letter failures.

This matters for AI infrastructure because agents can create high-value but
bursty operational events. Without contracts, offsets, replay, and poison-event
handling, the system becomes hard to debug and unsafe to automate.

## How To Use This Version

Use this version as a self-paced design and simulation lab:

1. Read the event streaming notes.
2. Inspect the `aois-p` event streaming plan.
3. Run the validator to prove the plan is safe and non-runtime.
4. Run the simulator to see how event order, offsets, lag, replay, and
   dead-letter handling fit together.
5. Defend when AOIS should move from simulation to a real broker.

Do not install or start a broker for this lesson. A real broker is only
appropriate after storage budgets, retention, monitoring, backup, and rollback
rules are explicit.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17 Contents](01-contents.md)
- Next: [v17 - Event Streaming Without Broker Runtime](03-notes.md)
<!-- AOIS-NAV-END -->
