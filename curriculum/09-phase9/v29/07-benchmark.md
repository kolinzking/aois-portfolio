# v29 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_experiment_model_delivery_plan.py examples/simulate_experiment_model_delivery.py
python3 examples/validate_experiment_model_delivery_plan.py
python3 examples/simulate_experiment_model_delivery.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- tracker, registry, training, eval, model, rollout, feature flag, network, and provider flags

## Interpretation

Pass means:

- experiment tracking scope is local and AOIS-P only
- metric catalog is complete
- evidence stages are complete
- every model-delivery decision has a case
- missing experiment, version, dataset, metric, guardrail, rollout, registry, release, flag, rollback, approval, and risk evidence blocks or holds correctly
- no live model-delivery runtime is enabled

Fail means the model-delivery tracking contract is incomplete. Fix the plan or
simulator before adding internal platform patterns in v30.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v29 Failure Story](06-failure-story.md)
- Next: [v29 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
