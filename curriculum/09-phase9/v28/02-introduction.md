# v28 Introduction

Authoring status: authored

## What This Version Is About

v28 starts Phase 9 by adding delivery pipeline and release controls to AOIS-P.

It models how a change becomes a release candidate and which gates must pass
before AOIS-P promotes, blocks, or holds that release.

## Why It Matters In AOIS

AI systems can fail through shipping discipline, not only through model output.
A policy-aware dashboard is still unsafe if an unreviewed change, unsigned
artifact, missing rollback, unstaged model rollout, or unsafe feature flag can
reach users.

v28 makes release safety part of the AOIS curriculum.

## How To Use This Version

Start with `03-notes.md`, then inspect:

- `release-safety/aois-p/delivery-release-controls.plan.json`
- `examples/validate_delivery_release_controls_plan.py`
- `examples/simulate_delivery_release_controls.py`

Run:

```bash
python3 -m py_compile examples/validate_delivery_release_controls_plan.py examples/simulate_delivery_release_controls.py
python3 examples/validate_delivery_release_controls_plan.py
python3 examples/simulate_delivery_release_controls.py
```

Expected simulator result:

```json
{
  "passed_cases": 16,
  "score": 1.0,
  "status": "pass",
  "total_cases": 16
}
```
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v28 Contents](01-contents.md)
- Next: [v28 - Delivery Pipeline And Release Controls](03-notes.md)
<!-- AOIS-NAV-END -->
