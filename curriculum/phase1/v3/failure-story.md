# v3 Failure Story

Authoring status: authored

## Symptom

A later change made OOMKilled incidents return `unknown`.

## Root Cause

The analyzer behavior changed, but no evaluation baseline was run before accepting the change.

## Fix

Run:

```bash
python3 examples/run_eval_baseline.py
```

Restore the expected `memory-pressure` classification or intentionally update the eval only after defending the behavior change.

## Prevention

Run the baseline before and after changes to analysis, routing, or prompt contracts.

Keep eval cases small, explicit, and tied to AOIS behavior.

## What This Taught Me

Reliability is repeatable evidence.

If the baseline is not run, regressions become surprises.
