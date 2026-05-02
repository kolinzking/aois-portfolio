# v26 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P dashboard visibility without starting an API
server, frontend runtime, browser, WebSocket server, SSE stream, agent runtime,
execution runtime, tool call, provider call, or network call.

Files:

- `product/aois-p/dashboard-visibility.plan.json`
- `examples/validate_dashboard_visibility_plan.py`
- `examples/simulate_dashboard_visibility.py`

Inspect:

```bash
sed -n '1,900p' product/aois-p/dashboard-visibility.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_dashboard_visibility_plan.py examples/simulate_dashboard_visibility.py
python3 examples/validate_dashboard_visibility_plan.py
python3 examples/simulate_dashboard_visibility.py
```

Expected:

```json
{
  "passed_cases": 13,
  "score": 1.0,
  "status": "pass",
  "total_cases": 13
}
```

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- remove the `approvals` panel
- remove `sequence_number` from required event fields
- change `connection_loss_banner.connection_status` to `connected`
- change `unredacted_payload_blocked.redaction_status` to `redacted`
- change `inaccessible_widget_blocked.accessibility_status` to `pass`
- change `stale_data_warning.event_age_seconds` to `5`

## Explanation Lab

Explain why each case chooses its decision:

- incident update shows overview
- completed trace shows timeline
- registry decision shows route and registry
- orchestration decision shows workflow state
- agent handoff shows autonomy and agent state
- approval request shows approval queue
- budget reserve risk shows budget panel
- execution boundary decision shows boundary panel
- stale event shows stale warning
- no incident shows empty state
- unredacted sensitive payload blocks rendering
- inaccessible widget blocks release readiness
- disconnected stream shows connection-loss banner

## Defense Lab

Defend why v26 uses local event replay instead of a live UI. The dashboard
should first prove which states must be visible, how events map to panels, and
which safety gates block rendering before choosing a frontend implementation.
