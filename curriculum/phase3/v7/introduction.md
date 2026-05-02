# v7 Introduction

Authoring status: authored

## What This Version Is About

`v7` packages the AOIS Kubernetes plan into a Helm chart.

It creates chart metadata, values, templates, and validation without installing a release.

## Why It Matters In AOIS

AOIS needs reusable deployment configuration.

Helm gives structure, but installing a chart still changes the live cluster, so this version stays validation-only.

## How To Use This Version

1. inspect chart files
2. inspect values
3. inspect templates
4. run the validator
5. explain why `helm install` is gated
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v7 Contents](CONTENTS.md)
- Next: [v7 - Helm Packaging Without Installing A Release](notes.md)
<!-- AOIS-NAV-END -->
