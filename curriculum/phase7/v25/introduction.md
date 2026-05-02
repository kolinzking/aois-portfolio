# v25 Introduction

Authoring status: authored

## What This Version Is About

v25 teaches safe execution boundaries for AOIS-P.

The lesson does not execute commands, call tools, write files, open network
connections, start a sandbox, or call a provider. It defines a local policy for
classifying requested actions and deciding whether AOIS-P should record,
stage, pause for approval, block, or deny.

## Why It Matters In AOIS

AOIS-P now has governed tool planning, cost accounting, registry decisions,
workflow state, orchestration, evaluation, autonomy control, and multi-agent
collaboration. Those controls are incomplete until execution is bounded.

The important distinction is:

```text
approval is not execution permission
```

An action can be approved and still be blocked because credentials are broad,
network egress is not allowed, sandboxing is missing, rollback is missing, a
guardrail trips, or dry-run staging is unavailable.

## How To Use This Version

Read `notes.md`, inspect the plan, run the validator, and run the simulator.
Then use the break lab to change one boundary control at a time.

Do not add live execution to this version. The point is to finish Phase 7 with
a defensible execution policy before Phase 8 builds the human-facing product
surface.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v25 Contents](CONTENTS.md)
- Next: [v25 - Safe Execution Boundaries](notes.md)
<!-- AOIS-NAV-END -->
