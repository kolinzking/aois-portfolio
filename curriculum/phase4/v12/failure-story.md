# v12 Failure Story

Authoring status: authored

## Symptom

A managed runtime appears in the provider account with unclear ownership. Costs increase overnight and operators cannot tell whether it belongs to primary AOIS or the portfolio.

## Root Cause

The runtime was created before governance existed.

There was no `aois-p` naming, no budget approval, no cost alarm, no workload identity review, and no primary AOIS separation review.

## Fix

Stop creating new runtime resources.

Quarantine or remove the unmanaged resource after approval.

Restore governance controls:

- `aois-p` naming
- budget approval gate
- cost alarms
- IAM least privilege
- workload identity
- observability
- rollback plan
- primary AOIS separation review

## Prevention

Run the `v12` validator before live runtime work.

Do not approve live cloud execution until governance exists and the portfolio cannot be confused with primary AOIS.

Lesson learned: managed runtime without governance is still unmanaged risk.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v12 Runbook](runbook.md)
- Next: [v12 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
