# v10.5 Contents

Authoring status: authored

## Start Here

Start with [02-introduction.md](02-introduction.md), then work through [03-notes.md](03-notes.md).

This version is about deciding who owns the agent loop:

- AOIS-owned runtime
- managed cloud agent runtime

The lesson does not create a cloud agent. It builds a tradeoff plan and validates that AOIS stays on the safer owned-runtime path until credentials, cost, data boundaries, tool permissions, evals, and rollback are approved.

## Topic Jumps

- Managed-agent tradeoff: [03-notes.md](03-notes.md#core-concepts)
- Resource gate: [03-notes.md](03-notes.md#resource-gate)
- Build and validation: [03-notes.md](03-notes.md#build)
- Break exercises: [04-lab.md](04-lab.md#break-lab)
- Operational recovery: [05-runbook.md](05-runbook.md)
- Benchmark: [07-benchmark.md](07-benchmark.md)
- Failure story: [06-failure-story.md](06-failure-story.md)
- Carry forward: [09-looking-forward.md](09-looking-forward.md)

## Self-Paced Path

1. Read the introduction and explain the difference between managed model calls and managed agents.
2. Inspect `cloud/aws/managed-agent-tradeoff.plan.json`.
3. Run the validator.
4. Complete the ops and break labs in [04-lab.md](04-lab.md).
5. Answer the mastery checkpoint in [03-notes.md](03-notes.md#mastery-checkpoint).
6. Check your answers against the answer key before moving to `v11`.

Do not move on if you cannot explain why managed agent creation is gated.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v10.5 Start Here](00-start-here.md)
- Next: [v10.5 Introduction](02-introduction.md)
<!-- AOIS-NAV-END -->
