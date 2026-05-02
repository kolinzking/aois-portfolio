# v29 Introduction

Authoring status: authored

## What This Version Is About

v29 adds experiment and model delivery tracking to AOIS-P.

v28 answered whether a release candidate should promote, block, or hold. v29
answers whether the AI behavior change has enough experiment, comparison, and
rollout evidence to justify delivery.

## Why It Matters In AOIS

Model and prompt behavior changes can fail even when code release controls are
healthy. A candidate can improve one quality score while regressing latency,
cost, safety, policy behavior, or tenant isolation.

AOIS-P needs traceable evidence for why a model or behavior change was
accepted, blocked, or held.

## How To Use This Version

Start with `notes.md`, then inspect:

- `release-safety/aois-p/experiment-model-delivery.plan.json`
- `examples/validate_experiment_model_delivery_plan.py`
- `examples/simulate_experiment_model_delivery.py`

Run:

```bash
python3 -m py_compile examples/validate_experiment_model_delivery_plan.py examples/simulate_experiment_model_delivery.py
python3 examples/validate_experiment_model_delivery_plan.py
python3 examples/simulate_experiment_model_delivery.py
```

Expected simulator result:

```json
{
  "passed_cases": 16,
  "score": 1.0,
  "status": "pass",
  "total_cases": 16
}
```
