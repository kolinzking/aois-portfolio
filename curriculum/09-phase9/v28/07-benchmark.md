# v28 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_delivery_release_controls_plan.py examples/simulate_delivery_release_controls.py
python3 examples/validate_delivery_release_controls_plan.py
python3 examples/simulate_delivery_release_controls.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- CI, workflow, build, signing, deployment, rollout, traffic, feature flag, model, network, and provider flags

## Interpretation

Pass means:

- release scope is local and AOIS-P only
- pipeline stages are complete
- source, workflow, test, policy, security, artifact, provenance, signature, approval, rollout, rollback, model, and flag controls are represented
- every release decision has a case
- no live delivery runtime is enabled

Fail means the release-control contract is incomplete. Fix the plan or
simulator before adding experiment and model delivery tracking in v29.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v28 Failure Story](06-failure-story.md)
- Next: [v28 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
