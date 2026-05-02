# v21 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_governed_tool_registry_plan.py examples/simulate_governed_tool_registry.py
python3 examples/validate_governed_tool_registry_plan.py
python3 examples/simulate_governed_tool_registry.py
```

Passing criteria:

- Python compile succeeds.
- Validator returns `status: pass`.
- Validator returns an empty `missing` list.
- Simulator returns `status: pass`.
- Simulator passes 7 of 7 cases.
- Simulator score is `1.0`.
- Output confirms `agent_runtime_started: false`.
- Output confirms `mcp_server_started: false`.
- Output confirms `tool_registry_runtime_started: false`.
- Output confirms `tool_calls_executed: false`.
- Output confirms `provider_call_made: false`.

## Interpretation

The benchmark covers:

- `allow_no_tool_route`
- `allow_read_only_tool_plan`
- `require_human_approval`
- `block_unregistered_tool`
- `block_untrusted_server`
- `block_side_effecting_tool`
- `block_disabled_tool`

It tests registry policy only. It does not start MCP and does not execute any
selected tool.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v21 Failure Story](failure-story.md)
- Next: [v21 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
