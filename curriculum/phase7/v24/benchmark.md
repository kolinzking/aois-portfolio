# v24 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_multi_agent_collaboration_plan.py examples/simulate_multi_agent_collaboration.py
python3 examples/validate_multi_agent_collaboration_plan.py
python3 examples/simulate_multi_agent_collaboration.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- runtime flags
- provider and tool flags

## Interpretation

Pass means:

- all collaboration policy controls are present
- every role is owned
- every role is blocked from tool execution and provider calls
- source notes are current for the lesson date
- shared state is supervisor-owned
- handoffs are serial
- all ten cases match expected decisions

Fail means AOIS-P is not ready to reason about multi-agent collaboration. Fix
the plan or simulator before moving to v25.
