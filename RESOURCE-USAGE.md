# AOIS Portfolio Resource Usage

This file tracks the resource footprint of `aois-p`, the AOIS portfolio/curriculum project.

The primary AOIS project takes priority on this 16 GB RAM server.

## Current Baseline

Measured after the `v0.5` checkpoint:

- Date: 2026-04-24
- Repo path: `/home/collins/aois-portfolio`
- Disk footprint: `9.1M`
- Memory snapshot: `15Gi` total, `9.1Gi` used, `6.2Gi` available, `4.0Gi` swap unused
- Persistent AOIS portfolio services running: none
- Containers/images added by AOIS portfolio: none
- External API/cloud usage: none
- Installs performed by AOIS portfolio: none

## Tracking Rules

Update this file when AOIS portfolio work:

- adds dependencies
- creates a virtual environment
- creates a container image
- starts a persistent service
- creates Kubernetes objects
- creates database files or volumes
- downloads large artifacts
- changes expected memory or disk usage materially

Small Markdown/code edits do not need a new row unless they are part of a checkpoint.

## Ledger

| Date | Change | Disk footprint | Runtime impact |
|---|---|---:|---|
| 2026-04-24 | Baseline after authoring through `v0.5` | `9.1M` | No persistent runtime |
| 2026-04-24 | Added server assessment and `aois-p` resource-management plan | `9.1M` before commit | No persistent runtime |
| 2026-04-24 | Authored `v0.6` FastAPI lesson/code shape without installing dependencies | `9.1M` | No persistent runtime |
