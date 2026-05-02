# v14.5 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v14.5` caching plan to safe no-runtime state.

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_performance_caching_plan.py examples/simulate_performance_caching.py
python3 examples/validate_performance_caching_plan.py
python3 examples/simulate_performance_caching.py
```

Required:

- validator `status=pass`
- simulator `status=pass`
- cache service is not started
- Redis is not installed
- no cache entries exist
- namespace is `aois-p`

## Recovery Steps

If validation fails:

1. Read `missing`.
2. Restore cache/runtime flags to `false`.
3. Restore cache layers.
4. Restore cache policy controls.
5. Restore batching tradeoff controls.
6. Restore live checks.
7. Rerun validation.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v14.5 Lab](lab.md)
- Next: [v14.5 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
