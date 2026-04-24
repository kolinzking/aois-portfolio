# v6.5 Introduction

Authoring status: authored

## What This Version Is About

`v6.5` adds workload identity and trust-boundary planning.

It extends the `aois-p` Kubernetes plan with ServiceAccount, RBAC, and NetworkPolicy.

## Why It Matters In AOIS

Running a pod is not enough.

AOIS workloads need explicit identity, minimal permissions, and constrained network reach before live deployment.

## How To Use This Version

1. inspect identity manifests
2. inspect deployment service account wiring
3. run the identity validator
4. explain why the Role is empty
5. do not apply without approval
