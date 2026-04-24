# v8 Introduction

Authoring status: authored

## What This Version Is About

`v8` is GitOps and ArgoCD flow without cluster sync.

It creates a reviewable ArgoCD Application manifest and validator for the `aois-p` Helm chart.

## Why It Matters In AOIS

GitOps turns Git into deployment intent.

That is powerful, but it also means Git changes can become cluster changes, so this version keeps sync gated.

## How To Use This Version

1. inspect the ArgoCD Application
2. inspect the GitOps README
3. run the validator
4. explain why automated sync is disabled
5. do not apply or sync without approval
