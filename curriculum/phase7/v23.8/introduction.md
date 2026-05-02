# v23.8 Introduction

Authoring status: authored

## What This Version Is About

This version introduces runtime operations and autonomy control for AOIS-P.

It does not start an agent runtime. It builds the local policy that decides
which autonomy mode is allowed:

- `disabled`
- `shadow`
- `supervised`
- `limited_autonomous`

The policy includes kill switch, safety event, evaluation, runtime health,
observability, budget, operator approval, and rollback gates.

## Why It Matters In AOIS

v23.5 proved that the connected agent behavior can be evaluated. Runtime
operations decide how much autonomy is allowed when those evaluations and live
signals are healthy.

Without autonomy control, an agent can keep running after an evaluation
regression, safety event, missing observability, exhausted budget, or operator
shutdown. v23.8 turns autonomy into an explicit operating mode.

## How To Use This Version

Work locally and deterministically:

```bash
python3 -m py_compile examples/validate_runtime_autonomy_control_plan.py examples/simulate_runtime_autonomy_control.py
python3 examples/validate_runtime_autonomy_control_plan.py
python3 examples/simulate_runtime_autonomy_control.py
```

Expected outcome:

- validator returns `status: pass`
- validator returns `missing: []`
- simulator passes 10 of 10 autonomy cases
- no agent runtime starts
- no provider call or tool execution happens
