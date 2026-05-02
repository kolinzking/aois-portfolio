# v13.5 Introduction

Authoring status: authored

## What This Version Is About

`v13.5` moves below the GPU inference service contract into infrastructure operations.

It teaches how GPU workloads become schedulable and observable.

The lesson is plan-only. Nothing is applied to Kubernetes and no GPU software is installed.

## Why It Matters In AOIS

A GPU inference service cannot run safely if the platform cannot expose GPU resources, schedule workloads to the right nodes, isolate GPU capacity, and show which pods consume which GPU resources.

This is why GPU infrastructure is its own discipline.

## How To Use This Version

Use this lesson as an operations readiness check.

Run the validator and explain every control. You are ready for `v14` only when you can explain what would break if GPU scheduling or observability is missing.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v13.5 Contents](CONTENTS.md)
- Next: [v13.5 - GPU Infrastructure Operations Without Applying Resources](notes.md)
<!-- AOIS-NAV-END -->
