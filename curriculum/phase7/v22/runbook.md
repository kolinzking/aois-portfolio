# v22 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide how an agentic incident workflow
should continue, pause, resume, recover, block, or time out.

## Primary Checks

1. Confirm the case is in `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm a workflow id, incident id, and trace id exist.
4. Confirm the v20.2 route decision is recorded.
5. Confirm the v21 registry decision is recorded.
6. Confirm every step has an owner.
7. Confirm every step checkpoints.
8. Confirm idempotency keys exist.
9. Confirm retry budgets are bounded.
10. Confirm timeout policy exists.
11. Confirm approval waits have a timeout and recovery action.
12. Confirm terminal states include `completed`, `blocked`, `failed`, and `timed_out`.
13. Confirm no workflow runtime, durable store, MCP server, tool call, or provider call is active.

## Recovery Steps

Run:

```bash
python3 examples/validate_durable_workflow_plan.py
python3 examples/simulate_durable_workflow.py
```

Decision handling:

- `complete_no_tool_workflow`: close from existing evidence.
- `complete_read_only_workflow_plan`: record the tool plan only.
- `pause_for_human_approval`: wait at the approval checkpoint.
- `resume_after_approval`: continue from the approval checkpoint.
- `block_registry_denial`: stop and require registry review.
- `recover_after_retry`: retry once and checkpoint the successful result.
- `fail_timeout`: mark a terminal timeout for operator review.
- `skip_duplicate_step`: reuse the previous checkpoint and avoid repeat work.

Escalate to a human operator if:

- an approval wait exceeds timeout
- retry budget is exhausted
- a registry block is terminal
- idempotency collision is ambiguous
- workflow state and checkpoint state disagree
- any live runtime flag is enabled
