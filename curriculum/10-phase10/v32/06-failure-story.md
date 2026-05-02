# v32 Failure Story

Authoring status: authored

## Symptom

An operations team deploys a local inference package to a gateway at a remote
site. The central service is slow during peak incidents, so the team wants the
gateway to keep working when the network drops.

The first offline incident looks successful. The gateway produces a
recommendation, the operator follows it, and the local dashboard records a
decision. After connectivity returns, central reviewers discover that the
cached model was two releases behind the approved version and telemetry from
the offline window was lost.

## Root Cause

The deployment treated offline inference as ordinary edge inference without a
network. It did not prove model freshness, telemetry buffering, signed update
channel, rollback readiness, privacy state, residency compliance, or release
approval for the cached package.

## Fix

v32 fixes the failure by requiring:

- known device profile
- model size, memory, compute, power, and latency budgets
- cache readiness
- sync policy
- model freshness indicator
- data residency and privacy gates
- observability buffer
- update channel
- rollback readiness
- access and release gates

## Prevention

Do not approve live edge or offline inference until the placement decision can
explain which model is running, why it fits the device, how stale state is
detected, where telemetry is buffered, how updates arrive, how rollback works,
and whether fallback is allowed.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v32 Runbook](05-runbook.md)
- Next: [v32 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
