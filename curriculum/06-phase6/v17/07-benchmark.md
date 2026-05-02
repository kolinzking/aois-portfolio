# v17 Benchmark

Authoring status: authored

## Measurements

Record these values for the checkpoint:

- Validator status: `pass`
- Simulator status: `pass`
- Broker runtime count: `0`
- Producer runtime count: `0`
- Consumer runtime count: `0`
- Simulated event count: `4`
- Consumed offsets: `[0, 1, 2, 3]`
- Replay start offset: `1`
- Replay event count: `3`
- Final lag: `0`
- Dead-letter event count: `0`
- Repo size after checkpoint
- Virtual environment size after checkpoint
- Host memory available after checkpoint

## Interpretation

The benchmark proves that v17 teaches the operational model without spending
runtime resources. A passing validator means the design has the required safety
controls before live deployment. A passing simulator means the learner can
explain event flow, offset progression, replay, lag, and dead-letter handling.

This is not a throughput benchmark. Throughput only matters after a broker is
approved, isolated from the primary project, and given explicit storage,
retention, and monitoring budgets.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17 Failure Story](06-failure-story.md)
- Next: [v17 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
