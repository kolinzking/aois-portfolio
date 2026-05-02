# v23.8 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide which autonomy mode is allowed and
which operational action should happen next.

## Primary Checks

1. Confirm the case is in `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm requested and current autonomy modes are recorded.
4. Confirm v23.5 evaluation status is recorded.
5. Confirm safety status is recorded.
6. Confirm budget status is recorded.
7. Confirm observability status is recorded.
8. Confirm runtime health is recorded.
9. Confirm operator approval is recorded for supervised or limited autonomy.
10. Confirm kill switch state is recorded.
11. Confirm rollback signal is recorded.
12. Confirm no live runtime, provider, or tool flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_runtime_autonomy_control_plan.py
python3 examples/simulate_runtime_autonomy_control.py
```

Decision handling:

- `disable_kill_switch`: disable autonomy immediately.
- `emergency_stop_safety_event`: disable autonomy and route to safety response.
- `rollback_on_regression`: roll back to shadow mode.
- `demote_runtime_degraded`: demote to shadow mode.
- `hold_observability_missing`: remain in shadow mode.
- `pause_budget_exhausted`: pause autonomy before spend.
- `allow_shadow_mode`: enter shadow mode.
- `allow_supervised_mode`: enter supervised mode.
- `require_human_approval_for_limited`: request operator approval.
- `allow_limited_autonomy`: enter limited autonomy in policy only.

Escalate to a human operator if:

- kill switch is active
- safety event is active
- evaluation regresses
- observability is missing
- runtime health degrades
- budget reserve is exhausted
- limited autonomy is requested
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23.8 Lab](lab.md)
- Next: [v23.8 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
