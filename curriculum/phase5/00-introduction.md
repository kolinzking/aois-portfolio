# Phase 5 Introduction

Authoring status: authored

Phase 5 is Inference and GPU Engineering.

Phase 4 taught cloud governance without creating cloud resources.
Phase 5 moves AOIS from model consumer toward inference operator.

## Phase Objective

Understand what changes when AOIS owns model execution instead of only calling external model APIs.

## Phase Versions

- `v13` GPU-backed inference service contract
- `v13.5` GPU infrastructure operations
- `v14` high-throughput inference serving
- `v14.5` batching, caching, and latency/throughput tradeoffs
- `v15` fine-tuning and adaptation
- `v15.5` quantization and memory economics

## Resource Rule

GPU actions are gated.

This phase may author plans, validators, and simulations, but it must not install drivers, download models, build images, run GPU containers, or consume paid GPU resources without explicit approval.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../READING-ORDER.md)
- Previous: [Phase 5 Contents](CONTENTS.md)
- Next: [v13 Start Here](v13/00-start-here.md)
<!-- AOIS-NAV-END -->
