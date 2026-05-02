# v5 Summary Notes

Authoring status: authored

## What Was Built

Local security inspection:

- prompt-injection signal detection
- secret-like redaction
- structured findings
- CLI inspection
- API inspection route

## What Was Learned

LLM security begins before model calls.

Inputs can contain instructions and secrets, so AOIS needs inspection before provider, log, and deployment boundaries.

## Core Limitation Or Tradeoff

Pattern matching is not complete security.

It is a first guardrail that prepares AOIS for stronger policy, red-teaming, and runtime controls later.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v5 Benchmark](07-benchmark.md)
- Next: [v5 Looking Forward](09-looking-forward.md)
<!-- AOIS-NAV-END -->
