# v23 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to choose the next bounded action from a
durable workflow state without letting an agent loop run open-ended.

## Primary Checks

1. Confirm the case is in `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm workflow id, incident id, trace id, and loop id exist.
4. Confirm the current workflow state is recorded.
5. Confirm route decision, registry decision, and approval status are recorded.
6. Confirm iteration and max-iteration values are recorded.
7. Confirm current and previous state hashes are recorded.
8. Confirm remaining budget is above reserve before action.
9. Confirm terminal states stop before actions.
10. Confirm registry blocks stop before action planning.
11. Confirm approval waits stop before evidence planning.
12. Confirm no action executes tools or calls providers.
13. Confirm no live runtime flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_stateful_orchestration_plan.py
python3 examples/simulate_stateful_orchestration.py
```

Decision handling:

- `stop_terminal_state`: leave the workflow closed.
- `stop_iteration_limit`: stop and inspect the loop guard.
- `stop_no_progress`: stop and inspect state hashing.
- `stop_budget_reserve`: stop before further spend.
- `stop_registry_block`: stop and require registry review.
- `wait_for_approval`: wait at the approval boundary.
- `resume_after_approval`: record the evidence plan after approval.
- `plan_read_only_evidence`: record read-only evidence plan only.
- `prepare_answer`: prepare answer from recorded state.
- `close_workflow`: close the workflow.

Escalate to a human operator if:

- a loop hits iteration limit
- a loop repeats without state change
- budget reserve is reached
- a registry block appears after an allowed route
- approval state is ambiguous
- any live runtime flag is enabled
