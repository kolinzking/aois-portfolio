# v20.1 Runbook

Authoring status: authored

## Purpose

Use this runbook when an AOIS-P agentic responder step or incident has unclear,
incomplete, or excessive cost.

This runbook is for the local training plan only. It does not inspect real
billing, execute tools, or enforce live budgets.

## Primary Checks

1. Confirm the incident is in the `aois-p` namespace.
2. Confirm the primary AOIS project is excluded.
3. Confirm every step has a usage record.
4. Confirm every step has an `accounted` boolean.
5. Confirm model token dimensions are present.
6. Confirm tool usage dimensions are present.
7. Confirm retry count and approval wait minutes are recorded.
8. Confirm the incident total is calculated from step totals.
9. Confirm no runtime, provider, or billing API flag is enabled.

## Recovery Steps

1. Run the validator:

```bash
python3 examples/validate_step_cost_accounting_plan.py
```

2. Run the simulator:

```bash
python3 examples/simulate_step_cost_accounting.py
```

3. If validation fails, fix the missing field or control named in `missing`.
4. If simulation fails, compare `decision` and `expected_decision`.
5. If the total is over budget, inspect `step_costs` to find the largest driver.
6. If accounting is incomplete, restore the missing step record before reviewing totals.
7. If approval wait dominates cost, require operator review before continuing.

Escalate to a human operator if:

- any live runtime flag is enabled
- any provider or billing API call is enabled
- the incident total exceeds the threshold
- a mutation approval loop consumes cost without new evidence
- a cost record is missing but the responder still recommends action
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.1 Lab](04-lab.md)
- Next: [v20.1 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
