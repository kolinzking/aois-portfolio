# AOIS Portfolio GitOps Plan

This directory contains desired-state GitOps artifacts for AOIS portfolio.

Resource posture:

- no `kubectl apply`
- no ArgoCD application creation
- no cluster sync
- no namespace/resource creation

The `aois-p` Application is a review artifact until a live GitOps step is explicitly approved.

Before live use:

1. replace `repoURL` with the real repository URL
2. confirm ArgoCD target cluster
3. confirm namespace `aois-p`
4. confirm resource budget
5. record expected resource impact
6. get explicit approval
