# Phase 3 Introduction

Authoring status: authored

Phase 3 is Infrastructure and GitOps.

Phase 2 created packaging and security foundations.
Phase 3 moves toward Kubernetes deployment discipline without sacrificing the resource controls required on this shared server.

## Phase Objective

Build infrastructure literacy around AOIS:

- `v6` Kubernetes manifest planning and resource limits
- `v6.5` workload identity and trust boundaries
- `v7` Helm packaging
- `v8` GitOps and ArgoCD flow
- `v9` autoscaling and event-driven scaling concepts

## Resource Rule

Kubernetes changes are gated.

Manifests may be authored and validated locally, but `kubectl apply`, Helm installs, ArgoCD apps, namespaces, CRDs, and controllers require explicit approval and resource tracking.

## AOIS Direction

The Phase 3 spine is:

`container plan -> Kubernetes manifests -> identity -> Helm -> GitOps -> autoscaling`
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../READING-ORDER.md)
- Previous: [Phase 3 Contents](CONTENTS.md)
- Next: [v6 Start Here](v6/00-start-here.md)
<!-- AOIS-NAV-END -->
