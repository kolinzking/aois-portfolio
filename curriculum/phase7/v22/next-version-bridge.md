# v22 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v22 gives AOIS-P a durable workflow contract. Agent work can now be represented
as checkpointed steps with route context, registry context, approval waits,
retry policy, timeout policy, terminal states, and recovery actions.

This means AOIS can reason about agent progress without relying on ephemeral
process memory or one-shot scripts.

## Why The Next Version Exists

v23 introduces stateful orchestration loops.

Durable workflows preserve state across steps. Orchestration loops decide what
the agent should do next when new evidence, approvals, retries, or failures
change the state.

The workflow answers "where are we and how do we resume?" v23 answers "given
the current state, what is the next bounded action?"
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v22 Looking Forward](looking-forward.md)
- Next: [v23 Contents](../v23/CONTENTS.md)
<!-- AOIS-NAV-END -->
