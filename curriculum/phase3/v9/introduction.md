# v9 Introduction

Authoring status: authored

## What This Version Is About

`v9` is autoscaling and event-driven planning without scaling resources.

It adds HPA and KEDA-style planning manifests capped at one replica.

## Why It Matters In AOIS

Autoscaling can protect availability, but it also multiplies resource usage.

This version teaches the policy while preventing the portfolio workload from consuming extra capacity.

## How To Use This Version

1. inspect autoscaling manifests
2. run the validator
3. explain HPA and KEDA
4. explain why scaling is capped
5. do not apply or install autoscaling components without approval
