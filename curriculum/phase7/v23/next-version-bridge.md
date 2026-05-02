# v23 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v23 gives AOIS-P a bounded orchestration loop. The loop can read durable
workflow state, apply ordered stop and wait guards, choose the next safe action,
and refuse to continue when state is terminal, stagnant, blocked, over budget,
or past iteration limits.

This turns durable workflow state from v22 into controlled next-action policy.

## Why The Next Version Exists

v23.5 introduces agent evaluation.

An orchestration loop is only useful if AOIS can measure whether the loop made
the right decisions. The next version evaluates routing, registry, workflow, and
orchestration outcomes as a connected agent behavior rather than isolated
validators.

v23 answers "what should the loop do next?" v23.5 answers "how do we know the
loop is good enough to trust?"
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23 Looking Forward](looking-forward.md)
- Next: [v23.5 Start Here](../v23.5/00-start-here.md)
<!-- AOIS-NAV-END -->
