# v29 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide whether a model or AI behavior
candidate should be promoted, blocked, or held.

## Primary Checks

1. Confirm the decision is for `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm experiment ID is present.
4. Confirm hypothesis is documented.
5. Confirm baseline model version is present.
6. Confirm candidate model version is present.
7. Confirm dataset version is pinned.
8. Confirm offline evaluation passed.
9. Confirm quality, latency, and cost deltas meet thresholds.
10. Confirm safety violation rate is zero.
11. Confirm policy regression count is zero.
12. Confirm tenant isolation failures are zero.
13. Confirm rollout sample size is sufficient.
14. Confirm rollout evidence is complete.
15. Confirm model registry record is complete.
16. Confirm v28 release gate passed.
17. Confirm feature flag state is guarded.
18. Confirm rollback target is ready.
19. Confirm approval is recorded.
20. Confirm risk review is accepted.
21. Confirm no tracker, registry, training, eval, rollout, flag, network, or provider runtime flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_experiment_model_delivery_plan.py
python3 examples/simulate_experiment_model_delivery.py
```

Decision handling:

- `allow_model_delivery_candidate`: promote challenger with evidence.
- `block_missing_hypothesis`: document experiment hypothesis.
- `block_missing_baseline`: set baseline model version.
- `block_missing_candidate_version`: set candidate model version.
- `block_missing_dataset_version`: pin evaluation dataset version.
- `block_offline_eval_failed`: fix or rerun offline evaluation.
- `block_metric_regression`: investigate metric regression.
- `block_guardrail_regression`: fix guardrail regression.
- `hold_sample_size_insufficient`: collect more rollout samples.
- `hold_missing_rollout_evidence`: collect rollout evidence.
- `block_registry_incomplete`: complete model registry record.
- `block_release_gate_failed`: return to release gate.
- `hold_feature_flag_not_ready`: repair feature-flag guard.
- `block_no_rollback`: define model rollback target.
- `block_missing_approval`: request model delivery approval.
- `hold_risk_review`: complete risk review.

Escalate to a model, platform, or risk owner if:

- a candidate has no baseline
- a dataset version is missing
- guardrail metrics regress
- rollout evidence is incomplete
- registry state cannot identify the candidate
- rollback or feature-flag controls are not reversible
