# v23 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_stateful_orchestration_plan.py examples/simulate_stateful_orchestration.py
python3 examples/validate_stateful_orchestration_plan.py
python3 examples/simulate_stateful_orchestration.py
```

Passing criteria:

- Python compile succeeds.
- Validator returns `status: pass`.
- Validator returns an empty `missing` list.
- Simulator returns `status: pass`.
- Simulator passes 10 of 10 cases.
- Simulator score is `1.0`.
- Output confirms `agent_runtime_started: false`.
- Output confirms `orchestration_runtime_started: false`.
- Output confirms `workflow_runtime_started: false`.
- Output confirms `mcp_server_started: false`.
- Output confirms `tool_calls_executed: false`.
- Output confirms `provider_call_made: false`.
- Output confirms `durable_store_created: false`.

## Interpretation

The benchmark covers:

- `stop_terminal_state`
- `stop_iteration_limit`
- `stop_no_progress`
- `stop_budget_reserve`
- `stop_registry_block`
- `wait_for_approval`
- `resume_after_approval`
- `plan_read_only_evidence`
- `prepare_answer`
- `close_workflow`

It tests orchestration policy only. It does not run an orchestration framework
or execute selected actions.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23 Failure Story](failure-story.md)
- Next: [v23 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
