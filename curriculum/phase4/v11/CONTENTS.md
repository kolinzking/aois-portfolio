# v11 Contents

Authoring status: authored

## Start Here

Start with [introduction.md](introduction.md), then work through [notes.md](notes.md).

This version teaches event-driven workflow planning without creating cloud resources.

The core question is:

How can AOIS move work through ingress, queue, worker, DLQ, and result sink while staying safe, traceable, and separate from the primary AOIS project?

## Topic Jumps

- Event workflow plan: [notes.md](notes.md#what-this-builds)
- Core concepts: [notes.md](notes.md#core-concepts)
- Build commands: [notes.md](notes.md#build)
- Lab path: [lab.md](lab.md)
- Recovery steps: [runbook.md](runbook.md)
- Benchmark: [benchmark.md](benchmark.md)
- Failure story: [failure-story.md](failure-story.md)
- Bridge to next version: [next-version-bridge.md](next-version-bridge.md)

## Self-Paced Path

1. Read the introduction.
2. Inspect `cloud/aws/event-workflow.plan.json`.
3. Run `python3 examples/validate_event_workflow_plan.py`.
4. Complete the build, ops, and break labs.
5. Answer the mastery checkpoint in [notes.md](notes.md#mastery-checkpoint).
6. Check the answer key.

Do not continue if you cannot explain idempotency, DLQ, trace propagation, and why live cloud limits are zero.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v11 Start Here](00-start-here.md)
- Next: [v11 Introduction](introduction.md)
<!-- AOIS-NAV-END -->
