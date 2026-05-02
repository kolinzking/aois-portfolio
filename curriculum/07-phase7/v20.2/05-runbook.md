# v20.2 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide whether an agentic responder route
should continue, pause for review, downgrade, or stop.

## Primary Checks

1. Confirm the case is in `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm cost accounting is complete.
4. Confirm severity is `low`, `medium`, or `high`.
5. Confirm evidence state is `complete`, `partial`, or `missing`.
6. Confirm confidence is recorded.
7. Confirm remaining budget is recorded.
8. Confirm candidate route costs and expected values are recorded.
9. Confirm runtime, tool, provider, and billing flags are disabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_budget_aware_routing_plan.py
python3 examples/simulate_budget_aware_routing.py
```

Decision handling:

- `route_small_model_no_tool`: use existing evidence and skip tools.
- `route_read_only_tool`: allow one bounded read-only evidence path in plan only.
- `request_budget_review`: pause before expensive non-high-severity spend.
- `stop_budget_exhausted`: stop before violating the reserve.
- `route_high_severity_full_investigation`: allow the full read-only plan shape.
- `block_incomplete_accounting`: restore the cost ledger before routing.

Escalate to a human operator if:

- accounting is incomplete
- selected route is `human_budget_review`
- a non-high-severity route crosses the expensive threshold
- remaining budget cannot preserve reserve
- any live execution flag is enabled
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.2 Lab](04-lab.md)
- Next: [v20.2 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
