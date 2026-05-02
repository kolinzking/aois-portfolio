# v32 Runbook

Authoring status: authored

## Purpose

Use this runbook when reviewing an AOIS-P edge or offline inference proposal.
The runbook is for local planning only. It does not approve live model loading,
device access, media capture, provider calls, or network calls.

## Primary Checks

Confirm:

- `primary_aois_excluded` is true
- `edge_runtime_started` is false
- `offline_model_loaded` is false
- `model_runtime_started` is false
- `device_accessed` is false
- `network_call_made` is false
- `provider_call_made` is false
- `approved_for_live_edge` is false

Review:

- deployment target and connectivity
- known device profile
- model format, model size, quantization review, memory, compute, power, and latency budgets
- cache, sync, freshness, and observability buffer for offline or degraded operation
- data residency and privacy state
- fallback eligibility
- update channel and rollback readiness
- access policy and release gate

## Recovery Steps

If an edge path fails:

- route to central fallback only when connectivity, residency, privacy, access, and release controls allow it
- hold for measurement or preparation when the issue is incomplete evidence
- block when the issue is policy, safety, rollback, update, size, memory, latency, residency, or privacy

If an offline edge path produced an unexpected result:

- identify the cached model version
- check model freshness
- inspect sync backlog
- inspect local telemetry buffer state
- verify update channel and rollback readiness
- verify whether central fallback was eligible at the time
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v32 Lab](04-lab.md)
- Next: [v32 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
