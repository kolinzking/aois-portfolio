# v14.5 Introduction

Authoring status: authored

## What This Version Is About

`v14.5` is about performance engineering and caching.

It compares no-cache, prompt-cache, prefix-reuse, and response-cache placeholder paths without starting Redis or writing cache entries.

## Why It Matters In AOIS

Caching can reduce latency and cost, but it can also return stale or unsafe outputs.

AOIS needs caching discipline before cache infrastructure exists.

## How To Use This Version

Run the validator and simulator.

Focus on what each cache layer saves and what correctness boundary it introduces.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v14.5 Contents](01-contents.md)
- Next: [v14.5 - Performance Engineering And Caching Without Runtime](03-notes.md)
<!-- AOIS-NAV-END -->
