# v30 Introduction

Authoring status: authored

## What This Version Is About

v30 completes Phase 9 by packaging repeated AOIS-P controls into internal
platform patterns.

It models a capability catalog, platform interfaces, golden path templates,
platform API contracts, and guardrails for self-service AOIS capabilities.

## Why It Matters In AOIS

AOIS-P now has visibility, access control, release controls, and model delivery
tracking. Without platform patterns, every team would reimplement those controls
in slightly different ways.

v30 turns repeated controls into reusable platform capabilities while still
blocking incomplete or unsafe abstractions.

## How To Use This Version

Start with `notes.md`, then inspect:

- `platform/aois-p/internal-platform-patterns.plan.json`
- `examples/validate_internal_platform_patterns_plan.py`
- `examples/simulate_internal_platform_patterns.py`

Run:

```bash
python3 -m py_compile examples/validate_internal_platform_patterns_plan.py examples/simulate_internal_platform_patterns.py
python3 examples/validate_internal_platform_patterns_plan.py
python3 examples/simulate_internal_platform_patterns.py
```

Expected simulator result:

```json
{
  "passed_cases": 16,
  "score": 1.0,
  "status": "pass",
  "total_cases": 16
}
```
