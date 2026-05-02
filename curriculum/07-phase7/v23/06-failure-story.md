# v23 Failure Story

Authoring status: authored

## Symptom

An AOIS-P workflow is waiting for approval to read an incident trace. The next
orchestration pass sees that the route is high severity and tries to record an
evidence plan anyway, even though approval is still missing.

## Root Cause

The loop treated route severity as stronger than workflow state. Decision
precedence was wrong: action planning was evaluated before approval waits and
registry stops.

The deeper issue is missing loop governance:

- no ordered decision precedence
- no stop-first policy
- no approval wait guard
- no state hash progress check
- no iteration limit
- no budget reserve stop

## Fix

Use the v23 orchestration policy and simulator:

```bash
python3 examples/simulate_stateful_orchestration.py
```

The `waiting_approval_pauses` case must return:

```text
decision=wait_for_approval
next_action=wait_for_approval
stop_reason=approval_required
```

Only `approval_granted_resumes` should choose `record_evidence_plan`.

## Prevention

Keep stop and wait rules ahead of action rules:

- terminal states stop first
- iteration limits stop before action
- unchanged state hashes stop before action
- budget reserve stops before action
- registry blocks stop before action
- missing approval waits before action
- only granted approval resumes
- no orchestration action executes tools in v23
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23 Runbook](05-runbook.md)
- Next: [v23 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
