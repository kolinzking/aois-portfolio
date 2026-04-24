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
| 2026-04-24 | Created isolated `.venv` and installed FastAPI/Uvicorn with `--no-cache-dir` | `41M` repo, `32M` `.venv` | No persistent runtime |
| 2026-04-24 | Validated `v0.6` FastAPI runtime on `127.0.0.1:8006` and stopped it | `41M` repo, `32M` `.venv` | Temporary uvicorn used about `45MB RSS`; stopped after validation |
| 2026-04-24 | Implemented checkpoint/resume persistence scripts | `41M` repo, `32M` `.venv` | No persistent runtime |
| 2026-04-24 | Authored `v0.7` provider-neutral LLM dry-run lesson and support pack | `41M` repo, `32M` `.venv` | No provider call, no network, no persistent runtime; memory snapshot `15Gi` total, `8.8Gi` used, `6.4Gi` available, swap unused |
| 2026-04-24 | Authored `v0.8` Postgres schema design and local validator without running a database | `41M` repo, `32M` `.venv` | No database server, no install, no persistent runtime; memory snapshot `15Gi` total, `9.1Gi` used, `6.1Gi` available, swap unused |
| 2026-04-24 | Closed Phase 0 capstone and looking-forward documents | `41M` repo, `32M` `.venv` | No install, no provider call, no database server, no persistent runtime; memory snapshot `15Gi` total, `9.1Gi` used, `6.2Gi` available, swap unused |
| 2026-04-24 | Authored `v1` structured AI endpoint contract and validated local FastAPI route | `41M` repo, `32M` `.venv` | Temporary uvicorn on `127.0.0.1:8006` stopped after validation; no provider call, no install, no persistent runtime; memory snapshot `15Gi` total, `9.1Gi` used, `6.1Gi` available, swap unused |
| 2026-04-24 | Authored `v2` provider-neutral model routing and validated local route decisions | `41M` repo, `32M` `.venv` | Temporary uvicorn on `127.0.0.1:8006` stopped after validation; no provider call, no install, no persistent runtime; memory snapshot `15Gi` total, `9.2Gi` used, `6.1Gi` available, swap unused |
| 2026-04-24 | Authored `v3` local reliability baseline and Phase 1 closeout | `42M` repo, `32M` `.venv` | No install, no provider call, no open portfolio port, no persistent runtime; memory snapshot `15Gi` total, `9.3Gi` used, `6.0Gi` available, swap unused |
| 2026-04-24 | Authored `v4` containerization plan and validator without Docker build/run | `42M` repo, `32M` `.venv` | No Docker image, no container, no install, no persistent runtime; memory snapshot `15Gi` total, `9.0Gi` used, `6.3Gi` available, swap unused |
