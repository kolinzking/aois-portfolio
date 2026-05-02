# v27 Failure Story

Authoring status: authored

## Symptom

A viewer opens the AOIS-P dashboard during a high-severity incident and sees
budget reserve, route-cost, and trace details for another tenant. Later, an
approval is recorded by the same person who requested the high-risk action.

## Root Cause

The product treated `isAuthenticated` as enough to render dashboard state. It
did not bind tenant context to identity, did not require explicit resource
permissions, did not block raw sensitive trace fields, and did not compare the
approver to the requester.

The dashboard also logged page views instead of access decisions, so the team
could not reconstruct which policy allowed the exposure.

## Fix

v27 fixes the failure with a policy-aware access contract:

- unknown roles are denied
- cross-tenant requests are denied
- missing role permissions are denied
- unredacted sensitive resources are denied
- self-approval is denied
- break-glass access is limited and audited
- allowed responses return explicit visible fields

## Prevention

Before live access implementation:

- select and review the identity provider
- review authentication assurance requirements
- review session security
- bind tenant context to authenticated identity
- review the permission matrix
- integrate a policy decision point
- review redaction policy
- review approval separation
- rehearse the break-glass runbook
- review access-audit retention
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v27 Runbook](runbook.md)
- Next: [v27 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
