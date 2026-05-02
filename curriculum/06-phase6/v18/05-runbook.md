# v18 Runbook

Authoring status: authored

## Purpose

This runbook restores the v18 incident response lesson to its safe local-only
state and explains how to correct validation failures.

## Primary Checks

Run:

```bash
python3 examples/validate_incident_response_plan.py
python3 examples/simulate_incident_response.py
```

The safe state is:

- `incident_runtime_started` is `false`.
- `pager_runtime_started` is `false`.
- `ticketing_runtime_started` is `false`.
- `chatops_runtime_started` is `false`.
- `status_page_runtime_started` is `false`.
- `agent_runtime_started` is `false`.
- `provider_call_made` is `false`.
- all runtime limits are `0`.
- all roles use `aois-p-` placeholders.
- agent incident controls require human approval and audit.

## Recovery Steps

1. Restore all runtime flags to `false`.
2. Restore `SEV1`, `SEV2`, and `SEV3`.
3. Restore required roles: incident commander, operations lead,
   communications lead, scribe, subject matter expert, and agent operator.
4. Restore lifecycle steps: detect, triage, declare, stabilize, mitigate,
   resolve, and review.
5. Restore runbook controls.
6. Restore agent incident controls.
7. Restore communication policy.
8. Restore post-incident review requirements.
9. Restore diagnosis policy.
10. Restore all runtime limits to `0`.
11. Rerun the validator and simulator.

If a real pager, ticketing, or chatops integration was started outside this
lesson, confirm it is not part of the primary AOIS workload before changing it.
This curriculum must not interfere with the primary project.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v18 Lab](04-lab.md)
- Next: [v18 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
