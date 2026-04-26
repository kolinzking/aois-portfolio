# v20.2 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P budget-aware routing without starting a router,
executing tools, calling a provider, or calling a billing API.

Files:

- `agentic/aois-p/budget-aware-routing.plan.json`
- `examples/validate_budget_aware_routing_plan.py`
- `examples/simulate_budget_aware_routing.py`

Inspect:

```bash
sed -n '1,440p' agentic/aois-p/budget-aware-routing.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_budget_aware_routing_plan.py examples/simulate_budget_aware_routing.py
python3 examples/validate_budget_aware_routing_plan.py
python3 examples/simulate_budget_aware_routing.py
```

Expected:

```json
{
  "passed_cases": 6,
  "score": 1.0,
  "status": "pass",
  "total_cases": 6
}
```

## Break Lab

Change one value at a time, run the simulator, then restore the plan:

- set `accounting_complete` to `false`
- lower `remaining_budget_units` below `0.5`
- lower a route's `expected_value_units`
- raise a medium route's `estimated_cost_units` above `3.5`
- lower high-severity remaining budget below the full route cost plus reserve

## Explanation Lab

Explain why each case chooses its route:

- complete low-severity evidence uses `small_model_no_tool`
- partial medium evidence uses `read_only_evidence`
- expensive medium branch uses `human_budget_review`
- exhausted budget uses `stop`
- high-severity missing evidence uses `full_investigation`
- incomplete accounting uses `blocked`

## Defense Lab

Defend why v20.2 does not execute the selected route. The selected route is a
policy outcome; tool execution and live provider calls remain future controlled
integration work.
