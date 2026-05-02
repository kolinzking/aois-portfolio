# v21 - MCP and Governed Tool Registries

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no MCP server, no registry runtime, no tool execution, no provider
call, no external network during validation, no install, no cloud resource, no
persistent storage, no live registry enforcement

## What This Builds

This version builds a local governed MCP tool registry plan and simulation:

- `agentic/aois-p/governed-tool-registry.plan.json`
- `examples/validate_governed_tool_registry_plan.py`
- `examples/simulate_governed_tool_registry.py`

It teaches:

- MCP host, client, server, and tool boundaries
- why tool descriptions and annotations are not enough governance
- trusted server labels
- stable tool names
- input and output schema references
- owner and audit requirements
- route allowlists from v20.2
- read-only, sensitive-read, write, and privileged tool classes
- human approval gates for sensitive reads
- default blocking for side-effecting tools
- deterministic registry simulation without live execution

## Why This Exists

An agentic system is only as safe as its exposed tools.

Budget-aware routing decides whether AOIS should spend the next step. A governed
tool registry decides whether the chosen route is allowed to see a tool, who
owns that tool, what schema it accepts, what data it can touch, what audit event
it emits, and whether a human must approve it.

The central registry question is:

```text
Given a route decision and requested tool list, which tools are allowed,
which require approval, and which must be blocked before execution?
```

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure`

v21 connects the route layer to the tool layer. A future MCP integration can
expose tools only after this registry proves:

- the server label is trusted for AOIS-P
- the tool exists in the catalog
- the tool is active
- the tool is allowed for the selected route
- side effects are classified
- sensitive operations pause for approval
- write and privileged operations are blocked by default

## Learning Goals

By the end of this version you should be able to:

- explain where MCP fits in the AOIS agent control plane
- distinguish tool discovery from tool permission
- define a governed tool registry entry
- explain why tool names need stable policy
- explain why tool descriptions are treated as untrusted metadata
- classify tools by side effect and data scope
- map v20.2 route decisions to allowed tool sets
- identify which tools need explicit approval
- block unregistered tools, untrusted servers, disabled tools, and write-effect tools
- validate and simulate the registry without starting MCP

## Prerequisites

You should have completed:

- `v20` tool-using incident responder
- `v20.1` per-incident and per-step cost accounting
- `v20.2` budget-aware routing

Required checks:

```bash
python3 -m py_compile examples/validate_governed_tool_registry_plan.py examples/simulate_governed_tool_registry.py
python3 examples/validate_governed_tool_registry_plan.py
python3 examples/simulate_governed_tool_registry.py
```

## Core Concepts

## MCP Shape

MCP separates the host application, client connection, and server capability.
Servers can expose tools, resources, and prompts. Tools are functions that an
AI system can request through the protocol.

AOIS-P does not start a server in v21. It records the governance contract that a
future MCP server must satisfy before any tool is exposed.

## Registry Before Runtime

Do not discover tools first and govern them later.

The registry comes first because tool exposure is a control-plane decision. A
tool should have a name, owner, schema, route allowlist, side-effect class,
approval policy, data scope, and audit event before the model can see it.

## Tool Descriptions Are Not Policy

Tool descriptions help a model understand how to use a tool. They are not a
security boundary.

v21 treats descriptions and annotations as untrusted metadata. The policy lives
in the registry fields and simulator decisions.

## Route Allowlists

v20.2 produced route decisions such as:

- `route_small_model_no_tool`
- `route_read_only_tool`
- `route_high_severity_full_investigation`

v21 maps those decisions to tool exposure:

- no-tool routes expose no tools
- read-only evidence routes can plan metrics and logs
- full investigation routes can plan broader read-only tools
- sensitive trace reads require approval
- write and privileged tools remain blocked

## Side-Effect Classes

The plan uses four side-effect classes:

- `read_only`: bounded read of AOIS-P evidence
- `sensitive_read`: read of data that needs explicit approval
- `write_effect`: mutation of AOIS-P state or workflow
- `privileged_execution`: command or host-level execution

Only `read_only` tools can be planned without approval in v21, and even those
are planned only in a local simulation. Nothing executes.

## Build

Inspect:

```bash
sed -n '1,520p' agentic/aois-p/governed-tool-registry.plan.json
sed -n '1,360p' examples/validate_governed_tool_registry_plan.py
sed -n '1,280p' examples/simulate_governed_tool_registry.py
```

Compile:

```bash
python3 -m py_compile examples/validate_governed_tool_registry_plan.py examples/simulate_governed_tool_registry.py
```

Validate:

```bash
python3 examples/validate_governed_tool_registry_plan.py
```

Simulate:

```bash
python3 examples/simulate_governed_tool_registry.py
```

Expected:

```json
{
  "passed_cases": 7,
  "score": 1.0,
  "status": "pass",
  "total_cases": 7
}
```

## Ops Lab

1. Open the registry plan.
2. Find `medium_read_only_registry_allow`.
3. Confirm both requested tools are registered and active.
4. Confirm their server label is trusted.
5. Confirm their side-effect class is `read_only`.
6. Confirm the simulator chooses `allow_read_only_tool_plan`.
7. Explain why this is still a plan, not execution.

## Break Lab

Break the plan locally, then restore it:

1. Change `query_service_metrics` to use an untrusted server label.
2. Confirm validation fails.
3. Restore the trusted server label.
4. Add a space to a tool name.
5. Confirm validation catches the name policy violation.
6. Restore the tool name.
7. Set `restart_pod.default_enabled` to `true`.
8. Confirm validation blocks side-effecting tools from being enabled by default.
9. Restore the value.

## Testing

The validator checks:

- runtime, MCP, provider, and execution flags remain disabled
- AOIS-P scope and primary AOIS separation are explicit
- MCP source notes are recorded
- registry controls are present
- required registry dimensions are present
- server labels are allowlisted
- tool names follow the policy
- tool entries include owners, schemas, routes, decisions, status, and audit events
- sensitive tools require approval
- side-effecting tools are disabled by default and have no allowed routes
- all seven decision gates have simulation cases
- live MCP prerequisites are listed

## Common Mistakes

- Treating MCP discovery as authorization.
- Letting tool descriptions act as the source of truth.
- Registering a tool without an owner.
- Forgetting input or output schema references.
- Allowing a tool on every route by default.
- Treating read-only and sensitive-read tools as the same risk.
- Exposing write-effect tools before approval, rollback, and audit exist.
- Mixing AOIS-P tools with primary AOIS tools.

## Troubleshooting

If validation fails, inspect the `missing` list.

If simulation fails, compare `decision`, `allowed_tools`,
`approval_required_for`, `blocked_tools`, and the expected fields for the case.

If a read-only tool is blocked, check:

- server label
- tool name
- `status`
- `side_effect_level`
- `allowed_routes`
- `allowed_decisions`

If a sensitive tool does not pause, check `human_approval_required` and
`approval_policy`.

## Benchmark

The benchmark target is:

- compile succeeds
- validator status `pass`
- validator missing list is empty
- simulator status `pass`
- 7 of 7 registry cases passing
- no agent runtime
- no MCP server
- no registry runtime
- no tool execution
- no provider call

## Architecture Defense

The registry is local and deterministic in this lesson because the goal is to
prove the governance shape before any protocol runtime exists.

A live MCP integration would need server identity, transport choice, auth,
consent UI, approval workflow, tool-result sanitization, registry change
control, audit logs, route integration tests, and primary AOIS separation.

v21 blocks write and privileged tools because those need rollback design,
operator authority, blast-radius limits, and stronger evidence than this lesson
is meant to prove.

## 4-Layer Tool Drill

1. User layer: explain why a tool request is allowed, paused, or blocked.
2. App layer: validate registry entries and simulate route-to-tool decisions.
3. Model layer: expose only route-appropriate tools, and treat descriptions as untrusted.
4. Infra layer: keep MCP servers, providers, tool execution, and persistent state disabled.

## 4-Level System Explanation Drill

1. Beginner: AOIS keeps a list of tools it is allowed to use.
2. Practitioner: each tool has an owner, schema, route allowlist, risk class, and approval rule.
3. Operator: untrusted, unknown, disabled, or side-effecting tools are blocked before execution.
4. Architect: governed registries turn MCP from open-ended tool discovery into a controlled agent boundary.

## Failure Story

See [06-failure-story.md](06-failure-story.md).

## Mastery Checkpoint

You are ready to move on when you can:

- explain every registry decision gate
- predict the result of all seven simulator cases
- defend why descriptions are not policy
- classify read-only, sensitive-read, write-effect, and privileged tools
- explain why v21 plans tools without executing them
- list the checks required before live MCP is acceptable

## Connection Forward

v22 introduces durable agent workflows. v21 controls which tools can be exposed
to a route; v22 will control how a multi-step agent workflow preserves state,
waits for approval, resumes safely, and records progress across time.

## Source Notes

Sources checked on 2026-04-29:

- Model Context Protocol specification: <https://modelcontextprotocol.io/specification/>
- MCP tools documentation: <https://modelcontextprotocol.io/docs/concepts/tools>
- MCP security best practices: <https://modelcontextprotocol.io/specification/draft/basic/security_best_practices>

Claims supported:

- MCP uses host, client, server, and tool boundaries.
- Tools expose names, descriptions, input schemas, and optional output schemas.
- Tool invocation requires explicit safety and consent controls.
- Tool metadata is not a sufficient security boundary.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v21 Introduction](02-introduction.md)
- Next: [v21 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
