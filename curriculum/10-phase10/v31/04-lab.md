# v31 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P multimodal decisions without starting a model
runtime, camera, microphone, OCR engine, transcription engine, upload path,
media reader, provider call, or network call.

Files:

- `frontier/aois-p/multimodal-aois.plan.json`
- `examples/validate_multimodal_aois_plan.py`
- `examples/simulate_multimodal_aois.py`

Inspect:

```bash
sed -n '1,900p' frontier/aois-p/multimodal-aois.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_multimodal_aois_plan.py examples/simulate_multimodal_aois.py
python3 examples/validate_multimodal_aois_plan.py
python3 examples/simulate_multimodal_aois.py
```

Expected:

```json
{
  "passed_cases": 17,
  "score": 1.0,
  "status": "pass",
  "total_cases": 17
}
```

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- remove `document` from `modality_catalog`
- remove `file_upload_security_review` from live checks
- change `case_defaults.media_type` to `image/svg+xml`
- change `case_defaults.consent_status` to `missing`
- change `missing_accessibility_alternative_blocked.overrides.accessibility_alternative_status` to `present`
- change `provider_unavailable_text_fallback.overrides.provider_status` to `available`

## Explanation Lab

Explain why each case chooses its decision:

- image analysis allows
- audio analysis allows
- video analysis allows
- document analysis allows
- unknown modality blocks
- unsupported media type blocks
- failed file validation blocks
- exceeded size limit blocks
- missing consent blocks
- unredacted PII blocks
- missing accessibility alternative blocks
- missing transcript blocks
- cross-modal mismatch blocks
- missing evidence holds
- low confidence holds
- unavailable provider routes to text fallback
- policy boundary failure blocks

## Defense Lab

Defend why v31 models multimodal behavior locally before processing real media.
The system should prove intake, consent, privacy, accessibility, consistency,
evidence, fallback, and policy gates before any live media or model runtime can
affect users.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v31 - Multimodal AOIS](03-notes.md)
- Next: [v31 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
