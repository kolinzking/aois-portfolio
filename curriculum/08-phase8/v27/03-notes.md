# v27 - Auth, Tenancy, And Policy-Aware Access

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no auth server,
no identity provider, no token issuance, no session creation, no API server, no
frontend runtime, no browser, no policy-engine runtime, no database, no tool
execution, no command execution, no file write during validation, no network
call, no provider call, no external network during validation, no persistent
storage

## What This Builds

This version builds an identity-aware access contract and simulation:

- `product/aois-p/policy-aware-access.plan.json`
- `examples/validate_policy_aware_access_plan.py`
- `examples/simulate_policy_aware_access.py`

It teaches:

- authentication boundaries
- authorization decisions
- tenant-scoped resource access
- role catalogs and permission matrices
- deny-by-default policy order
- redaction-aware dashboard rendering
- self-approval denial
- break-glass access limits
- access audit events

## Why This Exists

v26 made AOIS-P visible to operators. Visibility is useful only when the right
person sees the right state for the right tenant.

An operator dashboard can leak sensitive state in several ways:

- showing another tenant's incident
- rendering raw trace data before redaction
- letting a viewer inspect budget data
- letting a requester approve their own high-risk action
- letting a broad admin role bypass policy review
- omitting audit records for allowed and denied access

The central access question is:

```text
Given a subject, tenant, role, resource, action, ownership relationship,
approval relationship, break-glass context, and redaction state, should AOIS-P
show the requested dashboard state, deny it, or allow only a limited emergency
view?
```

v27 answers that question locally. It does not implement login, SSO, JWTs,
cookies, sessions, database row policies, or a live policy engine.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution -> show operators the state -> scope access by identity, tenant, role, resource, action, redaction, and audit`

v27 consumes the v26 dashboard panels:

- incident overview
- trace timeline
- route and registry
- workflow and orchestration
- autonomy and agents
- approvals
- budget
- execution boundaries
- access audit

The output is an access decision: allowed fields, denied state, operator action,
and audit event.

## Learning Goals

By the end of this version you should be able to:

- separate authentication from authorization
- explain why tenant context must be bound to authenticated identity
- design a role catalog without wildcard permissions
- map dashboard resources to explicit actions
- enforce same-tenant access before rendering operational state
- block sensitive resources until redaction passes
- deny unknown roles, missing permissions, cross-tenant requests, and self-approval
- define limited break-glass access with audit requirements
- validate and simulate policy-aware access locally

## Prerequisites

You should have completed:

- Phase 6 observability and incident-response lessons
- `v20` through `v25` in Phase 7
- `v26` dashboard and real-time visibility

Required checks:

```bash
python3 -m py_compile examples/validate_policy_aware_access_plan.py examples/simulate_policy_aware_access.py
python3 examples/validate_policy_aware_access_plan.py
python3 examples/simulate_policy_aware_access.py
```

## Core Concepts

## Authentication

Authentication answers: who is the subject?

v27 records the need for identity but does not create a login flow. No identity
provider is called, no token is issued, and no session is created. The lesson
keeps the subject ID as local data so the policy behavior can be inspected
without pretending that an auth system exists.

## Authorization

Authorization answers: may this subject perform this action on this resource?

v27 uses explicit role permissions such as `trace:view` and `approvals:approve`.
There is no wildcard permission and no implicit admin override.

## Tenancy

Tenancy answers: which customer, team, or bounded operating context owns this
resource?

The access plan requires both `tenant_id` and `resource_tenant_id`. A normal
request is denied when they differ.

## Resource Catalog

Each dashboard resource has:

- resource type
- panel ID
- tenant scope
- sensitivity
- allowed actions
- default visible fields

This prevents dashboard panels from becoming free-form data leaks.

## Permission Matrix

Roles grant resource actions. They do not grant arbitrary UI visibility.

Examples:

- `viewer` can view incident summaries only
- `operator` can inspect operational state but not budget or approval actions
- `approver` can approve eligible requests but cannot self-approve
- `finops` can inspect budget state
- `security` can inspect redacted traces, execution boundaries, and access audit
- `tenant_admin` can inspect access posture and manage tenant users
- `auditor` can read audit state without operational action rights

## Policy Order

The simulator evaluates:

1. unknown role
2. unredacted sensitive resource
3. self-approval
4. valid break-glass limited view
5. cross-tenant access
6. missing permission
7. explicit allow
8. deny by default

Order matters. A system that checks UI permissions before redaction can leak
sensitive trace data. A system that checks role before tenant can confuse
horizontal access with a normal missing permission.

## Redaction Gate

Sensitive dashboard resources must not render while raw. v27 blocks unredacted
trace state before it considers normal allow decisions.

## Approval Separation

Approval is not just a button permission. The policy must also know whether the
subject is the requester. A requester with the `approver` role still cannot
approve their own high-risk action.

## Break-Glass Access

Break-glass is a narrow emergency path, not a hidden superuser role. v27 allows
only a security subject, only for an active safety incident, only for redacted
incident state, and only with limited visible fields plus a break-glass audit
event.

## Build

Inspect:

```bash
sed -n '1,900p' product/aois-p/policy-aware-access.plan.json
sed -n '1,420p' examples/validate_policy_aware_access_plan.py
sed -n '1,320p' examples/simulate_policy_aware_access.py
```

Compile:

```bash
python3 -m py_compile examples/validate_policy_aware_access_plan.py examples/simulate_policy_aware_access.py
```

Validate:

```bash
python3 examples/validate_policy_aware_access_plan.py
```

Simulate:

```bash
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

## Ops Lab

1. Open the policy-aware access plan.
2. Find `role_catalog`.
3. Confirm every role has explicit permissions and no wildcard permission.
4. Find `resource_catalog`.
5. Confirm every resource is tenant scoped.
6. Find `policy_order`.
7. Confirm deny checks happen before normal allow decisions.
8. Find `access_cases`.
9. Confirm each decision gate has a case.
10. Run the validator.
11. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Change `viewer.permissions` to include `budget:view`.
2. Confirm the simulator no longer denies the viewer budget case.
3. Restore the permission list.
4. Change `operator_unredacted_trace_denied.redaction_status` to `redacted`.
5. Confirm the simulator no longer blocks the raw trace case.
6. Restore the value.
7. Change `cross_tenant_denied.resource_tenant_id` to `tenant-alpha`.
8. Confirm the simulator no longer denies cross-tenant access.
9. Restore the value.
10. Change `self_approval_denied.approval_relationship` to `independent_approver`.
11. Confirm the simulator no longer blocks self-approval.
12. Restore the value.
13. Remove `tenant_context_binding_review` from live access checks.
14. Confirm validation fails.
15. Restore the check.

## Testing

The validator checks:

- no live auth, identity provider, session, API, frontend, policy, database, network, provider, command, or tool runtime is enabled
- source notes are current for April 30, 2026
- access scope controls are explicit
- required controls are true
- access dimensions are present
- role catalog is complete
- role permissions are explicit and non-wildcard
- resource catalog is complete
- resources are tenant scoped
- policy order matches the deny-first sequence
- decision gates are defined
- every access decision has at least one case
- required live-access reviews are listed

The simulator checks:

- viewer incident access is allowed
- operator trace access is allowed after redaction
- independent approval review is allowed
- finops budget access is allowed
- security execution-boundary access is allowed
- auditor access-audit access is allowed
- unknown role is denied
- cross-tenant request is denied
- viewer budget access is denied
- raw trace rendering is denied
- self-approval is denied
- break-glass access is limited and audited

## Common Mistakes

- treating authentication as permission
- trusting a tenant ID supplied by the client without binding it to identity
- using broad admin or wildcard permissions
- checking UI visibility but not resource ownership
- hiding denied cases instead of auditing them
- letting budget, trace, or execution-boundary panels inherit generic viewer access
- allowing self-approval because the user has the approver role
- treating break-glass as permanent cross-tenant access

## Troubleshooting

If validation fails:

- read the `missing` list
- restore the required false runtime flags
- restore source notes and dates
- restore role, resource, policy order, and live access checks

If simulation fails:

- compare `decision` to `expected_decision`
- compare `visible_fields` to `expected_visible_fields`
- inspect role permissions for the case
- inspect tenant and resource tenant IDs
- inspect redaction status
- inspect approval relationship
- inspect break-glass context

## Benchmark

Run:

```bash
python3 -m py_compile examples/validate_policy_aware_access_plan.py examples/simulate_policy_aware_access.py
python3 examples/validate_policy_aware_access_plan.py
python3 examples/simulate_policy_aware_access.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- auth, identity provider, token, session, API, frontend, policy, network, and provider flags

## Architecture Defense

Defend this design:

- access is modeled before live SSO or session implementation
- authentication and authorization are separate
- tenant context is first-class
- resource actions are explicit
- redaction blocks sensitive rendering
- self-approval is blocked even for approvers
- break-glass is limited, redacted, and audited
- AOIS-P remains separated from primary AOIS

## 4-Layer Tool Drill

Explain the v27 work at four layers:

- data: subject, tenant, role, resource, action, redaction, audit
- policy: deny-first ordered access decisions
- product: dashboard panels render only allowed fields
- operations: access decisions create reviewable audit events

## 4-Level System Explanation Drill

Explain v27 at four levels:

- beginner: users only see the AOIS-P dashboard parts they are allowed to see
- practitioner: roles grant explicit resource actions inside a tenant boundary
- engineer: the simulator evaluates deny-first policy gates before allowed fields are returned
- architect: AOIS-P separates identity, tenancy, authorization, redaction, approval separation, and audit into a local contract that can be implemented later with real auth infrastructure

## Failure Story

A viewer opens a dashboard during an incident and sees the budget panel because
the UI used a generic `isAuthenticated` check. The viewer screenshots budget
reserve and route-cost details from another team. No one can tell whether the
view was intended because the dashboard logged page loads but not access
decisions.

v27 prevents this failure by requiring explicit `budget:view` permission,
tenant ownership, redaction, and audit events before rendering budget fields.

## Mastery Checkpoint

You are ready to move on when you can:

- explain the difference between authentication and authorization
- trace an access case through the policy order
- add a new dashboard resource without wildcard permissions
- explain why self-approval requires relationship checks
- explain why break-glass must be limited and audited
- pass validation and simulation without live auth infrastructure

## Connection Forward

Phase 8 is now complete. AOIS-P has a product visibility contract and an
identity-aware access contract.

v28 begins Phase 9 by turning AOIS changes into safe releases: CI/CD,
signatures, release gates, rollout controls, model rollout control, and
feature-flagged AI releases.

## Source Notes

Checked 2026-05-02.

- OWASP Application Security Verification Standard project page: used for the security-control framing around authentication, authorization, access control, and verification.
- OpenAI safety best-practices guidance: used for policy-review and safety-gate framing around AI product surfaces.
- v27 is a local policy-aware access contract. It does not enable live auth, sessions, tokens, database policies, network calls, or provider calls.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v27 Introduction](02-introduction.md)
- Next: [v27 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
