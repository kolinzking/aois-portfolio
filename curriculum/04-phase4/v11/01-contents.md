# v11 Contents

Authoring status: authored

## Start Here

Start with [02-introduction.md](02-introduction.md), then work through [03-notes.md](03-notes.md).

This version teaches event-driven workflow planning without creating cloud resources.

The core question is:

How can AOIS move work through ingress, queue, worker, DLQ, and result sink while staying safe, traceable, and separate from the primary AOIS project?

## Topic Jumps

- Event workflow plan: [03-notes.md](03-notes.md#what-this-builds)
- Core concepts: [03-notes.md](03-notes.md#core-concepts)
- Build commands: [03-notes.md](03-notes.md#build)
- Lab path: [04-lab.md](04-lab.md)
- Recovery steps: [05-runbook.md](05-runbook.md)
- Benchmark: [07-benchmark.md](07-benchmark.md)
- Failure story: [06-failure-story.md](06-failure-story.md)
- Bridge to next version: [10-next-version-bridge.md](10-next-version-bridge.md)

## Self-Paced Path

1. Read the introduction.
2. Inspect `cloud/aws/event-workflow.plan.json`.
3. Run `python3 examples/validate_event_workflow_plan.py`.
4. Complete the build, ops, and break labs.
5. Answer the mastery checkpoint in [03-notes.md](03-notes.md#mastery-checkpoint).
6. Check the answer key.

Do not continue if you cannot explain idempotency, DLQ, trace propagation, and why live cloud limits are zero.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v11 Start Here](00-start-here.md)
- Next: [v11 Introduction](02-introduction.md)
<!-- AOIS-NAV-END -->
