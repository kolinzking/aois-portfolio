# v33 Runbook

Authoring status: authored

## Purpose

Use this runbook when reviewing AOIS-P adversarial testing or red-team cases.
This runbook is for local planning and synthetic simulation only. It does not
authorize live testing, provider calls, tool execution, exploit execution, or
storage of harmful payloads.

## Primary Checks

Before recording a case, confirm:

- written authorization is approved
- rules of engagement are approved
- scope is AOIS-P only
- primary AOIS is excluded
- target is local and synthetic
- payload description is sanitized
- policy boundary passes
- tool permissions are least privilege
- data boundary passes
- telemetry is captured
- sanitized evidence is present
- severity is assigned
- mitigation status is known
- regression status is known

Block immediately when authorization, scope, target, payload safety, policy,
tool, or data-boundary checks fail.

Hold when telemetry, evidence, mitigation, or regression state is incomplete.

Escalate confirmed control failures by threat category.

## Recovery Steps

For every escalated finding:

- preserve sanitized observation evidence
- identify the expected control that failed
- assign mitigation owner
- add a regression case
- connect the finding to release controls
- connect the finding to access controls when tenant, privacy, or role state is involved
- rerun the simulator after the case is updated

Do not close a finding only because the test string was removed. Close it when
the control is repaired and a regression case proves the repair.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v33 Lab](04-lab.md)
- Next: [v33 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
