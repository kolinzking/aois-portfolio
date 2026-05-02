# v21 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P governed MCP tool registry decisions without
starting an MCP server, exposing tools to a model, executing tools, or calling a
provider.

Files:

- `agentic/aois-p/governed-tool-registry.plan.json`
- `examples/validate_governed_tool_registry_plan.py`
- `examples/simulate_governed_tool_registry.py`

Inspect:

```bash
sed -n '1,520p' agentic/aois-p/governed-tool-registry.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_governed_tool_registry_plan.py examples/simulate_governed_tool_registry.py
python3 examples/validate_governed_tool_registry_plan.py
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

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- remove `owner` from `query_service_metrics`
- change `query_service_metrics.server_label` to `unknown_external_mcp`
- add a space to `fetch_recent_logs.tool_name`
- set `read_incident_trace.human_approval_required` to `false`
- set `restart_pod.default_enabled` to `true`
- add `full_investigation` to `restart_pod.allowed_routes`
- remove `block_unregistered_tool` from `decision_gates`

## Explanation Lab

Explain why each case chooses its decision:

- no requested tools returns `allow_no_tool_route`
- active read-only tools on a trusted server return `allow_read_only_tool_plan`
- sensitive trace reads return `require_human_approval`
- unknown tools return `block_unregistered_tool`
- unknown servers return `block_untrusted_server`
- write-effect tools return `block_side_effecting_tool`
- disabled privileged tools return `block_disabled_tool`

## Defense Lab

Defend why v21 does not start MCP. The registry is a governance artifact. It
must prove ownership, naming, schema, routing, approval, and audit controls
before a protocol runtime is allowed to expose tools to a model.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v21 - MCP and Governed Tool Registries](notes.md)
- Next: [v21 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
