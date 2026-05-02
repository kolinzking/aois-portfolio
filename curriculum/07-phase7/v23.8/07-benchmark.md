# v23.8 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_runtime_autonomy_control_plan.py examples/simulate_runtime_autonomy_control.py
python3 examples/validate_runtime_autonomy_control_plan.py
python3 examples/simulate_runtime_autonomy_control.py
```

Passing criteria:

- Python compile succeeds.
- Validator returns `status: pass`.
- Validator returns an empty `missing` list.
- Simulator returns `status: pass`.
- Simulator passes 10 of 10 cases.
- Simulator score is `1.0`.
- Output confirms `agent_runtime_started: false`.
- Output confirms `autonomy_runtime_started: false`.
- Output confirms `provider_call_made: false`.
- Output confirms `tool_calls_executed: false`.

## Interpretation

The benchmark covers:

- kill switch disable
- safety event emergency stop
- evaluation regression rollback
- degraded runtime demotion
- missing observability hold
- budget exhaustion pause
- shadow mode entry
- supervised mode entry
- limited autonomy approval requirement
- limited autonomy gate pass

It tests autonomy policy only. It does not start a runtime or grant real
autonomy.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23.8 Failure Story](06-failure-story.md)
- Next: [v23.8 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
