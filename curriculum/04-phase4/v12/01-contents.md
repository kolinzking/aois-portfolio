# v12 Contents

Authoring status: authored

## Start Here

Start with [02-introduction.md](02-introduction.md), then work through [03-notes.md](03-notes.md).

This version closes Phase 4 by teaching managed-runtime governance before cloud creation.

The lesson stays local:

- no managed cluster
- no node pool
- no provider identity
- no dashboard
- no budget alarm
- no credentials
- no spend

## Topic Jumps

- Managed runtime governance: [03-notes.md](03-notes.md#what-this-builds)
- IAM boundaries: [03-notes.md](03-notes.md#core-concepts)
- Build commands: [03-notes.md](03-notes.md#build)
- Ops and break labs: [04-lab.md](04-lab.md)
- Recovery path: [05-runbook.md](05-runbook.md)
- Benchmark: [07-benchmark.md](07-benchmark.md)
- Failure story: [06-failure-story.md](06-failure-story.md)
- Phase bridge: [10-next-version-bridge.md](10-next-version-bridge.md)

## Self-Paced Path

1. Read the introduction.
2. Inspect `cloud/aws/managed-runtime-governance.plan.json`.
3. Run `python3 examples/validate_managed_runtime_governance_plan.py`.
4. Complete the ops and break labs.
5. Answer the mastery checkpoint in [03-notes.md](03-notes.md#mastery-checkpoint).
6. Read the Phase 4 closeout in [../zz-phase-end/01-looking-forward.md](../zz-phase-end/01-looking-forward.md).

Do not continue if you cannot explain least privilege, workload identity, observability, cost gates, rollback, and primary AOIS separation.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v12 Start Here](00-start-here.md)
- Next: [v12 Introduction](02-introduction.md)
<!-- AOIS-NAV-END -->
