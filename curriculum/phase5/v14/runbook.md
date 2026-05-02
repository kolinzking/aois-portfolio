# v14 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v14` serving plan to safe no-runtime state.

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_high_throughput_serving_plan.py examples/simulate_high_throughput_serving.py
python3 examples/validate_high_throughput_serving_plan.py
python3 examples/simulate_high_throughput_serving.py
```

Required:

- validator `status=pass`
- simulator `status=pass`
- runtime flags remain false
- model download remains false
- namespace is `aois-p`

## Recovery Steps

If validation fails:

1. Read `missing`.
2. Restore runtime flags to `false`.
3. Restore model download to `false`.
4. Restore serving modes.
5. Restore queue depth to zero.
6. Restore backpressure and load shedding.
7. Restore performance controls.
8. Restore required live checks.
9. Rerun validation.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v14 Lab](lab.md)
- Next: [v14 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
