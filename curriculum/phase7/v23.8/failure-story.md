# v23.8 Failure Story

Authoring status: authored

## Symptom

AOIS-P evaluation regresses after a registry-policy change, but the runtime
continues in `limited_autonomous` mode because the eval signal is recorded only
in a report and not connected to the autonomy gate.

## Root Cause

The system treated evaluation as documentation instead of an operational
control. The autonomy policy did not demote or roll back when v23.5 reported a
failure.

The deeper issue is missing runtime control:

- no evaluation gate
- no rollback mode
- no operator-facing autonomy state
- no kill switch check
- no observability gate
- no safety-event stop path

## Fix

Run the autonomy simulator:

```bash
python3 examples/simulate_runtime_autonomy_control.py
```

The `eval_regression_rolls_back` case must return:

```text
decision=rollback_on_regression
allowed_mode=shadow
next_action=rollback_to_shadow
stop_reason=evaluation_regression
```

## Prevention

Make evaluation and safety signals operational gates:

- evaluation failure rolls back to shadow
- kill switch disables autonomy
- safety events disable autonomy
- missing observability prevents promotion
- budget exhaustion pauses autonomy
- runtime degradation demotes autonomy
- limited autonomy requires explicit operator approval
