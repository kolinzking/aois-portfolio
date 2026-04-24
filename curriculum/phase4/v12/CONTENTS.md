# v12 Contents

Authoring status: authored

## Start Here

Start with [introduction.md](introduction.md), then work through [notes.md](notes.md).

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

- Managed runtime governance: [notes.md](notes.md#what-this-builds)
- IAM boundaries: [notes.md](notes.md#core-concepts)
- Build commands: [notes.md](notes.md#build)
- Ops and break labs: [lab.md](lab.md)
- Recovery path: [runbook.md](runbook.md)
- Benchmark: [benchmark.md](benchmark.md)
- Failure story: [failure-story.md](failure-story.md)
- Phase bridge: [next-version-bridge.md](next-version-bridge.md)

## Self-Paced Path

1. Read the introduction.
2. Inspect `cloud/aws/managed-runtime-governance.plan.json`.
3. Run `python3 examples/validate_managed_runtime_governance_plan.py`.
4. Complete the ops and break labs.
5. Answer the mastery checkpoint in [notes.md](notes.md#mastery-checkpoint).
6. Read the Phase 4 closeout in [../looking-forward.md](../looking-forward.md).

Do not continue if you cannot explain least privilege, workload identity, observability, cost gates, rollback, and primary AOIS separation.
