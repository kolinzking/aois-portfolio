# v21 Looking Forward

Authoring status: authored

## What You Should Carry Forward

Tool access is an operational boundary, not a convenience feature.

Carry forward these rules:

- route selection does not authorize every tool
- MCP discovery is not permission
- tool descriptions are not security policy
- every tool needs an owner, schema, side-effect class, route allowlist, approval rule, and audit event
- sensitive reads pause before execution
- write and privileged tools stay blocked until stronger runtime controls exist

## What The Next Version Will Build On

v22 will use this registry boundary as a workflow input.

The next step is not simply to run more tools. It is to make agent work durable:
the workflow must remember the selected route, requested tools, approvals,
blocked actions, cost context, and recovery point across a multi-step incident
response.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v21 Summary Notes](summarynotes.md)
- Next: [v21 Next Version Bridge](next-version-bridge.md)
<!-- AOIS-NAV-END -->
