# v14 Introduction

Authoring status: authored

## What This Version Is About

`v14` is about high-throughput inference serving.

It compares serving modes locally:

- serial baseline
- continuous batching placeholder
- cache-aware placeholder

## Why It Matters In AOIS

Inference systems are judged by more than output quality.

They must also meet latency, throughput, cost, and overload expectations.

This version teaches those tradeoffs without starting any runtime.

## How To Use This Version

Run the validator and simulator, then compare throughput gain versus p95 latency.

Focus on why more throughput can be worse if it creates tail-latency or overload problems.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v14 Contents](01-contents.md)
- Next: [v14 - High-Throughput Inference Serving Without Runtime](03-notes.md)
<!-- AOIS-NAV-END -->
