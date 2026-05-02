# v22 Lab

Authoring status: authored

## Build Lab

Validate and simulate durable AOIS-P agent workflows without starting a workflow
runtime, creating a durable store, starting MCP, executing tools, or calling a
provider.

Files:

- `agentic/aois-p/durable-workflow.plan.json`
- `examples/validate_durable_workflow_plan.py`
- `examples/simulate_durable_workflow.py`

Inspect:

```bash
sed -n '1,620p' agentic/aois-p/durable-workflow.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_durable_workflow_plan.py examples/simulate_durable_workflow.py
python3 examples/validate_durable_workflow_plan.py
python3 examples/simulate_durable_workflow.py
```

Expected:

```json
{
  "passed_cases": 8,
  "score": 1.0,
  "status": "pass",
  "total_cases": 8
}
```

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- remove `checkpoint_required` from a step
- set `wait_for_approval.timeout_seconds` to a negative number
- remove `timed_out` from `terminal_states`
- change an approval case from `required_missing` to `granted`
- set `idempotency_key_seen` to `false` in the duplicate case
- remove `retry_budget_review` from `required_before_live_workflow`

## Explanation Lab

Explain why each case chooses its decision:

- no-tool routes complete directly
- read-only registry plans complete without tool execution
- sensitive tools pause for approval
- approval checkpoints resume
- registry denials block workflows
- transient step failures recover inside retry budget
- timeouts become terminal states
- duplicate idempotency keys reuse existing checkpoints

## Defense Lab

Defend why v22 does not start a workflow engine. Durable workflows introduce
state, persistence, approval waits, retries, and timeouts. AOIS-P first proves
the workflow contract locally before adding a runtime and durable store.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v22 - Durable Agent Workflows](notes.md)
- Next: [v22 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
