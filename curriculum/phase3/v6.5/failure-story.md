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
