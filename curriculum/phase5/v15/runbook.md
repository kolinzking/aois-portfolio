# v15 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v15` adaptation plan to safe no-training state.

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_fine_tuning_plan.py examples/simulate_adaptation_eval.py
python3 examples/validate_fine_tuning_plan.py
python3 examples/simulate_adaptation_eval.py
```

Required:

- validator `status=pass`
- simulator `status=pass`
- no training job
- no dataset upload
- no model download
- no GPU runtime

## Recovery Steps

If validation fails:

1. Read `missing`.
2. Restore training and upload flags to `false`.
3. Restore adaptation options.
4. Restore dataset controls.
5. Restore eval controls.
6. Restore limits to zero.
7. Restore required live checks.
