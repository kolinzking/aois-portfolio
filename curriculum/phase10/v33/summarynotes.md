# v33 Summary Notes

Authoring status: authored

## What Was Built

v33 adds a local adversarial testing and red-team contract:

- `frontier/aois-p/adversarial-red-teaming.plan.json`
- `examples/validate_adversarial_red_teaming_plan.py`
- `examples/simulate_adversarial_red_teaming.py`

The simulator decides whether a sanitized red-team case is recorded, blocked,
held, regression-required, or escalated.

## What Was Learned

Key controls:

- authorization
- rules of engagement
- scope boundary
- local synthetic target
- sanitized payload label
- prompt injection and indirect injection tests
- leakage, disclosure, poisoning, output handling, agency, retrieval, consumption, cache, fallback, and policy-confusion scenarios
- telemetry and sanitized evidence
- severity
- mitigation owner
- regression status

## Core Limitation Or Tradeoff

v33 does not run a red team, call a live model, generate attack payloads,
execute exploits, call tools, use the network, call providers, access secrets,
exfiltrate data, or approve live testing. It models the governance and evidence
path before any live adversarial work begins.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v33 Benchmark](benchmark.md)
- Next: [v33 Looking Forward](looking-forward.md)
<!-- AOIS-NAV-END -->
