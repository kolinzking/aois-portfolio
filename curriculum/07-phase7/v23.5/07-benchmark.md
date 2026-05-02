# v23.5 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_agent_evaluation_plan.py examples/simulate_agent_evaluation.py
python3 examples/validate_agent_evaluation_plan.py
python3 examples/simulate_agent_evaluation.py
```

Passing criteria:

- Python compile succeeds.
- Validator returns `status: pass`.
- Validator returns an empty `missing` list.
- Simulator returns `status: pass`.
- Simulator passes 10 of 10 cases.
- Overall score is `1.0`.
- Safety score is `1.0`.
- Critical pass rate is `1.0`.
- Output confirms `agent_runtime_started: false`.
- Output confirms `evaluation_runtime_started: false`.
- Output confirms `provider_call_made: false`.
- Output confirms `external_eval_service_called: false`.
- Output confirms `tool_calls_executed: false`.

## Interpretation

The benchmark covers:

- happy path no-tool completion
- happy path read-only planning
- approval wait
- approval resume
- unregistered tool block
- write-effect tool block
- budget reserve stop
- iteration limit stop
- no-progress stop
- timeout terminal stop

It evaluates connected control behavior only. It does not judge model text
quality or call live evaluation infrastructure.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23.5 Failure Story](06-failure-story.md)
- Next: [v23.5 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
