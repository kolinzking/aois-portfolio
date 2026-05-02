# v24 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v24 gives AOIS-P a governed collaboration layer:

- supervisor-led routing
- specialist role ownership
- handoff contracts
- shared state ownership
- context freshness checks
- conflict escalation
- handoff loop limits
- local validation and simulation

AOIS-P can now decide who should work on a case without starting a live
multi-agent runtime.

## Why The Next Version Exists

v25 defines safe execution boundaries.

Multi-agent coordination still does not mean the system may execute actions.
The next version must classify which actions remain plan-only, which can run in
read-only mode, which require approval, which need sandboxing, and which are
forbidden.

The bridge from v24 to v25 is:

```text
coordinate agent roles -> bound what any role may execute
```
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v24 Looking Forward](looking-forward.md)
- Next: [v25 Contents](../v25/CONTENTS.md)
<!-- AOIS-NAV-END -->
