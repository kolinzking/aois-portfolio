# v13 Contents

Authoring status: authored

## Start Here

Start with [02-introduction.md](02-introduction.md), then work through [03-notes.md](03-notes.md).

This version introduces GPU-backed inference service design without running GPU infrastructure.

Use it to understand the contract and readiness checks before any model download, GPU runtime, driver install, or container build.

## Topic Jumps

- Main lesson: [03-notes.md](03-notes.md)
- Build commands: [03-notes.md](03-notes.md#build)
- Labs: [04-lab.md](04-lab.md)
- Runbook: [05-runbook.md](05-runbook.md)
- Benchmark: [07-benchmark.md](07-benchmark.md)
- Failure story: [06-failure-story.md](06-failure-story.md)
- Next bridge: [10-next-version-bridge.md](10-next-version-bridge.md)

## Self-Paced Path

1. Read the introduction.
2. Inspect `inference/aois-p/gpu-inference-service.plan.json`.
3. Run the validator.
4. Run the local inference profile simulator.
5. Complete the ops and break labs.
6. Answer the mastery checkpoint in [03-notes.md](03-notes.md#mastery-checkpoint).

Do not continue if you cannot explain latency, throughput, token accounting, model download gates, and fallback routing.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v13 Start Here](00-start-here.md)
- Next: [v13 Introduction](02-introduction.md)
<!-- AOIS-NAV-END -->
