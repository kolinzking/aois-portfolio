# v20.2 Summary Notes

Authoring status: authored

## What Was Built

- A provider-neutral budget-aware routing plan.
- A validator for route policy controls.
- A simulator covering six routing decisions.
- Deterministic thresholds for confidence, budget reserve, severity, review, and value-to-cost ratio.
- Progress updates that move Phase 7 to v20.2.

## What Was Learned

Cost accounting becomes useful when it changes the next decision.

v20.2 teaches AOIS to choose smaller, bounded, reviewed, stopped, or full routes
based on severity, confidence, evidence state, remaining budget, and expected
value.

## Core Limitation Or Tradeoff

The selected route is not executed. That is intentional. Execution requires
governed tools, ownership, schemas, approval boundaries, observability, and live
budget reconciliation.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.2 Benchmark](07-benchmark.md)
- Next: [v20.2 Looking Forward](09-looking-forward.md)
<!-- AOIS-NAV-END -->
