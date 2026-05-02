# v5 Introduction

Authoring status: authored

## What This Version Is About

`v5` adds API and LLM security foundations.

It creates local inspection for prompt-injection signals and secret-like content before provider execution exists.

## Why It Matters In AOIS

AI systems accept natural language, and natural language can contain instructions, secrets, or manipulation attempts.

AOIS needs security checks before model calls, logs, containers, and deployment.

## How To Use This Version

1. inspect `app/security.py`
2. run safe input
3. run prompt-injection input
4. run secret-like input
5. explain redaction and provider gating
6. keep real secrets out of the repo
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v5 Contents](CONTENTS.md)
- Next: [v5 - API And LLM Security Foundations](notes.md)
<!-- AOIS-NAV-END -->
