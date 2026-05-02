# v20.2 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_budget_aware_routing_plan.py examples/simulate_budget_aware_routing.py
python3 examples/validate_budget_aware_routing_plan.py
python3 examples/simulate_budget_aware_routing.py
```

Passing criteria:

- Python compile succeeds.
- Validator returns `status: pass`.
- Validator returns an empty `missing` list.
- Simulator returns `status: pass`.
- Simulator passes 6 of 6 cases.
- Simulator score is `1.0`.
- Output confirms `agent_runtime_started: false`.
- Output confirms `routing_runtime_started: false`.
- Output confirms `tool_calls_executed: false`.
- Output confirms `provider_call_made: false`.
- Output confirms `billing_api_called: false`.

## Interpretation

The benchmark covers:

- `route_small_model_no_tool`
- `route_read_only_tool`
- `request_budget_review`
- `stop_budget_exhausted`
- `route_high_severity_full_investigation`
- `block_incomplete_accounting`

It tests routing policy only. It does not execute the selected route.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.2 Failure Story](failure-story.md)
- Next: [v20.2 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
