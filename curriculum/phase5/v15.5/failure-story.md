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
