# v22 Failure Story

Authoring status: authored

## Symptom

A high-severity investigation requests `read_incident_trace`, which v21 marks
as a sensitive read. The workflow pauses for human approval, but a restart loses
the wait state and the responder tries to continue from the evidence step.

## Root Cause

The agent process treated approval as an in-memory state instead of a durable
checkpoint. After interruption, the workflow did not know whether approval was
missing, granted, expired, or denied.

The deeper issue is missing durability:

- no checkpoint after registry review
- no persisted approval wait state
- no idempotency key for resume
- no terminal timeout path
- no recovery action for incomplete approval

## Fix

Record the approval wait as a durable workflow state:

```bash
python3 examples/simulate_durable_workflow.py
```

The `sensitive_trace_waits_for_approval` case must return:

```text
decision=pause_for_human_approval
state=waiting_for_approval
terminal_status=non_terminal
recovery_action=wait_for_operator_approval
```

Only the `approval_checkpoint_resumes` case should continue after approval is
recorded.

## Prevention

Keep workflow state durable before live execution:

- checkpoint every step
- persist approval waits
- require idempotency keys
- bound retries
- define timeout recovery
- keep registry denials terminal
- never resume sensitive tool work without recorded approval
- keep live workflow engines disabled until durable storage and observability are reviewed
