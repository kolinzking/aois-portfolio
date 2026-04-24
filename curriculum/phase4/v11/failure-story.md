# v11 Failure Story

Authoring status: authored

## Symptom

AOIS receives one incident event, but the result sink contains multiple conflicting analysis records for the same incident.

## Root Cause

The workflow retried failed messages but did not require an `idempotency_key`.

The worker treated each retry as new work. The system had a queue, but it did not have duplicate protection.

## Fix

Add idempotency to the message contract.

Deduplicate by `idempotency_key` or `event_id` before writing final results.

Send messages to a DLQ after retry exhaustion so operators can inspect and replay deliberately.

## Prevention

Validate the event workflow plan before creating infrastructure.

Do not approve live cloud execution until AOIS has:

- event schema review
- idempotency test
- DLQ replay runbook
- observability
- IAM least privilege
- rollback plan

Lesson learned: retries improve reliability only when duplicate side effects are controlled.
