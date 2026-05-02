# v29 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P experiment and model delivery tracking without
starting an experiment tracker, model registry, training job, eval job, rollout
controller, feature-flag service, provider call, or network call.

Files:

- `release-safety/aois-p/experiment-model-delivery.plan.json`
- `examples/validate_experiment_model_delivery_plan.py`
- `examples/simulate_experiment_model_delivery.py`

Inspect:

```bash
sed -n '1,760p' release-safety/aois-p/experiment-model-delivery.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_experiment_model_delivery_plan.py examples/simulate_experiment_model_delivery.py
python3 examples/validate_experiment_model_delivery_plan.py
python3 examples/simulate_experiment_model_delivery.py
```

Expected:

```json
{
  "passed_cases": 16,
  "score": 1.0,
  "status": "pass",
  "total_cases": 16
}
```

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- remove `tenant_isolation_failures` from `metric_catalog`
- remove `rollout_evidence` from `evidence_stages`
- change `case_defaults.baseline_model_version` to an empty string
- change `metric_regression_blocked.overrides.metric_delta.quality_score` to `0.05`
- change `guardrail_regression_blocked.overrides.metric_delta.policy_regression_count` to `0`
- change `risk_review_pending_held.overrides.risk_status` to `accepted`

## Explanation Lab

Explain why each case chooses its decision:

- fully evidenced candidate promotes
- missing hypothesis blocks
- missing baseline blocks
- missing candidate version blocks
- missing dataset version blocks
- failed offline evaluation blocks
- metric regression blocks
- guardrail regression blocks
- insufficient sample size holds
- missing rollout evidence holds
- incomplete registry blocks
- failed release gate blocks
- unsafe feature flag holds
- missing rollback blocks
- missing approval blocks
- pending risk review holds

## Defense Lab

Defend why v29 models experiment tracking locally before starting a real
tracking server or registry. The system should prove evidence requirements and
decision behavior before any model promotion, rollout, or feature-flag mutation
can affect users.
