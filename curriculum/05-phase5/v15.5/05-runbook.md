# v15.5 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v15.5` quantization plan to safe no-runtime state.

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_quantization_plan.py examples/simulate_quantization_tradeoffs.py
python3 examples/validate_quantization_plan.py
python3 examples/simulate_quantization_tradeoffs.py
```

Required:

- validator `status=pass`
- simulator `status=pass`
- no quantization job
- no model download
- no GPU runtime
- no inference runtime

## Recovery Steps

If validation fails:

1. Read `missing`.
2. Restore quantization/runtime flags to `false`.
3. Restore precision options.
4. Restore controls.
5. Restore limits to zero.
6. Restore live checks.
7. Rerun validation.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v15.5 Lab](04-lab.md)
- Next: [v15.5 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
