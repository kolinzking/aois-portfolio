# v20.2 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v20.2 gives AOIS route choice before spend:

```text
incident -> evidence -> confidence -> budget -> route
```

AOIS can now decide whether to skip a tool, use a bounded read-only route, pause
for review, stop, or spend more on a high-severity investigation.

## Why The Next Version Exists

v21 introduces MCP and governed tool registries.

Budget-aware routing answers whether a route should be taken. It does not answer
which tools are registered, who owns them, what schemas they expose, what scopes
they require, or how they are audited.

v21 will turn the tool list into a governed registry so route policy has a safe
tool catalog to choose from.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.2 Looking Forward](09-looking-forward.md)
- Next: [v21 Start Here](../v21/00-start-here.md)
<!-- AOIS-NAV-END -->
