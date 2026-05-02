# Phase 1 Introduction

Authoring status: authored

Phase 1 is the Intelligence Core.

Phase 0 built the foundation:

`Linux -> Bash -> Git -> HTTP -> Python -> API -> LLM dry-run -> persistence schema`

Phase 1 starts turning that foundation into an AI-capable service without losing resource discipline.

## Phase Objective

Build the first structured intelligence layer for AOIS:

- `v1` creates the structured AI analysis endpoint contract
- `v2` adds model routing, fallbacks, latency, and cost choices
- `v3` adds reliability, tracing, validation, and evaluation baseline

## Resource Rule

Real provider calls remain gated.

The portfolio project must not call OpenAI, Groq, Anthropic, or any other paid/external provider unless the provider, budget, key handling, and request limit are explicitly approved.

## AOIS Direction

The Phase 1 spine is:

`incident -> structured prompt contract -> provider-gated analysis -> routing -> tracing -> evaluation`

The goal is not to make AI seem magical.
The goal is to make AI behavior inspectable, bounded, and explainable.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../READING-ORDER.md)
- Previous: [Phase 1 Contents](CONTENTS.md)
- Next: [v1 Start Here](v1/00-start-here.md)
<!-- AOIS-NAV-END -->
