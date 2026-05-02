# v27 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v27 completes Phase 8. AOIS-P now has:

- dashboard visibility from v26
- policy-aware access from v27
- role-scoped product state
- tenant-scoped resource visibility
- deny-first access behavior
- audited allow and deny decisions

## Why The Next Version Exists

v28 begins Phase 9 by adding delivery pipeline and release controls.

The bridge from v27 to v28 is:

```text
If AOIS-P has product visibility and policy-aware access, the next risk is
shipping changes without enough release safety.
```

v28 will focus on CI/CD, tests in delivery, image signing, release gates,
rollout controls, model rollout control, and feature-flagged AI releases.
