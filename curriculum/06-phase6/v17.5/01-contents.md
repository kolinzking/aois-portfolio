# v17.5 Contents

Authoring status: authored

Topic: Service and agent SLOs for AI infrastructure

Safety mode: local plan and simulation only. This version does not start
Prometheus, Alertmanager, Grafana, an agent runtime, a provider call, cloud
resources, containers, or persistent services.

## Start Here

1. Read [02-introduction.md](02-introduction.md) to understand why SLOs come after
   telemetry, tracing, and event streaming.
2. Read [03-notes.md](03-notes.md) for the full SLI/SLO/error-budget model.
3. Inspect `reliability/aois-p/service-agent-slo.plan.json`.
4. Run:

```bash
python3 -m py_compile examples/validate_service_agent_slo_plan.py examples/simulate_slo_error_budget.py
python3 examples/validate_service_agent_slo_plan.py
python3 examples/simulate_slo_error_budget.py
```

Expected result: both scripts pass while all runtime flags remain false.

## Topic Jumps

- SLIs, SLOs, and error budgets: [03-notes.md](03-notes.md)
- Hands-on validation and break exercises: [04-lab.md](04-lab.md)
- Recovery procedure: [05-runbook.md](05-runbook.md)
- Measurement checklist: [07-benchmark.md](07-benchmark.md)
- Agent-quality failure mode: [06-failure-story.md](06-failure-story.md)
- Transition to incident response maturity: [10-next-version-bridge.md](10-next-version-bridge.md)

## Self-Paced Path

1. Explain the difference between SLI, SLO, SLA, and alert.
2. Identify the service SLOs and agent SLO in the plan.
3. Run the validator and prove no monitoring runtime started.
4. Run the simulator and identify which budget is exhausted.
5. Explain why agent quality and safety cannot be replaced by HTTP success.
6. Break the plan in a scratch edit, then use validator output to explain the
   risk.
7. Answer the mastery checkpoint in [03-notes.md](03-notes.md).
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17.5 Start Here](00-start-here.md)
- Next: [v17.5 Introduction](02-introduction.md)
<!-- AOIS-NAV-END -->
