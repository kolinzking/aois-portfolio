# v10.5 Contents

Authoring status: authored

## Start Here

Start with [introduction.md](introduction.md), then work through [notes.md](notes.md).

This version is about deciding who owns the agent loop:

- AOIS-owned runtime
- managed cloud agent runtime

The lesson does not create a cloud agent. It builds a tradeoff plan and validates that AOIS stays on the safer owned-runtime path until credentials, cost, data boundaries, tool permissions, evals, and rollback are approved.

## Topic Jumps

- Managed-agent tradeoff: [notes.md](notes.md#core-concepts)
- Resource gate: [notes.md](notes.md#resource-gate)
- Build and validation: [notes.md](notes.md#build)
- Break exercises: [lab.md](lab.md#break-lab)
- Operational recovery: [runbook.md](runbook.md)
- Benchmark: [benchmark.md](benchmark.md)
- Failure story: [failure-story.md](failure-story.md)
- Carry forward: [looking-forward.md](looking-forward.md)

## Self-Paced Path

1. Read the introduction and explain the difference between managed model calls and managed agents.
2. Inspect `cloud/aws/managed-agent-tradeoff.plan.json`.
3. Run the validator.
4. Complete the ops and break labs in [lab.md](lab.md).
5. Answer the mastery checkpoint in [notes.md](notes.md#mastery-checkpoint).
6. Check your answers against the answer key before moving to `v11`.

Do not move on if you cannot explain why managed agent creation is gated.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v10 Next Version Bridge](../v10/next-version-bridge.md)
- Next: [v10.5 Introduction](introduction.md)
<!-- AOIS-NAV-END -->
