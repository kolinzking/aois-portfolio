# v13 Failure Story

Authoring status: authored

## Symptom

The server runs out of disk after someone downloads a model before checking model size and storage headroom.

## Root Cause

The team treated model download as a harmless setup step.

They skipped license review, model size review, storage budget, and rollback planning.

## Fix

Remove the unapproved model artifact after approval.

Restore disk headroom.

Update the inference plan so model download remains gated.

## Prevention

Do not download models until AOIS has model license review, model size review, memory budget, storage budget, cost budget, fallback route, and rollback approval.

Lesson learned: inference operations begin before the first inference request.
