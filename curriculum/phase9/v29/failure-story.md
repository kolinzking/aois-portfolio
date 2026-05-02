# v29 Failure Story

Authoring status: authored

## Symptom

A model alias is promoted after one offline quality score improves. Two days
later, operators see higher latency, higher cost, and tenant-isolation alerts.
No one can tell which dataset version was used, which baseline was compared,
or what rollout evidence justified the change.

## Root Cause

The team tracked the model name but not the delivery evidence. The experiment
had no documented hypothesis, the baseline version was implicit, the dataset
version was not pinned, guardrail metrics were not release blockers, rollout
sample size was unknown, feature-flag state was not recorded, and risk review
was pending.

## Fix

v29 fixes the failure with an experiment and model-delivery tracking contract:

- experiment ID and hypothesis
- baseline and candidate versions
- dataset version
- metric catalog
- guardrail metrics
- offline evaluation evidence
- rollout evidence and sample size
- model registry record
- release gate link
- feature flag link
- rollback target
- approval and risk review

## Prevention

Before live model delivery:

- review experiment tracking
- review model registry fields
- review dataset versioning
- review metric and guardrail catalogs
- review offline evaluation
- review sample size and rollout evidence
- review release gate and feature flag links
- rehearse rollback
- record approval and risk review
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v29 Runbook](runbook.md)
- Next: [v29 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
