# Phase 2 Introduction

Authoring status: authored

Phase 2 is Containerization and Security.

Phase 1 built the intelligence core:

`structured endpoint -> provider gate -> model routing -> reliability baseline`

Phase 2 prepares that service to become portable and harder to misuse.

## Phase Objective

Build a safe local packaging and security foundation:

- `v4` creates a container plan without building or running images by default
- `v5` adds API and LLM security controls before broader deployment

## Resource Rule

Docker builds and container runs are gated.

This server already hosts the primary AOIS project, so the portfolio project must not create images, containers, volumes, or networks unless the expected footprint is approved first.

## AOIS Direction

The Phase 2 spine is:

`service -> container plan -> resource limits -> security checks -> safer deployment path`
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../READING-ORDER.md)
- Previous: [Phase 2 Contents](CONTENTS.md)
- Next: [v4 Start Here](v4/00-start-here.md)
<!-- AOIS-NAV-END -->
