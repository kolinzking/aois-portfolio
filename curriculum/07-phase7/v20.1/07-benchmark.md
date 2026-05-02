# v20.1 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_step_cost_accounting_plan.py examples/simulate_step_cost_accounting.py
python3 examples/validate_step_cost_accounting_plan.py
python3 examples/simulate_step_cost_accounting.py
```

Passing criteria:

- Python compile succeeds.
- Validator returns `status: pass`.
- Validator returns an empty `missing` list.
- Simulator returns `status: pass`.
- Simulator passes 5 of 5 cases.
- Simulator score is `1.0`.
- Output confirms `agent_runtime_started: false`.
- Output confirms `tool_calls_executed: false`.
- Output confirms `provider_call_made: false`.
- Output confirms `billing_api_called: false`.

## Interpretation

The benchmark covers:

- `within_budget`
- `step_waste_flagged`
- `incident_budget_exceeded`
- `accounting_incomplete`
- `approval_cost_review`

It does not estimate a real invoice, call a live model, call a billing API,
execute tools, start an agent runtime, create a dashboard, or persist telemetry.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.1 Failure Story](06-failure-story.md)
- Next: [v20.1 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
