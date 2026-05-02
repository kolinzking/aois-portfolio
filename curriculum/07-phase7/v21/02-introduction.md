# v21 Introduction

Authoring status: authored

## What This Version Is About

This version introduces MCP and governed tool registries for AOIS-P.

It does not start an MCP server. It builds the local control plane that must
exist before a future agent can discover or call tools:

- tool names
- server labels
- owners
- input and output schema references
- side-effect classification
- route allowlists
- approval policy
- audit event names
- disabled and review-required states

## Why It Matters In AOIS

v20.2 decided whether an incident route should continue, downgrade, pause, or
stop. v21 decides which tools can be exposed to that route at all.

MCP makes tool discovery and invocation composable. That is useful only when
the registry is governed. Without a registry, an agent can drift from bounded
read-only evidence into unknown tools, untrusted servers, sensitive reads, or
side-effecting actions.

## How To Use This Version

Work locally and deterministically:

```bash
python3 -m py_compile examples/validate_governed_tool_registry_plan.py examples/simulate_governed_tool_registry.py
python3 examples/validate_governed_tool_registry_plan.py
python3 examples/simulate_governed_tool_registry.py
```

Expected outcome:

- the validator returns `status: pass`
- the validator returns `missing: []`
- the simulator passes 7 of 7 registry cases
- no MCP server starts
- no tool executes
- no provider call is made
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v21 Contents](01-contents.md)
- Next: [v21 - MCP and Governed Tool Registries](03-notes.md)
<!-- AOIS-NAV-END -->
