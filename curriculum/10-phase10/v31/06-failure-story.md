# v31 Failure Story

Authoring status: authored

## Symptom

An incident response includes a screenshot and a short video. AOIS-P reports a
root cause from the screenshot, but the video transcript contradicts the visual
claim. The screenshot also contains an unredacted token, and no text
alternative exists for the image.

## Root Cause

The team treated multimodal input as just another prompt. There was no media
type allowlist, file validation, consent check, redaction gate, accessibility
alternative, transcript requirement, cross-modal consistency check, or
confidence hold.

## Fix

v31 fixes the failure with a multimodal AOIS contract:

- modality catalog
- media type allowlist
- file validation
- size limits
- consent and source trust
- PII redaction
- accessibility alternatives
- transcripts or extracted text
- cross-modal consistency
- evidence and confidence checks
- text fallback
- policy boundaries

## Prevention

Before live multimodal use:

- review media intake
- review file upload security
- review modality catalog
- review consent and privacy
- review PII redaction
- review accessibility alternatives
- review transcripts
- review cross-modal consistency
- review confidence thresholds
- review model routes and fallback paths
- review platform and release integration
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v31 Runbook](05-runbook.md)
- Next: [v31 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
