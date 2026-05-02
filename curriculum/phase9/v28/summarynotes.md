# v28 Summary Notes

Authoring status: authored

## What Was Built

A local AOIS-P delivery release-control contract:

- release-safety plan
- validator
- simulator
- five pipeline stages
- 16 release decision cases

## What Was Learned

- release safety is more than CI passing
- workflow permissions can be a release risk
- policy and dashboard regressions belong in delivery gates
- artifact digest, provenance, signature, and verification are separate controls
- environment approval is distinct from tests
- rollout health and rollback readiness must gate release
- model rollout and feature flags are AI delivery controls

## Core Limitation Or Tradeoff

v28 does not create a live CI/CD workflow, build an image, push an artifact,
sign anything, deploy to Kubernetes, shift traffic, change feature flags, or
change model endpoints. It intentionally proves the release-control contract
before any automation can affect live systems.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v28 Benchmark](benchmark.md)
- Next: [v28 Looking Forward](looking-forward.md)
<!-- AOIS-NAV-END -->
