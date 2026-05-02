# v31 Introduction

Authoring status: authored

## What This Version Is About

v31 starts Phase 10 by extending AOIS-P from text-only signals to multimodal
signals: image, audio, video, and documents.

It models the controls required before AOIS-P can reason over non-text inputs.

## Why It Matters In AOIS

Incidents often include screenshots, charts, call recordings, videos, scanned
documents, or other media. Those signals can improve diagnosis, but they add
file safety, consent, privacy, accessibility, transcript, consistency, and
confidence risks.

v31 makes multimodal reasoning a governed path instead of a loose model feature.

## How To Use This Version

Start with `notes.md`, then inspect:

- `frontier/aois-p/multimodal-aois.plan.json`
- `examples/validate_multimodal_aois_plan.py`
- `examples/simulate_multimodal_aois.py`

Run:

```bash
python3 -m py_compile examples/validate_multimodal_aois_plan.py examples/simulate_multimodal_aois.py
python3 examples/validate_multimodal_aois_plan.py
python3 examples/simulate_multimodal_aois.py
```

Expected simulator result:

```json
{
  "passed_cases": 17,
  "score": 1.0,
  "status": "pass",
  "total_cases": 17
}
```
