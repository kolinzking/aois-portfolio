# AOIS Resource Policy

This repository is secondary work on a shared 16 GB RAM server.

The primary project on the server takes priority.
AOIS work must not consume excessive memory, disk, CPU, network, or long-running process capacity.

## Project Identity

Use `aois-p` for this portfolio/curriculum project when naming server-side resources.

Reserved naming:

- repo: `aois-portfolio`
- short name: `aois-p`
- Kubernetes namespace: `aois-p`
- labels: `project=aois-p`, `purpose=portfolio-lab`
- local services: `aois-p-*`
- future Hetzner resources, if ever needed: `aois-p-*`

Do not name secondary resources simply `aois`.
That name is reserved for the primary AOIS project.

## Hard Rules

- Do not run long-lived services unless they are required for a short validation lab.
- Stop local servers immediately after validation.
- Do not run heavy benchmarks by default.
- Do not install dependencies without explicit approval.
- Do not pull large images, models, datasets, or package caches without explicit approval.
- Do not start Docker, Kubernetes, database, GPU, or model-serving workloads without explicit approval.
- Do not use cloud resources, paid APIs, secrets, or deployment credentials without explicit approval.
- Keep validation commands lightweight and local.
- Prefer Python standard library and shell validation during Phase 0.
- Do not create a second local Kubernetes cluster such as minikube while K3s already exists on this server.
- Do not run portfolio workloads in the default namespace or primary AOIS namespace.
- Do not run portfolio workloads without explicit CPU and memory limits.

## Resource Tracking Rule

Every checkpoint must report:

- current `aois-portfolio` disk footprint
- whether any new persistent files, services, images, volumes, or caches were created
- whether any runtime process was left running

Before any action expected to add more than `50 MB` disk or use more than `250 MB` RAM, stop and ask.

Before any action expected to add more than `500 MB` disk or use more than `1 GB` RAM, treat it as a high-risk action and require explicit approval.

Because the primary AOIS project recently hit OOM pressure, memory safety takes priority over curriculum speed.

## Local Service Rule

If a local service is needed for validation:

1. bind to `127.0.0.1`
2. use a high non-privileged port
3. run only for the duration of the check
4. stop it immediately after the check
5. do not leave background processes running

## Disk Rule

Avoid generating large artifacts.

Before adding anything likely to exceed `50 MB`, stop and ask.

Examples requiring approval:

- container images
- model weights
- datasets
- trace archives
- database dumps
- generated media
- dependency caches

## Memory Rule

Avoid commands expected to consume more than `1 GB` RAM.

Examples requiring approval:

- model inference
- vector database services
- Kubernetes clusters
- Docker Compose stacks
- load tests
- browser automation
- large test suites

For routine AOIS portfolio work, prefer commands expected to stay below `250 MB` RAM.
FastAPI or Kubernetes practice must use explicit resource limits when run on the shared server.

## Safe Default Commands

These are acceptable by default when needed:

- `rg`
- `sed`
- `git status`
- `git diff`
- `git add`
- `git commit`
- `bash -n`
- `python3 -m py_compile`
- short-lived local scripts in `scripts/`

## Current Phase 0 Resource Posture

Phase 0 should remain lightweight:

- shell scripts
- Markdown curriculum
- small Python files
- short local HTTP server checks
- no persistent services
- no containers
- no databases yet unless explicitly started for a bounded lab

The AOIS rebuild should preserve the primary server workload.
