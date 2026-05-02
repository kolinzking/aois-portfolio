# v33 Failure Story

Authoring status: authored

## Symptom

An operator asks AOIS-P to summarize a diagnostic document. The document carries
a hidden instruction that conflicts with the system policy. AOIS-P retrieves
the document, treats the hidden instruction as normal context, activates a tool
path, and routes the result through central fallback because the edge cache is
stale.

The incident record shows a normal answer, but the trace does not prove which
instruction won.

## Root Cause

The system had not red-teamed indirect prompt injection, cache poisoning,
fallback abuse, or tool permission boundaries together. Each control looked
reasonable alone, but the combined path created a policy confusion failure.

## Fix

v33 fixes the failure by requiring:

- written authorization and rules of engagement
- sanitized indirect-injection scenarios
- local synthetic targets
- least-privilege tool tests
- cache and fallback abuse tests
- telemetry and sanitized evidence
- severity assignment
- mitigation ownership
- regression before closure

## Prevention

Do not call a frontier control ready until it has an adversarial case that can
prove the expected control behavior, record safe evidence, assign mitigation
when it fails, and keep a regression case so the failure does not return.
