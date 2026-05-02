# v23.8 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P runtime autonomy control without starting an agent
runtime, autonomy runtime, orchestration runtime, workflow runtime, MCP server,
tool call, provider call, or durable store.

Files:

- `agentic/aois-p/runtime-autonomy-control.plan.json`
- `examples/validate_runtime_autonomy_control_plan.py`
- `examples/simulate_runtime_autonomy_control.py`

Inspect:

```bash
sed -n '1,760p' agentic/aois-p/runtime-autonomy-control.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_runtime_autonomy_control_plan.py examples/simulate_runtime_autonomy_control.py
python3 examples/validate_runtime_autonomy_control_plan.py
python3 examples/simulate_runtime_autonomy_control.py
```

Expected:

```json
{
  "passed_cases": 10,
  "score": 1.0,
  "status": "pass",
  "total_cases": 10
}
```

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- set `kill_switch` to `false` in `kill_switch_disables`
- change `safety_event_emergency_stop.safety_status` to `clear`
- change `eval_regression_rolls_back.eval_status` to `pass`
- set `observability_missing_holds.observability_status` to `healthy`
- set `limited_requires_approval.operator_approval` to `granted`
- change one mode to `executes_tools: true`

## Explanation Lab

Explain why each case chooses its decision:

- kill switch disables autonomy
- safety event emergency-stops autonomy
- evaluation regression rolls back to shadow
- degraded runtime demotes to shadow
- missing observability holds shadow mode
- budget exhaustion pauses autonomy
- shadow mode is allowed without approval
- supervised mode requires approval
- limited autonomy requires approval
- limited autonomy is allowed only when all gates pass

## Defense Lab

Defend why v23.8 does not start a runtime. Runtime autonomy changes operational
risk. AOIS-P first proves the mode catalog, promotion gates, demotion gates,
kill switch, rollback path, and operator controls locally.
