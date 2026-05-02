# v22 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_durable_workflow_plan.py examples/simulate_durable_workflow.py
python3 examples/validate_durable_workflow_plan.py
python3 examples/simulate_durable_workflow.py
```

Passing criteria:

- Python compile succeeds.
- Validator returns `status: pass`.
- Validator returns an empty `missing` list.
- Simulator returns `status: pass`.
- Simulator passes 8 of 8 cases.
- Simulator score is `1.0`.
- Output confirms `agent_runtime_started: false`.
- Output confirms `workflow_runtime_started: false`.
- Output confirms `durable_store_created: false`.
- Output confirms `mcp_server_started: false`.
- Output confirms `tool_calls_executed: false`.
- Output confirms `provider_call_made: false`.

## Interpretation

The benchmark covers:

- `complete_no_tool_workflow`
- `complete_read_only_workflow_plan`
- `pause_for_human_approval`
- `resume_after_approval`
- `block_registry_denial`
- `recover_after_retry`
- `fail_timeout`
- `skip_duplicate_step`

It tests workflow policy only. It does not start a workflow engine, create a
durable store, start MCP, execute tools, or call a provider.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v22 Failure Story](failure-story.md)
- Next: [v22 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
