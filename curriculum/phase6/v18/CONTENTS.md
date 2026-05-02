# v18 Contents

Authoring status: authored

Topic: Incident response maturity for AI infrastructure

Safety mode: local plan and simulation only. This version does not start pager,
ticketing, chatops, status page, agent runtime, provider calls, cloud resources,
containers, or persistent services.

## Start Here

1. Read [introduction.md](introduction.md) to understand why incident response
   follows SLOs.
2. Read [notes.md](notes.md) for the full severity, role, lifecycle,
   communication, mitigation, and review model.
3. Inspect `incident-response/aois-p/incident-response.plan.json`.
4. Run:

```bash
python3 -m py_compile examples/validate_incident_response_plan.py examples/simulate_incident_response.py
python3 examples/validate_incident_response_plan.py
python3 examples/simulate_incident_response.py
```

Expected result: both scripts pass while all runtime flags remain false.

## Topic Jumps

- Severity and roles: [notes.md](notes.md)
- Hands-on validation and break exercises: [lab.md](lab.md)
- Recovery procedure: [runbook.md](runbook.md)
- Measurement checklist: [benchmark.md](benchmark.md)
- Agent-quality incident story: [failure-story.md](failure-story.md)
- Transition to release safety: [next-version-bridge.md](next-version-bridge.md)

## Self-Paced Path

1. Explain why incident response comes after SLOs.
2. Identify the severities, roles, and lifecycle in the plan.
3. Run the validator and prove no pager or chatops runtime started.
4. Run the simulator and trace the SEV2 incident timeline.
5. Explain why unsafe agent behavior needs incident response even if the API is
   available.
6. Break the plan in a scratch edit and use validator output to explain the
   risk.
7. Answer the mastery checkpoint in [notes.md](notes.md).
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17.5 Next Version Bridge](../v17.5/next-version-bridge.md)
- Next: [v18 Introduction](introduction.md)
<!-- AOIS-NAV-END -->
