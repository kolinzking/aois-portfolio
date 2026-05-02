# v28 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P delivery release controls without starting CI,
running a workflow, building a container, pushing an image, signing an artifact,
deploying to Kubernetes, shifting traffic, calling a feature-flag service,
changing a model endpoint, calling a provider, or using the network.

Files:

- `release-safety/aois-p/delivery-release-controls.plan.json`
- `examples/validate_delivery_release_controls_plan.py`
- `examples/simulate_delivery_release_controls.py`

Inspect:

```bash
sed -n '1,760p' release-safety/aois-p/delivery-release-controls.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_delivery_release_controls_plan.py examples/simulate_delivery_release_controls.py
python3 examples/validate_delivery_release_controls_plan.py
python3 examples/simulate_delivery_release_controls.py
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

- remove `release_gate` from `pipeline_stages`
- remove `signature_verification_review` from live release checks
- change `case_defaults.workflow_permissions` to `write_all`
- change `missing_provenance_blocked.overrides.provenance_status` to `present`
- change `degraded_health_holds_rollout.overrides.health_status` to `healthy`
- change `model_rollout_unstaged_held.overrides.model_rollout_status` to `staged`

## Explanation Lab

Explain why each case chooses its decision:

- fully gated release candidate promotes canary
- unreviewed branch blocks
- overprivileged workflow blocks
- failed dependency review blocks
- failed tests block
- failed AOIS policy tests block
- failed security scan blocks
- missing digest blocks
- missing provenance blocks
- unsigned artifact blocks
- unverified signature blocks
- missing environment approval blocks
- degraded health holds rollout
- missing rollback blocks
- unstaged model rollout holds
- unsafe feature flag holds

## Defense Lab

Defend why v28 models release controls locally before creating a real CI/CD
workflow. The system should prove gate logic, expected release evidence, and
AI behavior rollout controls before any automation can deploy or mutate live
state.
