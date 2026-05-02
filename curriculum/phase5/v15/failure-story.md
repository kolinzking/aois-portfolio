# v15 Failure Story

Authoring status: authored

## Symptom

An adapted model improves GPU incident wording but misclassifies ordinary operator requests.

## Root Cause

The team optimized for one domain case and skipped regression evaluation.

## Fix

Reject the adapted candidate, expand eval coverage, and resolve regressions before training.

## Prevention

Require baseline, adapted, holdout, and regression evals before live training.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v15 Runbook](runbook.md)
- Next: [v15 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
