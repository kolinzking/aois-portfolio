# v20.1 Introduction

Authoring status: authored

## What This Version Is About

v20 gave AOIS a safe tool-using responder shape. It could plan read-only steps,
block mutation, redact secret-bearing evidence, and decide when more evidence
was required.

v20.1 adds the missing economic view:

```text
incident -> step -> usage -> cost units -> decision
```

This lesson does not use live provider pricing and does not call a billing API.
It uses deterministic provider-neutral `cost_units` so the accounting mechanics
can be tested locally.

## Why It Matters In AOIS

The goal is not to guess a real invoice. The goal is to make every agentic step
visible enough that AOIS can answer:

- how much the incident consumed
- which step consumed it
- whether the cost was justified
- whether repeated tool use was waste
- whether approval waiting became its own cost
- whether accounting records are complete enough to trust

## How To Use This Version

Inspect the new plan and run the deterministic checks:

```bash
python3 -m py_compile examples/validate_step_cost_accounting_plan.py examples/simulate_step_cost_accounting.py
python3 examples/validate_step_cost_accounting_plan.py
python3 examples/simulate_step_cost_accounting.py
```

The new files are:

- `agentic/aois-p/step-cost-accounting.plan.json`
- `examples/validate_step_cost_accounting_plan.py`
- `examples/simulate_step_cost_accounting.py`

This is still AOIS-P only. The primary AOIS system is excluded, no runtime is
started, no tool is executed, no provider call is made, and no billing API is
called.
