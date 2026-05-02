# v28 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide whether a release candidate should
be promoted, blocked, or held.

## Primary Checks

1. Confirm the release is for `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm source revision is present.
4. Confirm branch policy and review passed.
5. Confirm workflow permissions are least privilege.
6. Confirm dependency review passed.
7. Confirm build, unit, integration, dashboard, and access-policy checks passed.
8. Confirm AOIS policy regression checks passed.
9. Confirm security scans passed.
10. Confirm artifact digest is present.
11. Confirm build provenance is present.
12. Confirm artifact signature exists and is verified.
13. Confirm environment approval exists.
14. Confirm rollout strategy is controlled.
15. Confirm rollout health is healthy.
16. Confirm rollback is ready.
17. Confirm model rollout is staged.
18. Confirm feature flag state is guarded and reversible.
19. Confirm no CI, build, signing, deploy, rollout, traffic, flag, model, network, or provider runtime flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_delivery_release_controls_plan.py
python3 examples/simulate_delivery_release_controls.py
```

Decision handling:

- `allow_release_candidate`: promote canary.
- `block_unreviewed_branch`: return to code review.
- `block_workflow_overprivileged`: reduce workflow permissions.
- `block_dependency_review_failed`: resolve dependency risk.
- `block_tests_failed`: fix regression tests.
- `block_policy_tests_failed`: fix AOIS policy regressions.
- `block_security_scan_failed`: resolve security findings.
- `block_missing_digest`: produce artifact digest.
- `block_missing_provenance`: produce build provenance.
- `block_unsigned_artifact`: sign release artifact.
- `block_signature_unverified`: verify artifact signature.
- `block_missing_environment_approval`: request environment approval.
- `hold_rollout_health`: pause rollout and investigate health.
- `block_no_rollback`: define rollback target.
- `hold_model_rollout`: stage model rollout.
- `hold_feature_flag`: repair feature-flag guard.

Escalate to a platform or release owner if:

- workflow permissions are broad
- signatures exist but are not verified
- release evidence does not identify the artifact
- rollout health is degraded
- rollback is missing
- model rollout or feature flags cannot be reversed
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v28 Lab](lab.md)
- Next: [v28 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
