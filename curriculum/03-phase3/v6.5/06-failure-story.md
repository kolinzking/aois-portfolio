# v6.5 Failure Story

Authoring status: authored

## Symptom

A compromised pod can call the Kubernetes API.

## Root Cause

The pod received an unnecessary service account token and broad RBAC permissions.

## Fix

Use:

- minimal ServiceAccount
- `automountServiceAccountToken: false`
- empty Role until permissions are required
- NetworkPolicy

## Prevention

Validate identity manifests before applying them.

Do not grant permissions before a workload proves it needs them.

## What This Taught Me

Identity and permissions are part of the workload, not an afterthought.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v6.5 Runbook](05-runbook.md)
- Next: [v6.5 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
