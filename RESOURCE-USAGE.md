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
| 2026-04-24 | Authored `v5` local API/LLM security checks and Phase 2 closeout | `42M` repo, `32M` `.venv` | No install, no provider call, no open portfolio port, no persistent runtime; memory snapshot `15Gi` total, `9.3Gi` used, `6.0Gi` available, `512Ki` swap used |
| 2026-04-24 | Authored `v6` Kubernetes manifest plan and validator without applying resources | `42M` repo, `32M` `.venv` | No `kubectl apply`, no namespace/resource created, no install, no persistent runtime; memory snapshot `15Gi` total, `9.3Gi` used, `6.0Gi` available, `512Ki` swap used |
| 2026-04-24 | Authored `v6.5` workload identity/RBAC/network-policy plan without applying resources | `42M` repo, `32M` `.venv` | No `kubectl apply`, no RBAC/NetworkPolicy resource created, no install, no persistent runtime; memory snapshot `15Gi` total, `9.2Gi` used, `6.0Gi` available, `512Ki` swap used |
| 2026-04-24 | Authored `v7` Helm chart plan and validator without installing a release | `42M` repo, `32M` `.venv` | No Helm install/upgrade, no Kubernetes resource created, no install, no persistent runtime; memory snapshot `15Gi` total, `9.4Gi` used, `5.8Gi` available, `512Ki` swap used |
| 2026-04-24 | Authored `v8` GitOps/ArgoCD plan and validator without applying or syncing | `42M` repo, `32M` `.venv` | No ArgoCD app created, no sync, no `kubectl apply`, no install, no persistent runtime; memory snapshot `15Gi` total, `9.1Gi` used, `6.1Gi` available, `512Ki` swap used |
| 2026-04-24 | Authored `v9` autoscaling/event-driven plan and Phase 3 closeout without applying resources | `43M` repo, `32M` `.venv` | No HPA apply, no KEDA install, no extra replicas, no install, no persistent runtime; memory snapshot `15Gi` total, `9.2Gi` used, `6.1Gi` available, `512Ki` swap used |
| 2026-04-24 | Authored `v10` managed model layer plan without cloud calls | `43M` repo, `32M` `.venv` | No AWS/cloud call, no credentials, no provider call, no install, no persistent runtime; memory snapshot `15Gi` total, `8.9Gi` used, `6.3Gi` available, `512Ki` swap used |
| 2026-04-24 | Authored `v10.5` managed-agent tradeoff plan without cloud calls | `43M` repo, `32M` `.venv` | No cloud agent, no credentials, no provider call, no install, no persistent runtime; memory snapshot `15Gi` total, `9.0Gi` used, `6.3Gi` available, `512Ki` swap used |
| 2026-04-24 | Authored `v11` event-driven workflow plan without cloud calls | `43M` repo, `32M` `.venv` | No event bus, queue, function, DLQ, provider call, credentials, install, or persistent runtime; memory snapshot `15Gi` total, `9.2Gi` used, `6.1Gi` available, `512Ki` swap used |
| 2026-04-24 | Authored `v12` managed-runtime governance plan and Phase 4 closeout without cloud calls | `43M` repo, `32M` `.venv` | No managed cluster, node pool, identity, dashboard, budget alarm, provider call, credentials, install, or persistent runtime; memory snapshot `15Gi` total, `9.3Gi` used, `5.9Gi` available, `768Ki` swap used |
| 2026-04-24 | Authored `v13` GPU-backed inference service plan without GPU runtime | `43M` repo, `32M` `.venv` | No GPU runtime, model download, driver install, container build, provider call, credentials, or persistent runtime; memory snapshot `15Gi` total, `9.2Gi` used, `6.1Gi` available, `1.5Mi` swap used |
| 2026-04-24 | Authored `v13.5` GPU infrastructure operations plan without applying resources | `43M` repo, `32M` `.venv` | No `kubectl apply`, GPU operator install, device plugin install, GPU runtime, driver install, provider call, credentials, or persistent runtime; memory snapshot `15Gi` total, `9.0Gi` used, `6.2Gi` available, `1.5Mi` swap used |
| 2026-04-24 | Authored `v14` high-throughput inference serving plan without runtime | `43M` repo, `32M` `.venv` | No inference runtime, GPU runtime, model download, container build, provider call, credentials, or persistent runtime; memory snapshot `15Gi` total, `9.3Gi` used, `6.0Gi` available, `1.5Mi` swap used |
| 2026-04-24 | Authored `v14.5` performance caching plan without runtime | `44M` repo, `32M` `.venv` | No Redis install, cache service, cache entries, inference runtime, provider call, credentials, or persistent runtime; memory snapshot `15Gi` total, `9.2Gi` used, `6.1Gi` available, `1.5Mi` swap used |
| 2026-04-24 | Authored `v15` fine-tuning and adaptation plan without training | `44M` repo, `32M` `.venv` | No training job, dataset upload, model download, GPU runtime, provider call, credentials, or persistent runtime; memory snapshot `15Gi` total, `9.7Gi` used, `5.6Gi` available, `1.5Mi` swap used |
| 2026-04-24 | Authored `v15.5` quantization and memory economics plan and Phase 5 closeout without runtime | `44M` repo, `32M` `.venv` | No quantization job, model download, GPU runtime, inference runtime, provider call, credentials, or persistent runtime; memory snapshot `15Gi` total, `9.4Gi` used, `5.9Gi` available, `1.5Mi` swap used |
| 2026-04-24 | Authored `v16` unified telemetry plan without runtime | `44M` repo, `32M` `.venv` | No OpenTelemetry install, collector, Prometheus, Loki, Tempo, persistent storage, provider call, credentials, or persistent runtime; memory snapshot `15Gi` total, `9.6Gi` used, `5.6Gi` available, `1.5Mi` swap used |
| 2026-04-25 | Authored `v16.5` agent and incident tracing plan without runtime | `253M` repo, `241M` `.venv` | No agent runtime, tool calls, provider call, collector, trace backend, install, persistent storage, or persistent runtime; `.venv` footprint increase observed in existing site-packages, not changed by this checkpoint; memory snapshot `15Gi` total, `9.6Gi` used, `5.7Gi` available, `19Mi` swap used |
| 2026-04-25 | Authored `v17` event streaming plan and simulator without broker runtime | `264M` repo, `251M` `.venv` | No Kafka, Redis Streams, NATS, broker, producer, consumer, container, cloud call, install, persistent storage, or persistent runtime; memory snapshot `15Gi` total, `9.5Gi` used, `5.8Gi` available, `19Mi` swap used |
