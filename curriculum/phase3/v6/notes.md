# v6 - Kubernetes Plan Without Applying Resources

Estimated time: 10-12 focused hours

Authoring status: authored

Resource posture: manifest authoring and local validation only, no `kubectl apply`

## What This Builds

This version builds the AOIS portfolio Kubernetes plan:

- `k8s/aois-p/namespace.yaml`
- `k8s/aois-p/resource-quota.yaml`
- `k8s/aois-p/limit-range.yaml`
- `k8s/aois-p/deployment.yaml`
- `k8s/aois-p/service.yaml`
- `k8s/aois-p/kustomization.yaml`
- `examples/validate_k8s_plan.py`

It teaches:

- namespace separation
- ResourceQuota
- LimitRange
- Deployment
- Service
- probes
- resource requests and limits
- why Kubernetes apply is resource-gated

## Why This Exists

AOIS must eventually run on infrastructure, but this server already hosts the primary AOIS project.

The portfolio project can practice Kubernetes design safely by writing and validating manifests before applying anything.

## AOIS Connection

The AOIS path is now:

`container plan -> Kubernetes namespace -> resource limits -> deployment shape -> service boundary`

The namespace is `aois-p`, making portfolio resources unambiguous if they are ever applied.

## Learning Goals

By the end of this version you should be able to:

- explain namespace separation
- explain ResourceQuota and LimitRange
- explain Deployment and Service
- explain readiness and liveness probes
- explain resource requests and limits
- explain why `kubectl apply` is gated
- validate the manifest plan without touching the cluster

## Resource Gate

Do not run:

```bash
kubectl apply
helm install
kubectl create namespace
```

Allowed by default:

- read manifests
- run `python3 examples/validate_k8s_plan.py`
- inspect existing cluster state with approved read-only commands

Applying this plan later requires explicit approval because it would create server-visible resources in namespace `aois-p`.

## Prerequisites

You should have completed:

- Phase 2
- `v4` containerization plan
- `v5` security foundations

Required check:

```bash
python3 -m py_compile examples/validate_k8s_plan.py
python3 examples/validate_k8s_plan.py
```

## Core Concepts

## Namespace

A namespace separates Kubernetes resources.

This curriculum uses:

```text
aois-p
```

That distinguishes portfolio resources from the primary AOIS project.

## ResourceQuota

ResourceQuota caps total namespace usage.

This plan limits:

- CPU requests and limits
- memory requests and limits
- pod count

## LimitRange

LimitRange supplies default container requests and limits.

It reduces the chance of unbounded workloads.

## Deployment

A Deployment describes desired pod replicas and pod template.

This plan uses:

- one replica
- resource limits
- provider calls disabled
- non-root security context
- health probes

## Service

A Service gives stable in-cluster access to pods.

This plan uses `ClusterIP`, not public ingress.

## Build

Inspect:

```bash
sed -n '1,220p' k8s/aois-p/deployment.yaml
sed -n '1,160p' k8s/aois-p/resource-quota.yaml
sed -n '1,160p' k8s/aois-p/service.yaml
```

Compile validator:

```bash
python3 -m py_compile examples/validate_k8s_plan.py
```

Run validator:

```bash
python3 examples/validate_k8s_plan.py
```

Expected:

```json
{
  "kubectl_apply_ran": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer:

1. Which namespace is used?
2. Which file caps total namespace usage?
3. Which file sets default container limits?
4. Which file defines the pod template?
5. Which file defines in-cluster access?

Answer key:

1. `aois-p`
2. `resource-quota.yaml`
3. `limit-range.yaml`
4. `deployment.yaml`
5. `service.yaml`

## Break Lab

Do not skip this.

### Option A - Missing Limits

In a scratch copy, remove deployment resource limits.

Expected risk:

- pod could consume more CPU or memory than intended

### Option B - Wrong Namespace

In a scratch copy, change `aois-p` to `aois`.

Expected risk:

- portfolio resources become confusing or collide with primary project naming

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. no `kubectl apply` is run
4. no namespace is created
5. you can explain each manifest and resource limit

## Common Mistakes

- applying manifests before reading them
- using ambiguous namespace names
- omitting resource limits
- exposing services publicly too early
- confusing image build with Kubernetes deployment
- assuming manifests are harmless after apply

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_k8s_plan.py
```

Read the `missing` list and inspect the referenced manifest.

If you want to apply:

- stop
- confirm cluster target
- confirm namespace
- confirm CPU and memory budget
- get explicit approval
- record resource usage after apply

## Benchmark

Measure:

- validator compile result
- validator status
- whether `kubectl apply` ran
- repo disk footprint
- memory snapshot

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can inspect, validate, break, explain, and defend Kubernetes manifests without applying them. |
| 4/5 | Plan validates, but one Kubernetes concept needs review. |
| 3/5 | Files exist, but resource or namespace reasoning is weak. |
| 2/5 | Manifests exist, but cluster risk is unclear. |
| 1/5 | Kubernetes still means blindly applying YAML. |

Minimum pass: `4/5`.

## Architecture Defense

Why manifests before apply?

Because applying manifests creates real server-visible resources.
The design must be correct before the cluster is changed.

Why `aois-p` namespace?

Because portfolio resources must be unambiguous and separate from primary AOIS.

Why quotas and limits first?

Because this server already had memory pressure history, and portfolio workloads must stay bounded.

## 4-Layer Tool Drill

Tool: Kubernetes Deployment

1. Plain English
It tells Kubernetes how to run the app pods.

2. System Role
It turns AOIS from local service into desired cluster workload shape.

3. Minimal Technical Definition
It is a Kubernetes controller object that manages ReplicaSets and Pods from a template.

4. Hands-on Proof
The validator checks namespace, replica count, resource limits, probes, and security context without applying the manifest.

## 4-Level System Explanation Drill

1. Simple English
AOIS now has a Kubernetes plan.

2. Practical Explanation
I can inspect manifests and validate resource controls without touching the cluster.

3. Technical Explanation
`v6` adds `aois-p` namespace, quota, limits, deployment, service, kustomization, and a local validator.

4. Engineer-Level Explanation
AOIS now separates Kubernetes infrastructure design from cluster mutation, preserving shared-server safety while preparing for resource-bounded deployment.

## Failure Story

Representative failure:

- Symptom: a portfolio pod consumes too much memory
- Root cause: manifest was applied without ResourceQuota, LimitRange, or container limits
- Fix: add quota, limits, and one-replica deployment
- Prevention: validate manifests before applying
- What this taught me: Kubernetes safety starts before `kubectl apply`

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v6` solve in AOIS?
2. What is a namespace?
3. Why is the namespace `aois-p`?
4. What does ResourceQuota do?
5. What does LimitRange do?
6. What does a Deployment do?
7. What does a Service do?
8. Why are probes useful?
9. Why is `kubectl apply` gated?
10. Explain Deployment using the 4-layer tool rule.
11. Explain `v6` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v6` solve in AOIS?

It prepares AOIS for Kubernetes deployment with namespace separation and resource controls without changing the cluster.

2. What is a namespace?

A Kubernetes scope for grouping and separating resources.

3. Why is the namespace `aois-p`?

To distinguish portfolio resources from primary AOIS resources.

4. What does ResourceQuota do?

It caps total resource usage in a namespace.

5. What does LimitRange do?

It sets default or allowed resource requests and limits for containers.

6. What does a Deployment do?

It manages desired pod replicas from a pod template.

7. What does a Service do?

It provides stable networking to matching pods.

8. Why are probes useful?

They let Kubernetes check whether a container is ready or healthy.

9. Why is `kubectl apply` gated?

It mutates the live cluster and can consume CPU, memory, network, and namespace resources.

10. Explain Deployment using the 4-layer tool rule.

- Plain English: it tells Kubernetes how to run app pods.
- System Role: it becomes the workload controller for AOIS.
- Minimal Technical Definition: it manages ReplicaSets and Pods from a desired template.
- Hands-on Proof: the local validator checks deployment safety fields before apply.

11. Explain `v6` using the 4-level system explanation rule.

- Simple English: AOIS has a Kubernetes plan.
- Practical explanation: I can inspect and validate manifests safely.
- Technical explanation: `v6` defines namespace, quota, limits, deployment, service, and kustomization.
- Engineer-level explanation: AOIS now has a cluster deployment design that keeps portfolio resources isolated and bounded before any live cluster mutation.

## Connection Forward

`v6` creates the cluster workload plan.

`v6.5` adds identity and trust boundaries so workloads can be understood as authenticated actors, not just pods.
