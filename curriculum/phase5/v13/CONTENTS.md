# v13 Contents

Authoring status: authored

## Start Here

Start with [introduction.md](introduction.md), then work through [notes.md](notes.md).

This version introduces GPU-backed inference service design without running GPU infrastructure.

Use it to understand the contract and readiness checks before any model download, GPU runtime, driver install, or container build.

## Topic Jumps

- Main lesson: [notes.md](notes.md)
- Build commands: [notes.md](notes.md#build)
- Labs: [lab.md](lab.md)
- Runbook: [runbook.md](runbook.md)
- Benchmark: [benchmark.md](benchmark.md)
- Failure story: [failure-story.md](failure-story.md)
- Next bridge: [next-version-bridge.md](next-version-bridge.md)

## Self-Paced Path

1. Read the introduction.
2. Inspect `inference/aois-p/gpu-inference-service.plan.json`.
3. Run the validator.
4. Run the local inference profile simulator.
5. Complete the ops and break labs.
6. Answer the mastery checkpoint in [notes.md](notes.md#mastery-checkpoint).

Do not continue if you cannot explain latency, throughput, token accounting, model download gates, and fallback routing.
