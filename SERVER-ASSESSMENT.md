# AOIS Server Assessment

Date: 2026-04-24

Scope: read-only inspection of the current Hetzner server.

This server hosts the primary AOIS project.
The AOIS portfolio project must use the `aois-p` name and must not interfere with the primary workload.

## Host Capacity Snapshot

- CPU cores: `8`
- Memory: `15Gi`
- Swap: `4.0Gi`
- Root disk: `150G`
- Root disk used: `23G`
- Root disk available: `122G`
- AOIS portfolio repo footprint at assessment time: `9.1M`

## Current Load Snapshot

- Host load average was around `9.5` on `8` CPU cores during inspection.
- K3s node metrics reported `8000m` CPU, `100%`.
- K3s node memory reported about `7508Mi`, `60%`.
- System memory snapshot showed about `6.2Gi` available and swap unused.

## Existing Infrastructure

Installed tooling observed:

- `k3s`
- `kubectl`
- `docker`
- `helm`

Running services observed:

- `k3s`
- `docker`
- `containerd`
- `nginx`
- `code-server`
- standard system services

Kubernetes cluster:

- single-node K3s cluster
- node name: `aois`
- Kubernetes version: `v1.34.6+k3s1`
- OS: Ubuntu 24.04.4 LTS
- container runtime: containerd

Namespaces observed:

- `aois`
- `argocd`
- `cert-manager`
- `chaos-mesh`
- `default`
- `falco`
- `kafka`
- `keda`
- `kube-system`

Notable workloads observed:

- primary `aois` pod
- Argo CD
- cert-manager
- Chaos Mesh
- Falco
- Kafka / Strimzi
- KEDA
- Traefik
- metrics-server

## Resource Governance Findings

No Kubernetes `ResourceQuota` objects were found.

No Kubernetes `LimitRange` objects were found.

This means new workloads can potentially consume more CPU or memory than intended unless explicit limits are added.

## Host-Level CPU Concern

Processes named `xmrig` and `xmr_linux_amd64` were observed consuming very high CPU at the host level.

AOIS portfolio work must not modify, stop, or assume ownership of these processes without explicit user instruction.

However, their presence means the server should be treated as CPU-constrained.

## Recommendation

Do not install minikube.

Reason:

- K3s already exists.
- The node is already CPU-saturated.
- Running another local Kubernetes cluster would duplicate overhead.
- The primary AOIS project recently had OOM pressure.

Use this plan instead:

1. Keep Phase 0 and Phase 1 mostly local and lightweight.
2. Use the existing K3s cluster for read-only learning first.
3. When write practice is needed, create a separate `aois-p` namespace only after explicit approval.
4. Add `ResourceQuota` and `LimitRange` to `aois-p` before deploying anything.
5. Keep `aois-p` workloads tiny and short-lived.
6. Do not share the primary `aois` namespace for portfolio practice.

## Proposed `aois-p` Limits For Later Approval

If Kubernetes write practice is approved later, start with:

- namespace: `aois-p`
- CPU request ceiling: low
- memory ceiling: low
- no persistent volumes by default
- no LoadBalancer services by default
- no cluster-wide controllers
- no chaos experiments against primary namespaces

Example target envelope:

- default container memory request: `64Mi`
- default container memory limit: `128Mi`
- default container CPU request: `25m`
- default container CPU limit: `100m`
- namespace memory hard limit: `512Mi`
- namespace CPU hard limit: `500m`

These are intentionally small because this is a shared server.
