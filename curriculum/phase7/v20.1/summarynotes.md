# v20.1 Summary Notes

Authoring status: authored

## What Was Built

- A provider-neutral cost accounting plan.
- Per-step usage records.
- Per-incident cost totals.
- Deterministic unit costs.
- Validation for cost controls and usage dimensions.
- Simulation for five cost decisions.
- Disabled runtime, tool, provider, billing, and persistence paths.

## What Was Learned

Cost accounting is an agent safety control.

If AOIS cannot explain what an agentic incident response consumed, it cannot
decide whether the response should continue, route differently, or stop.

Decision gates:

- `within_budget`
- `step_waste_flagged`
- `incident_budget_exceeded`
- `accounting_incomplete`
- `approval_cost_review`

## Core Limitation Or Tradeoff

`cost_units` are training units, not dollars.

The accounting model is useful because it is deterministic, auditable, and
testable. Real enforcement needs live pricing review, reconciliation, budget
ownership, and operator dashboards before it is safe.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.1 Benchmark](benchmark.md)
- Next: [v20.1 Looking Forward](looking-forward.md)
<!-- AOIS-NAV-END -->
