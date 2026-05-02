# v18 Lab

Authoring status: authored

## Build Lab

Compile and run the local-only incident response validator and simulator:

```bash
python3 -m py_compile examples/validate_incident_response_plan.py examples/simulate_incident_response.py
python3 examples/validate_incident_response_plan.py
python3 examples/simulate_incident_response.py
```

Expected validator result:

- `incident_runtime_started: false`
- `pager_runtime_started: false`
- `ticketing_runtime_started: false`
- `chatops_runtime_started: false`
- `status_page_runtime_started: false`
- `agent_runtime_started: false`
- `provider_call_made: false`
- `status: pass`

Expected simulator result:

- A local `SEV2` incident is declared.
- The trigger is agent error budget exhaustion.
- Low-confidence or destructive agent actions are routed to human review.
- Prompt and tool changes are frozen.
- Post-incident review is required.

## Ops Lab

Answer from the plan:

1. Which severities exist?
2. Which role coordinates the incident?
3. Which role writes updates?
4. Which role records the timeline?
5. Which controls protect agent behavior during an incident?
6. Which policy prevents premature root cause claims?
7. Which fields prove no live response tooling started?

## Break Lab

Use a scratch copy or reversible local edit only.

Break 1: set `pager_runtime_started` to `true`.

Expected result: the validator fails because v18 is not approved to connect
live paging.

Break 2: remove `communications_lead`.

Expected result: the validator fails because incident communication has no
owner.

Break 3: disable `post_incident_review_required`.

Expected result: the validator fails because incident learning is mandatory.

## Explanation Lab

Explain the incident response flow:

1. Detect the symptom.
2. Triage impact and severity.
3. Declare the incident.
4. Assign roles.
5. Stabilize the system.
6. Mitigate active impact.
7. Resolve using explicit criteria.
8. Review the incident and create action items.

## Defense Lab

Defend these decisions:

1. No live pager or chatops runtime is started because routing and operational
   ownership are not being deployed in this lesson.
2. Agent incidents need explicit controls because HTTP success can hide unsafe
   output.
3. Severity exists to match response intensity to impact.
4. Root cause waits for evidence because premature conclusions lead to wrong
   mitigations.
5. Post-incident review is required because repeated failures are a process
   defect, not just a technical defect.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v18 - Incident Response Maturity Without Runtime](03-notes.md)
- Next: [v18 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
