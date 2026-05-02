# v23.5 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v23.5 gives AOIS-P a connected agent evaluation layer. The system can now score
whether routing, registry, workflow, orchestration, safety, and budget decisions
match expected outcomes across representative cases.

This makes future runtime work less speculative because there is a local
regression gate for the agent control plane.

## Why The Next Version Exists

v23.8 introduces runtime operations and autonomy control.

Evaluation says whether the behavior is correct under test. Runtime operations
decide how much autonomy is allowed live, how to observe it, when to pause it,
and how to roll it back.

v23.5 answers "is the connected agent behavior correct enough in local evals?"
v23.8 answers "how do we operate that behavior safely when a runtime exists?"
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23.5 Looking Forward](looking-forward.md)
- Next: [v23.8 Contents](../v23.8/CONTENTS.md)
<!-- AOIS-NAV-END -->
