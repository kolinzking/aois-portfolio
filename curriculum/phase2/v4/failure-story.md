# v4 Failure Story

Authoring status: authored

## Symptom

A Docker build unexpectedly consumes much more disk than expected.

## Root Cause

The build context included files that should not enter the image, such as `.venv`, `.git`, caches, or curriculum content.

## Fix

Use `.dockerignore` and validate it:

```bash
python3 examples/validate_container_plan.py
```

## Prevention

Inspect container plans before building.

Keep Docker build/run approval-gated on the shared server.

## What This Taught Me

Container builds are resource events.

They need the same discipline as database, Kubernetes, and provider runtime work.
