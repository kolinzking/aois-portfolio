# v26 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide which dashboard panel, badge, and
operator action should be shown for the latest operational event.

## Primary Checks

1. Confirm the case is in `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm incident ID and trace ID are present.
4. Confirm latest event type is supported.
5. Confirm event ordering and dedupe fields are defined.
6. Confirm connection status is recorded.
7. Confirm event age and freshness budget are recorded.
8. Confirm sensitive payloads are redacted before render.
9. Confirm accessibility status is pass before release readiness.
10. Confirm empty state exists when no incidents are in scope.
11. Confirm active panel is one of the panel catalog entries.
12. Confirm status badge and operator action are explicit.
13. Confirm no API, frontend, browser, stream, provider, tool, or network flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_dashboard_visibility_plan.py
python3 examples/simulate_dashboard_visibility.py
```

Decision handling:

- `show_incident_overview`: inspect incident summary.
- `show_trace_timeline`: inspect trace timeline.
- `show_route_registry_state`: inspect model route and tool exposure.
- `show_workflow_state`: inspect workflow checkpoint or next action.
- `show_autonomy_agent_state`: inspect autonomy mode and agent owner.
- `show_approval_queue`: review approval request.
- `show_budget_risk`: inspect budget reserve.
- `show_execution_boundary`: inspect execution-boundary reason.
- `show_stale_data_warning`: refresh or check stream health.
- `show_empty_state`: wait for incident.
- `block_unredacted_payload`: fix redaction before rendering.
- `block_inaccessible_widget`: fix accessibility before release.
- `show_connection_loss_banner`: check stream health.

Escalate to a product or operations owner if:

- the latest event maps to no panel
- stale data has no visible warning
- sensitive data is unredacted
- keyboard navigation or accessible labels fail
- the dashboard hides an approval or execution-boundary decision
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v26 Lab](lab.md)
- Next: [v26 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
