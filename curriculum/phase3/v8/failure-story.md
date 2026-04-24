# v8 Failure Story

Authoring status: authored

## Symptom

A Git commit unexpectedly changes live cluster resources.

## Root Cause

Automated sync was enabled before review and approval discipline was ready.

## Fix

Disable automated sync for the portfolio plan:

```yaml
automated: null
```

## Prevention

Validate GitOps manifests before applying them.

Keep sync gated until resource and deployment impact is approved.

## What This Taught Me

GitOps is deployment power through Git.

That power needs review and approval boundaries.
