# v24 Introduction

Authoring status: authored

## What This Version Is About

v24 teaches governed multi-agent collaboration for AOIS-P.

The lesson does not start a live multi-agent framework. It defines a local plan
for supervisor-led routing, specialist roles, handoff contracts, shared state,
context freshness, conflict escalation, and loop limits. The validator checks
the plan shape. The simulator proves that collaboration decisions are
deterministic.

## Why It Matters In AOIS

AOIS-P now has tool planning, budget routing, registry governance, durable
workflow state, orchestration, evaluation, and runtime autonomy control. A
multi-agent layer can only help if it preserves those controls.

Without explicit collaboration policy, agents can:

- pass stale context
- duplicate work
- hide ownership
- race on shared state
- disagree without escalation
- continue handoffs after the operator has lost the thread

v24 treats multi-agent design as an operations problem first.

## How To Use This Version

Read `notes.md`, inspect the plan, run the validator, and run the simulator.
Then use the break lab to change one control at a time and observe how the
validator or simulator catches it.

Do not add a live runtime in this version. The point is to prove the role and
handoff policy before execution boundaries are introduced in v25.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v24 Contents](CONTENTS.md)
- Next: [v24 - Multi-Agent Collaboration](notes.md)
<!-- AOIS-NAV-END -->
