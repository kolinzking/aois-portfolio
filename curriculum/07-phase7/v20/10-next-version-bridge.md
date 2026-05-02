# v20 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v20 gives AOIS step structure:

```text
incident -> planned step -> tool boundary -> evidence -> decision
```

Every step now has a reason, a safety status, and an outcome.

## Why The Next Version Exists

v20.1 adds per-incident and per-step cost accounting.

Agentic systems can become expensive in small increments:

- one extra trace query
- one repeated log search
- one unnecessary model turn
- one failed tool result followed by a retry
- one approval loop with no useful evidence

Without cost accounting, AOIS cannot tell whether an agentic investigation is
worth what it consumed.

v20.1 will attach cost and usage records to the responder steps introduced in
v20.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20 Looking Forward](09-looking-forward.md)
- Next: [v20.1 Start Here](../v20.1/00-start-here.md)
<!-- AOIS-NAV-END -->
