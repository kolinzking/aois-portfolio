# v31 - Multimodal AOIS

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no multimodal
runtime, no model runtime, no vision model call, no audio model call, no video
model call, no OCR engine, no transcription engine, no camera, no microphone,
no media file read, no upload, no download, no media processing, no network
call, no provider call, no persistent storage

## What This Builds

This version builds a local multimodal AOIS contract:

- `frontier/aois-p/multimodal-aois.plan.json`
- `examples/validate_multimodal_aois_plan.py`
- `examples/simulate_multimodal_aois.py`

It teaches:

- modality catalogs
- media type allowlists
- file validation gates
- consent and privacy controls
- PII redaction for media
- accessibility alternatives
- transcript requirements
- cross-modal consistency
- multimodal evidence and confidence
- model route and fallback controls
- policy and platform integration for non-text signals

## Why This Exists

Phase 10 starts the frontier layer. Frontier work should expand AOIS without
discarding rigor.

Text-only AOIS cannot inspect screenshots, charts, logs embedded in images,
recorded incident calls, short diagnostic videos, or scanned documents. But
multimodal inputs add new failure paths:

- unsafe files
- unsupported media types
- missing consent
- faces, voices, screenshots, or documents containing sensitive data
- missing captions, transcripts, or descriptions
- audio and video disagreeing with attached text
- low-confidence visual claims
- provider outages without accessible fallback

The central multimodal question is:

```text
Given modality, media type, validation, size, consent, PII state,
accessibility alternatives, transcript state, cross-modal consistency,
evidence, confidence, route, provider availability, fallback, and policy
status, should AOIS-P analyze, block, hold, or fall back?
```

v31 answers that question locally. It does not read or process real media.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution -> show operators the state -> scope access -> release changes safely -> track model delivery evidence -> package reusable platform controls -> reason over non-text signals`

v31 consumes Phase 9:

- platform controls guard multimodal capability exposure
- release controls govern multimodal feature rollout
- model delivery tracking governs multimodal behavior changes
- access controls protect sensitive media-derived state

The output is a multimodal decision: allow, block, hold, or text fallback.

## Learning Goals

By the end of this version you should be able to:

- define a modality catalog for AOIS-P
- explain why media type allowlists and file validation precede model calls
- identify privacy and consent gates for media inputs
- require accessibility alternatives for non-text signals
- require transcripts or extracted text for time-based media and documents
- detect cross-modal mismatches
- hold low-confidence or evidence-free multimodal claims
- route to text fallback when multimodal providers are unavailable
- keep multimodal paths integrated with platform, release, and access controls

## Prerequisites

You should have completed:

- Phase 8 product visibility and policy-aware access
- Phase 9 delivery, model-delivery, and platform patterns

Required checks:

```bash
python3 -m py_compile examples/validate_multimodal_aois_plan.py examples/simulate_multimodal_aois.py
python3 examples/validate_multimodal_aois_plan.py
python3 examples/simulate_multimodal_aois.py
```

## Core Concepts

## Modality Catalog

The modality catalog defines what AOIS-P can accept:

- image
- audio
- video
- document

Each modality has media type allowlists, size limits, accessibility needs,
transcript needs, and primary risks.

## Media Intake

Media intake is not just upload. It includes source trust, media type
allowlist, file signature validation, filename safety, size limits, and
quarantine behavior.

v31 models these checks without reading a real file.

## Consent And Privacy

Media can include faces, voices, documents, screenshots, locations, and
credentials. v31 blocks missing consent and unredacted sensitive media before
analysis.

## Accessibility Alternatives

Non-text signals need usable alternatives:

- image descriptions
- video descriptions
- captions
- transcripts
- extracted text

The goal is not only legal accessibility. It also creates reviewable evidence
that operators can inspect without depending on the original media.

## Transcript Requirements

Audio, video, and scanned documents need transcript or extracted text records.
Without them, the system cannot make claims that are accessible, searchable,
and auditable.

## Cross-Modal Consistency

Multimodal analysis must compare signals. A screenshot, caption, transcript,
and operator note may disagree. v31 blocks unexplained mismatches rather than
choosing the most convenient signal.

## Evidence And Confidence

Multimodal answers need cited evidence and confidence. v31 holds missing
evidence and low confidence for human review.

## Text Fallback

If the multimodal provider is unavailable, AOIS-P should fall back to an
accessible text path when one exists. Fallback is not success; it is a controlled
degradation.

## Build

Inspect:

```bash
sed -n '1,900p' frontier/aois-p/multimodal-aois.plan.json
sed -n '1,420p' examples/validate_multimodal_aois_plan.py
sed -n '1,280p' examples/simulate_multimodal_aois.py
```

Compile:

```bash
python3 -m py_compile examples/validate_multimodal_aois_plan.py examples/simulate_multimodal_aois.py
```

Validate:

```bash
python3 examples/validate_multimodal_aois_plan.py
```

Simulate:

```bash
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

## Ops Lab

1. Open the multimodal AOIS plan.
2. Find `modality_catalog`.
3. Confirm every modality has allowed media types, max bytes, accessibility requirements, transcript requirements, and primary risks.
4. Find `case_defaults`.
5. Confirm the default path is validated, consented, redacted, accessible, evidenced, confident, routed, and policy-approved.
6. Find `multimodal_cases`.
7. Confirm every decision gate has a case.
8. Run the validator.
9. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Remove `video` from `modality_catalog`.
2. Confirm validation fails.
3. Restore the modality.
4. Change `case_defaults.consent_status` to `missing`.
5. Confirm the first case no longer allows analysis.
6. Restore the value.
7. Change `missing_transcript_blocked.overrides.transcript_status` to `present`.
8. Confirm that case no longer blocks.
9. Restore the value.
10. Change `low_confidence_held.overrides.confidence` to `0.9`.
11. Confirm that case no longer holds.
12. Restore the value.

## Testing

The validator checks:

- no live multimodal, model, OCR, transcription, camera, microphone, media, network, provider, command, or tool runtime is enabled
- source notes are current for May 1, 2026
- multimodal scope controls are explicit
- required controls are true
- multimodal dimensions are present
- modality catalog is complete
- decision gates are complete
- defaults describe a safe image analysis path
- every decision has a case
- live multimodal review checks are listed

The simulator checks:

- image analysis is allowed
- audio analysis is allowed
- video analysis is allowed
- document analysis is allowed
- unknown modality is blocked
- unsupported media type is blocked
- failed file validation is blocked
- exceeded size is blocked
- missing consent is blocked
- unredacted PII is blocked
- missing accessibility alternative is blocked
- missing transcript is blocked
- cross-modal mismatch is blocked
- missing evidence is held
- low confidence is held
- provider unavailable routes to text fallback
- policy boundary failure is blocked

## Common Mistakes

- letting model capability drive media policy
- allowing any uploaded media type
- trusting content type without file validation
- skipping consent because the media is operational
- treating transcripts as optional
- making visual output inaccessible to non-visual users
- ignoring contradictions between image, audio, video, and text
- presenting low-confidence visual claims as fact
- failing to provide text fallback

## Troubleshooting

If validation fails:

- read the `missing` list
- restore false runtime flags
- restore source notes and dates
- restore scope and required controls
- restore modality catalog and live checks

If simulation fails:

- compare `decision` to `expected_decision`
- inspect the case override
- inspect media type against modality allowlist
- inspect consent, PII, accessibility, transcript, evidence, confidence, provider, and policy status

## Benchmark

Run:

```bash
python3 -m py_compile examples/validate_multimodal_aois_plan.py examples/simulate_multimodal_aois.py
python3 examples/validate_multimodal_aois_plan.py
python3 examples/simulate_multimodal_aois.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- multimodal, model, media, camera, microphone, OCR, transcription, network, and provider flags

## Architecture Defense

Defend this design:

- multimodal expansion is modeled before live media processing
- media intake is gated before model routing
- consent and privacy gates precede analysis
- accessibility alternatives are release controls
- transcripts and extracted text make media evidence auditable
- cross-modal mismatches block action
- low confidence holds for review
- text fallback is required
- Phase 9 platform and release controls still apply

## 4-Layer Tool Drill

Explain v31 at four layers:

- intake: modality, media type, file validation, size, source trust
- safety: consent, PII, accessibility, transcripts, policy
- reasoning: cross-modal consistency, evidence, confidence, route
- operations: observability, fallback, release, platform integration

## 4-Level System Explanation Drill

Explain v31 at four levels:

- beginner: AOIS-P can reason over images, audio, video, and documents only when safety checks pass
- practitioner: each non-text input needs media validation, consent, redaction, accessibility, evidence, and policy approval
- engineer: the simulator evaluates one multimodal failure mode at a time and returns allow, block, hold, or fallback
- architect: AOIS-P extends frontier input types while preserving access, release, platform, observability, and governance contracts

## Failure Story

An operator uploads a screenshot and a short incident video. The model claims a
root cause from the image, but the video transcript contradicts it. The
screenshot also contains an unredacted token, and no text alternative exists
for the visual evidence. The incident response records the claim as fact.

v31 prevents this by requiring file validation, consent, redaction,
accessibility alternatives, transcript or extracted text, cross-modal
consistency, evidence, confidence, fallback, and policy gates before analysis.

## Mastery Checkpoint

You are ready to move on when you can:

- explain why multimodal input changes the AOIS architecture
- define a modality catalog
- explain why accessibility alternatives and transcripts are operational evidence
- trace a multimodal case through allow, block, hold, or fallback
- explain how Phase 9 platform controls still apply
- pass validation and simulation without live media processing

## Connection Forward

v32 builds on v31 by moving inference toward edge and offline contexts. Once
AOIS-P can model non-text signals, the next frontier question is what happens
when compute, memory, connectivity, latency, data locality, and update channels
are constrained.

## Source Notes

Checked 2026-05-02.

- OpenAI images and vision documentation: used for current image-input and multimodal API vocabulary.
- OpenAI file-inputs documentation: used for document and file-input handling concepts.
- OpenAI safety best-practices guidance: used for safety-review, adversarial testing, and policy-boundary framing.
- v31 is a local multimodal contract. It does not process media, call OCR/transcription, upload files, run a model, or call providers.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v31 Introduction](introduction.md)
- Next: [v31 Lab](lab.md)
<!-- AOIS-NAV-END -->
