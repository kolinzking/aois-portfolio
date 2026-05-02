# v32 Lab

Authoring status: authored

## Build Lab

Run:

```bash
python3 -m py_compile examples/validate_edge_offline_inference_plan.py examples/simulate_edge_offline_inference.py
python3 examples/validate_edge_offline_inference_plan.py
python3 examples/simulate_edge_offline_inference.py
```

Expected simulator summary:

```json
{
  "passed_cases": 18,
  "score": 1.0,
  "status": "pass",
  "total_cases": 18
}
```

## Ops Lab

Open `frontier/aois-p/edge-offline-inference.plan.json`.

Find `deployment_targets` and answer:

- what must be true for `central_cloud`
- what dominates `edge_online`
- what dominates `offline_edge`
- why offline inference is not just edge inference without a network

Find `device_profiles` and record each profile's model size, memory, latency,
quantization, and power constraints.

## Break Lab

Change one value at a time, run the simulator, then restore it:

- set `model_size_mb` above `model_size_budget_mb`
- set `memory_mb` above `memory_budget_mb`
- set `model_freshness_status` to `stale`
- set `observability_status` to `missing`
- set `rollback_ready` to `false`

For each change, record the decision and operator action.

## Explanation Lab

Explain why `compute_budget_review_held` is different from
`edge_constraint_routes_to_central_fallback`.

Explain why fallback is governed by residency, privacy, access, release, and
connectivity.

## Defense Lab

Defend these choices:

- unknown device profiles block
- offline execution requires cache, sync, freshness, and telemetry buffers
- update channel and rollback are mandatory before live edge deployment
- v32 models placement without loading a model or touching hardware
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v32 - Edge And Offline Inference](03-notes.md)
- Next: [v32 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
