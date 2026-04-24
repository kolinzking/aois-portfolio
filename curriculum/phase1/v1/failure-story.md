# v1 Failure Story

Authoring status: authored

## Symptom

A request tried to enable provider execution with `allow_provider_call=true`.

## Root Cause

No provider, budget, API key storage, rate limit, or data policy had been approved.

The caller treated external inference like a normal boolean option.

## Fix

Return `403`:

```json
{
  "detail": "External AI provider calls are disabled..."
}
```

Keep the dry-run structured contract path active.

## Prevention

Make provider execution visible and gated:

- request field: `allow_provider_call`
- response field: `provider_call_made`
- mode field: `provider_mode`
- tests that prove forced provider use is rejected

## What This Taught Me

External inference is an operational boundary.

It involves secrets, money, latency, data exposure, and reliability.
