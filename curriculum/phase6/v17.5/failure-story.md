# v17.5 Failure Story

Authoring status: authored

## Symptom

The AOIS API dashboard looks healthy. Requests return 200, latency is fine, and
the incident endpoint appears available. Operators still report that the agent
is giving weak or unsafe recommendations.

## Root Cause

AOIS only measured service availability. It did not define an agent quality SLO
or safety gate. The agent could produce a successful HTTP response even when
the recommendation failed the real operational goal.

## Fix

Define `valid_recommendation_ratio` for `aois-p-incident-agent`, require schema,
quality, and safety checks, and burn the agent error budget when those checks
fail. Route destructive or low-trust actions to human review.

## Prevention

Prevent recurrence by requiring:

- service SLOs for availability, latency, and freshness
- agent SLOs for quality and safety
- burn-rate alerts
- error-budget policy
- human review gates for destructive action
- post-incident review when trust is lost

An AI infrastructure system is not reliable just because its HTTP layer is up.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17.5 Runbook](runbook.md)
- Next: [v17.5 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
