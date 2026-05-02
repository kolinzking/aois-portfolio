# v27 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide whether a subject may view or act
on a dashboard resource.

## Primary Checks

1. Confirm the case is in `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm subject ID is present.
4. Confirm tenant ID is present.
5. Confirm role is in the role catalog.
6. Confirm resource type is in the resource catalog.
7. Confirm resource tenant matches the subject tenant.
8. Confirm the role has the requested resource action.
9. Confirm sensitive resources are redacted before render.
10. Confirm approval actions are not self-approval.
11. Confirm break-glass is limited to the approved emergency case.
12. Confirm allowed responses list visible fields explicitly.
13. Confirm allowed and denied decisions emit audit events.
14. Confirm no auth, identity provider, token, session, API, frontend, policy, database, provider, or network runtime flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_policy_aware_access_plan.py
python3 examples/simulate_policy_aware_access.py
```

Decision handling:

- `allow_incident_overview`: render incident overview fields.
- `allow_trace_view`: render redacted trace timeline fields.
- `allow_approval_review`: render approval review for an independent approver.
- `allow_budget_view`: render budget and cost fields.
- `allow_execution_boundary_view`: render execution-boundary fields.
- `allow_access_audit_view`: render access audit fields.
- `deny_unknown_role`: reject and review role assignment.
- `deny_cross_tenant`: reject and inspect tenant context binding.
- `deny_missing_permission`: reject and review role permissions.
- `deny_unredacted_sensitive`: fix redaction before render.
- `deny_self_approval`: route to an independent approver.
- `allow_break_glass_limited_view`: record break-glass review.

Escalate to a product or security owner if:

- cross-tenant access is allowed outside the break-glass case
- an unknown role is accepted
- a role uses wildcard permissions
- sensitive state renders without redaction
- approval separation fails
- break-glass lacks a limited field list or audit event
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v27 Lab](lab.md)
- Next: [v27 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
