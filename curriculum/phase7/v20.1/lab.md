# v20.1 Lab

Authoring status: authored

## Build Lab

Validate and simulate cost accounting for AOIS-P agentic responder steps without
starting a runtime, executing tools, calling a provider, or calling a billing
API.

Files:

- `agentic/aois-p/step-cost-accounting.plan.json`
- `examples/validate_step_cost_accounting_plan.py`
- `examples/simulate_step_cost_accounting.py`

Inspect:

```bash
sed -n '1,420p' agentic/aois-p/step-cost-accounting.plan.json
```

Confirm:

- `agent_runtime_started` is `false`
- `tool_calls_executed` is `false`
- `provider_call_made` is `false`
- `billing_api_called` is `false`
- `unit_cost_model` is `provider_neutral_training_units`
- every case has per-step usage records

## Ops Lab

Compile and run the deterministic checks:

```bash
python3 -m py_compile examples/validate_step_cost_accounting_plan.py examples/simulate_step_cost_accounting.py
python3 examples/validate_step_cost_accounting_plan.py
python3 examples/simulate_step_cost_accounting.py
```

Expected:

```json
{
  "passed_cases": 5,
  "score": 1.0,
  "status": "pass",
  "total_cases": 5
}
```

## Break Lab

Change one value at a time, run the simulator, then restore the plan:

- set a passing step's `accounted` value to `false`
- raise a step's `retry_count` to `2`
- duplicate a read-only tool in one incident
- raise output tokens until an incident crosses `5.0` cost units

## Explanation Lab

Use the simulator output to explain:

- `bounded_latency_investigation`: accounting is complete and total cost is under budget.
- `repeated_log_search`: the same read-only tool is used twice.
- `runaway_trace_investigation`: no single step is too expensive, but the incident total is.
- `missing_step_usage_record`: one step is not trusted for accounting.
- `approval_loop_wait`: approval wait cost crosses the review threshold.

## Defense Lab

Defend why this lesson uses deterministic `cost_units` instead of USD. The core
answer: the lesson is testing the accounting contract, while real pricing and
billing reconciliation are live integration concerns.
