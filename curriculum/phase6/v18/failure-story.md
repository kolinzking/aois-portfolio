# v18 Failure Story

Authoring status: authored

## Symptom

The incident agent begins producing vague recommendations during a memory
pressure event. The API is still available, so the team hesitates to declare an
incident.

## Root Cause

AOIS had SLO data but no incident response policy for agent quality failures.
There was no incident commander, no agent operator, no prompt freeze, no
timeline, and no communication cadence.

## Fix

Declare a `SEV2` incident, assign roles, route risky agent actions to human
review, freeze prompt and tool changes, preserve traces and outputs, communicate
impact, resolve using explicit criteria, and create post-incident action items.

## Prevention

Prevent recurrence by requiring:

- severity policy
- single incident commander
- agent operator role
- timeline
- communication cadence
- human approval for destructive action
- post-incident review
- action item owners and due dates

Availability alone does not prove an AI infrastructure system is safe to trust.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v18 Runbook](runbook.md)
- Next: [v18 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
