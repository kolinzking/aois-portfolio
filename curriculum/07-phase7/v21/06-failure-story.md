# v21 Failure Story

Authoring status: authored

## Symptom

A future incident responder is allowed to use a read-only evidence route, but
the model requests `dump_cluster_secrets` from the observability server. The
tool name sounds useful during debugging, but it is not in the governed AOIS-P
registry.

## Root Cause

The route decision was treated as broad permission to discover tools. The tool
registry boundary was skipped, so an unregistered request reached the point
where a runtime might try to resolve it.

The deeper issue is confusing three different controls:

- budget route selection
- MCP tool discovery
- governed tool authorization

## Fix

Reject the request before execution:

```bash
python3 examples/simulate_governed_tool_registry.py
```

The `unknown_tool_blocked` case must return:

```text
decision=block_unregistered_tool
blocked_tools=dump_cluster_secrets
```

Then require registry review before the tool can be added. A valid addition
needs an owner, trusted server label, schema references, side-effect class,
route allowlist, approval policy, audit event, and live MCP readiness review.

## Prevention

Keep the registry in front of MCP exposure:

- never expose tools only because the model asked for them
- treat tool descriptions as untrusted metadata
- require server labels from the trusted AOIS-P list
- require owners and schemas
- allow tools per route, not globally
- pause sensitive reads for approval
- block write and privileged tools by default
- keep live MCP disabled until all live-readiness checks pass
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v21 Runbook](05-runbook.md)
- Next: [v21 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
