# Phase 4 Introduction

Authoring status: authored

Phase 4 is Enterprise Cloud.

Phase 3 built infrastructure and GitOps planning.
Phase 4 maps those concepts onto managed cloud services while keeping cloud spend, credentials, and deployment gated.

## Phase Objective

Understand managed-cloud equivalents without blindly creating cloud resources:

- `v10` managed model layer planning
- `v10.5` managed agent tradeoff planning
- `v11` event-driven cloud workflow planning
- `v12` managed runtime governance planning

## Resource Rule

Cloud actions are gated.

This phase may author plans and validators, but it must not call AWS, create Bedrock resources, invoke models, deploy Lambda, create EKS clusters, use credentials, or spend money without explicit approval.

## AOIS Direction

The Phase 4 spine is:

`managed model plan -> managed agent tradeoff -> event workflow -> managed runtime governance`
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [Phase 4 Contents](01-contents.md)
- Next: [v10 Start Here](../v10/00-start-here.md)
<!-- AOIS-NAV-END -->
