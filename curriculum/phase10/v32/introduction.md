# v32 Introduction

Authoring status: authored

## What This Version Is About

v32 moves AOIS-P from multimodal capability into deployment placement. The
question is no longer only whether AOIS-P may analyze a signal. The question is
where inference may run when memory, compute, power, latency, connectivity,
cache, freshness, privacy, observability, update, and rollback constraints all
matter.

## Why It Matters In AOIS

Edge and offline inference can reduce latency, preserve privacy, and keep a
site working during network loss. Those benefits are only useful when the
system can prove that the model fits the device, the cache is ready, the local
model is fresh, telemetry can be recovered, and updates can be rolled back.

## How To Use This Version

Use the plan, validator, and simulator to compare:

- central cloud when online central controls pass
- edge online when a known device and budgeted model can run safely
- offline edge when cache, sync, freshness, and telemetry buffers are ready
- block when policy, residency, privacy, update, rollback, size, memory, or latency fails
- hold when more measurement or preparation is required
- fallback when edge fails but central fallback is allowed
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v32 Contents](CONTENTS.md)
- Next: [v32 - Edge And Offline Inference](notes.md)
<!-- AOIS-NAV-END -->
