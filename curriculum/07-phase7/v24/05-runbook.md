# v24 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide whether work should stay with the
supervisor, move to a specialist, stop, block, or escalate to a human operator.

## Primary Checks

1. Confirm the case is in `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm the current agent is recorded.
4. Confirm the requested target is in the role catalog.
5. Confirm the current agent is allowed to route to the target.
6. Confirm autonomy mode is recorded.
7. Confirm shadow mode is plan-only.
8. Confirm context status is fresh.
9. Confirm parallel handoff is not requested.
10. Confirm handoff count is below the limit.
11. Confirm safety status is recorded.
12. Confirm budget status is recorded.
13. Confirm conflict status is recorded.
14. Confirm audit event and trace ID are present.
15. Confirm no live runtime, provider, or tool flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_multi_agent_collaboration_plan.py
python3 examples/simulate_multi_agent_collaboration.py
```

Decision handling:

- `handoff_to_evidence_agent`: request a missing evidence plan.
- `handoff_to_safety_agent`: request safety review.
- `handoff_to_budget_agent`: request budget review.
- `handoff_to_response_agent`: request final response synthesis.
- `block_unknown_agent`: reject the target and review the role catalog.
- `block_parallel_handoff`: serialize collaboration before continuing.
- `block_stale_context`: refresh shared state.
- `escalate_conflict`: route to `human_operator`.
- `stop_handoff_loop`: stop and review the loop.
- `hold_autonomy_mode`: record the proposed handoff without transferring control.

Escalate to a human operator if:

- specialist findings conflict
- the handoff loop repeats
- role ownership is unclear
- state freshness cannot be established
- a target role is missing or unowned
- safety or budget posture is disputed
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v24 Lab](04-lab.md)
- Next: [v24 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
