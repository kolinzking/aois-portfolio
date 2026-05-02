# v21 Summary Notes

Authoring status: authored

## What Was Built

A local governed MCP tool registry plan and deterministic simulator:

- `agentic/aois-p/governed-tool-registry.plan.json`
- `examples/validate_governed_tool_registry_plan.py`
- `examples/simulate_governed_tool_registry.py`

## What Was Learned

MCP tool discovery is not enough. AOIS-P needs a registry that decides which
tools can be exposed to which route, which tools require approval, and which
tools must be blocked before execution.

The key controls are:

- trusted server label
- stable tool name
- owner
- schema references
- side-effect class
- route allowlist
- approval policy
- audit event
- status

## Core Limitation Or Tradeoff

v21 intentionally does not start MCP or execute tools. It proves governance
shape first. Live MCP would require transport, auth, consent UI, approval
workflow, audit sink, tool-result sanitization, registry change control, and
route integration testing before it should be used.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v21 Benchmark](07-benchmark.md)
- Next: [v21 Looking Forward](09-looking-forward.md)
<!-- AOIS-NAV-END -->
