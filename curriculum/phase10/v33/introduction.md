# v33 Introduction

Authoring status: authored

## What This Version Is About

v33 turns the v31 multimodal contract and v32 edge/offline contract into
adversarial test surfaces. It asks whether AOIS-P can handle prompt injection,
hidden instructions, sensitive disclosure, poisoning, unsafe output handling,
excessive agency, unbounded consumption, edge cache manipulation, fallback
abuse, and policy confusion.

## Why It Matters In AOIS

Controls that look correct in a normal path may fail under hostile input or
ambiguous state. A multimodal document can carry hidden instructions. A stale
edge cache can carry outdated policy. A fallback route can cross a residency
boundary. A tool registry can give an agent too much power.

v33 makes those failures testable without attacking live systems.

## How To Use This Version

Use the v33 plan to review sanitized red-team cases only. Every case must have:

- written authorization and rules of engagement
- approved scope and local synthetic target
- sanitized payload label
- policy, tool, and data-boundary checks
- telemetry and sanitized evidence
- severity, mitigation owner, and regression status
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v33 Contents](CONTENTS.md)
- Next: [v33 - Adversarial Testing And Red Teaming](notes.md)
<!-- AOIS-NAV-END -->
