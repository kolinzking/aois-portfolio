# v16 Failure Story

Authoring status: authored

## Symptom

AOIS latency increases, but the team cannot connect the slow route decision to the logs and metrics for the same request.

## Root Cause

Trace IDs were not included consistently across logs, metrics, and traces.

## Fix

Add shared correlation fields and validate the telemetry plan before runtime instrumentation.

## Prevention

Require trace, span, request, incident, and route identifiers before live telemetry deployment.

Lesson learned: observability starts with correlation design.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v16 Runbook](05-runbook.md)
- Next: [v16 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
