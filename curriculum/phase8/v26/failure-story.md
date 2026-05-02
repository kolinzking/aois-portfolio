# v26 Failure Story

Authoring status: authored

## Symptom

AOIS-P blocks an unsafe execution request, but the dashboard still shows only
the incident overview. The operator believes nothing is waiting and opens a
manual change outside AOIS-P.

## Root Cause

The product surface treated execution-boundary state as backend detail instead
of operator state. The dashboard had no dedicated panel, badge, or next action
for blocked execution.

## Fix

v26 fixes this by requiring:

- an execution-boundary panel
- event-to-panel routing
- status badges
- operator actions
- stale-state warnings
- redaction checks
- accessibility checks
- connection-loss handling

## Prevention

Before building a live frontend, prove the visibility contract:

```bash
python3 examples/validate_dashboard_visibility_plan.py
python3 examples/simulate_dashboard_visibility.py
```

Then review every new backend event for panel mapping, badge, operator action,
redaction, accessibility, and stale-state behavior.
