# v6 Introduction

Authoring status: authored

## What This Version Is About

`v6` is Kubernetes planning without applying resources.

It creates an `aois-p` namespace manifest set with quota, limits, deployment, service, and validation.

## Why It Matters In AOIS

AOIS needs infrastructure discipline before live deployment.

On this shared server, Kubernetes practice must not create workloads unless resource impact is approved.

## How To Use This Version

1. inspect the manifests
2. run the validator
3. explain each resource
4. explain why `kubectl apply` is gated
5. do not create cluster resources without approval
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v6 Contents](01-contents.md)
- Next: [v6 - Kubernetes Plan Without Applying Resources](03-notes.md)
<!-- AOIS-NAV-END -->
