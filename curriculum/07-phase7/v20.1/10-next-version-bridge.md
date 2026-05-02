# v20.1 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v20.1 gives AOIS a cost ledger:

```text
incident -> step -> usage -> cost units -> decision
```

Every simulated agentic response now has an economic shape.

## Why The Next Version Exists

v20.2 adds budget-aware routing.

Cost visibility is useful, but it is still reactive. The next improvement is to
choose a route before spend happens:

- use a cheaper model when confidence is already high
- avoid a tool call when evidence is sufficient
- ask a human before an expensive branch
- stop a workflow when the expected value is too low
- reserve expensive routes for severe incidents

v20.2 will use the accounting fields from v20.1 to decide where the responder
should go next.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.1 Looking Forward](09-looking-forward.md)
- Next: [v20.2 Start Here](../v20.2/00-start-here.md)
<!-- AOIS-NAV-END -->
