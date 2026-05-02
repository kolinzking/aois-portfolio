# v9 Failure Story

Authoring status: authored

## Symptom

Autoscaling creates more pods and memory pressure returns.

## Root Cause

Max replicas were raised without resource budget or dependency-capacity review.

## Fix

Cap replicas and require approval before live autoscaling:

```yaml
maxReplicas: 1
```

## Prevention

Validate autoscaling plans before applying.

Record resource impact for every scaling change.

## What This Taught Me

Autoscaling is controlled resource multiplication.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v9 Runbook](runbook.md)
- Next: [v9 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
