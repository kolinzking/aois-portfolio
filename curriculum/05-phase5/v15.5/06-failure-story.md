# v15.5 Failure Story

Authoring status: authored

## Symptom

An INT4 artifact fits memory but produces worse incident recommendations.

## Root Cause

The team optimized footprint and skipped task regression evaluation.

## Fix

Roll back to FP16 or INT8 and rerun quality evals.

## Prevention

Require quality eval, task regression eval, and fallback precision before using lower precision.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v15.5 Runbook](05-runbook.md)
- Next: [v15.5 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
