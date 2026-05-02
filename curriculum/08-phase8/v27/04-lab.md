# v27 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P policy-aware access without starting an auth
server, identity provider, token issuer, session, API server, frontend runtime,
browser, policy engine, database, tool call, provider call, or network call.

Files:

- `product/aois-p/policy-aware-access.plan.json`
- `examples/validate_policy_aware_access_plan.py`
- `examples/simulate_policy_aware_access.py`

Inspect:

```bash
sed -n '1,900p' product/aois-p/policy-aware-access.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_policy_aware_access_plan.py examples/simulate_policy_aware_access.py
python3 examples/validate_policy_aware_access_plan.py
python3 examples/simulate_policy_aware_access.py
```

Expected:

```json
{
  "passed_cases": 12,
  "score": 1.0,
  "status": "pass",
  "total_cases": 12
}
```

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- remove `security` from `role_catalog`
- add `*` to any role permission list
- remove `tenant_context_binding_review` from live access checks
- change `cross_tenant_denied.resource_tenant_id` to `tenant-alpha`
- change `operator_unredacted_trace_denied.redaction_status` to `redacted`
- change `self_approval_denied.approval_relationship` to `independent_approver`
- change `security_break_glass_limited_cross_tenant.policy_context` to `normal`

## Explanation Lab

Explain why each case chooses its decision:

- viewer incident same tenant is allowed
- operator redacted trace same tenant is allowed
- independent approver review is allowed
- finops budget same tenant is allowed
- security execution-boundary same tenant is allowed
- auditor access audit same tenant is allowed
- unknown role is denied
- cross-tenant request is denied
- viewer budget request is denied
- raw trace request is denied
- self-approval is denied
- break-glass access is limited and audited

## Defense Lab

Defend why v27 models access locally before implementing SSO or sessions. The
system should first prove policy shape, deny order, tenant boundaries,
redaction gates, approval separation, and audit events before wiring those
decisions to live identity infrastructure.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v27 - Auth, Tenancy, And Policy-Aware Access](03-notes.md)
- Next: [v27 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
