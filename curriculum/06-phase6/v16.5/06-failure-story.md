# v16.5 Failure Story

Authoring status: authored

## Symptom

AOIS emits a recommendation, but nobody can tell whether classification, routing, or a future agent step produced the decision.

## Root Cause

Only the final response was logged.

Intermediate step decisions were not traced.

## Fix

Add incident step traces with parent-child relationships, durations, summaries, and decision reasons.

## Prevention

Validate the `v16.5` tracing plan before adding live agent behavior.

Lesson learned: final answers are not enough for operations.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v16.5 Runbook](05-runbook.md)
- Next: [v16.5 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
