# v32 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_edge_offline_inference_plan.py examples/simulate_edge_offline_inference.py
python3 examples/validate_edge_offline_inference_plan.py
python3 examples/simulate_edge_offline_inference.py
```

Expected validator result:

```json
{
  "missing": [],
  "mode": "edge_offline_inference_plan_no_runtime",
  "namespace": "aois-p",
  "plan": "frontier/aois-p/edge-offline-inference.plan.json",
  "status": "pass"
}
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

## Interpretation

The benchmark covers central allow, edge allow, offline allow, unknown device
block, model size block, memory block, compute hold, power hold, latency block,
cache hold, stale model hold, residency block, privacy block, central fallback,
observability hold, update block, rollback block, and policy block.

v32 passes only when validator status is `pass`, simulator status is `pass`, 18
of 18 cases pass, score is `1.0`, runtime boundary flags remain false, and no
placeholder marker remains in the v32 lesson pack.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v32 Failure Story](failure-story.md)
- Next: [v32 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
