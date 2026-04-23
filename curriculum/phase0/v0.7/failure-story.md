# v0.7 Failure Story

## Symptom

The model returned a useful explanation, but the result could not be cleanly slotted into `summary`, `severity`, and `suggestion` fields without extra work.

## Root Cause

Raw model output is optimized for language quality, not application schema.

## Fix

Treat raw inference and structured application output as separate problems.

## Prevention

Do not confuse "smart text" with "production-ready contract."
