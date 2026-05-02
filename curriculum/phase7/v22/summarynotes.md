# v22 Summary Notes

Authoring status: authored

## What Was Built

A local durable agent workflow plan and deterministic simulator:

- `agentic/aois-p/durable-workflow.plan.json`
- `examples/validate_durable_workflow_plan.py`
- `examples/simulate_durable_workflow.py`

## What Was Learned

Agent work needs durable state before it can be trusted. AOIS-P must record the
route decision, registry decision, approval state, retry budget, timeout,
checkpoint, idempotency key, and recovery action for each workflow.

The core workflow outcomes are:

- complete
- pause for approval
- resume after approval
- block on registry denial
- recover after retry
- fail on timeout
- skip duplicate work by idempotency key

## Core Limitation Or Tradeoff

v22 intentionally does not run a workflow engine or create a durable store. It
proves the state model first. Live execution would require resource review,
persistence design, observability, audit sinks, approval UX, and integration
tests with the v20.2 router and v21 registry.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v22 Benchmark](benchmark.md)
- Next: [v22 Looking Forward](looking-forward.md)
<!-- AOIS-NAV-END -->
