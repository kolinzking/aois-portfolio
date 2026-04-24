# v0.6 Failure Story

Authoring status: authored

## Symptom

`POST /analyze` returned a validation error.

## Root Cause

The request body did not include the required `message` field.

## Fix

Send a valid body:

```bash
curl -i -X POST http://127.0.0.1:8006/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx after deploy"}'
```

## Prevention

Keep request models explicit and test invalid input on purpose.

## What This Taught Me

API boundaries should reject malformed input before business logic runs.

Validation failure is a useful safety behavior, not just an error.
