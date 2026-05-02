# v31 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide whether a non-text input can be
analyzed, blocked, held, or routed to fallback.

## Primary Checks

1. Confirm the decision is for `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm modality is in the modality catalog.
4. Confirm media type is allowlisted for the modality.
5. Confirm file validation passed.
6. Confirm media size is within limit.
7. Confirm source trust is recorded.
8. Confirm consent is present.
9. Confirm PII and sensitive media content are redacted.
10. Confirm required accessibility alternative is present.
11. Confirm transcript or extracted text is present when required.
12. Confirm cross-modal consistency passed.
13. Confirm multimodal evidence is present.
14. Confirm confidence is above threshold.
15. Confirm model route is approved.
16. Confirm text fallback is available.
17. Confirm policy boundaries pass.
18. Confirm no live multimodal, model, OCR, transcription, camera, microphone, media, network, or provider runtime flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_multimodal_aois_plan.py
python3 examples/simulate_multimodal_aois.py
```

Decision handling:

- `allow_image_analysis`: render image evidence summary.
- `allow_audio_analysis`: render audio transcript summary.
- `allow_video_analysis`: render video scene summary.
- `allow_document_analysis`: render document evidence summary.
- `block_unknown_modality`: reject unknown modality.
- `block_unsupported_media_type`: reject unsupported media type.
- `block_file_validation_failed`: quarantine media before analysis.
- `block_size_limit_exceeded`: request smaller or sampled media.
- `block_missing_consent`: obtain media intake consent.
- `block_pii_unredacted`: redact sensitive media content.
- `block_missing_accessibility_alternative`: add text alternative or description.
- `block_missing_transcript`: add transcript or extracted text.
- `block_cross_modal_mismatch`: investigate cross-modal conflict.
- `hold_missing_evidence`: collect multimodal evidence.
- `hold_low_confidence`: route to human review.
- `route_to_text_fallback`: use accessible text fallback.
- `block_policy_boundary`: repair multimodal policy boundary.

Escalate to a security, accessibility, or platform owner if:

- file validation fails
- consent or PII redaction is missing
- required accessibility alternative or transcript is missing
- cross-modal evidence conflicts
- fallback path is unavailable
- policy boundaries fail
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v31 Lab](lab.md)
- Next: [v31 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
