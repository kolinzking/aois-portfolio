# v17.5 Summary Notes

Authoring status: authored

## What Was Built

A local-only SLO lesson for AOIS:

- `reliability/aois-p/service-agent-slo.plan.json`
- `examples/validate_service_agent_slo_plan.py`
- `examples/simulate_slo_error_budget.py`
- authored v17.5 notes, lab, runbook, benchmark, failure story, and bridge

No metrics backend, alerting service, dashboard service, agent runtime,
provider call, cloud call, install, or persistent runtime was started.

## What Was Learned

You learned how AOIS moves from observability to reliability policy.

Key ideas:

- SLIs are measurements.
- SLOs are targets.
- Error budgets define allowed failure.
- Burn rate determines urgency.
- Agent reliability includes quality and safety, not just uptime.
- Exhausted budgets must change operational behavior.

## Core Limitation Or Tradeoff

v17.5 does not prove live Prometheus, Alertmanager, or Grafana behavior. That is
intentional. The tradeoff is lower runtime realism in exchange for zero
persistent resource impact on the shared server.

Live SLO monitoring should only be deployed after retention, storage, alert
routing, dashboards, and primary-project separation are explicit.
