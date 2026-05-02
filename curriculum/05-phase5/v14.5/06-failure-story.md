# v14.5 Failure Story

Authoring status: authored

## Symptom

A user receives an old incident recommendation after the source incident changed.

## Root Cause

The response cache had no TTL or invalidation policy.

## Fix

Disable the response cache, purge stale entries, define TTL and invalidation rules, then retest.

## Prevention

Validate cache policy before live writes.

Lesson learned: cache speed is useful only when cached data is still correct.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v14.5 Runbook](05-runbook.md)
- Next: [v14.5 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
