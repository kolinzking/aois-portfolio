# v9 - Autoscaling And Event-Driven Planning Without Scaling Resources

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: autoscaling manifest planning only, no autoscaler install, no apply, max replicas capped at 1

## What This Builds

This version builds autoscaling plans:

- `k8s/aois-p/hpa.yaml`
- `k8s/aois-p/keda-scaledobject.plan.yaml`
- `examples/validate_autoscaling_plan.py`

It teaches:

- HorizontalPodAutoscaler
- target workload
- metrics
- min/max replicas
- KEDA-style event-driven scaling concepts
- why autoscaling is gated on the shared server
- why this plan caps replicas at `1`

## Why This Exists

AI infrastructure often needs to scale with load, but uncontrolled scaling can harm other workloads.

On this server, primary AOIS has priority.
So `v9` teaches scaling design while preventing the portfolio project from actually scaling.

## AOIS Connection

The AOIS path is now:

`workload -> metrics -> scaling policy -> resource cap -> future event-driven behavior`

`v9` completes Phase 3 by adding controlled scale reasoning to the Kubernetes/GitOps foundation.

## Learning Goals

By the end of this version you should be able to:

- explain HPA
- explain min and max replicas
- explain CPU utilization target
- explain KEDA at a high level
- explain why autoscaling is resource-gated
- validate autoscaling manifests without applying them
- defend replica caps on a shared server

## Resource Gate

Do not run:

```bash
kubectl apply
helm install keda
kubectl scale
```

Allowed:

- read autoscaling manifests
- run `python3 examples/validate_autoscaling_plan.py`

Live autoscaling requires explicit approval because it can create extra pods and consume CPU/RAM.

## Prerequisites

You should have completed:

- `v6` Kubernetes plan
- `v6.5` workload identity
- `v7` Helm packaging
- `v8` GitOps flow

Required checks:

```bash
python3 -m py_compile examples/validate_autoscaling_plan.py
python3 examples/validate_autoscaling_plan.py
```

## Core Concepts

## HPA

HorizontalPodAutoscaler adjusts replica count based on metrics.

This plan uses CPU utilization as a teaching metric.

## Min Replicas

Minimum replicas is the floor.

This plan uses:

```yaml
minReplicas: 1
```

## Max Replicas

Maximum replicas is the ceiling.

This plan intentionally uses:

```yaml
maxReplicas: 1
```

That means no real scaling can happen from this manifest.

## KEDA

KEDA scales workloads from event sources such as queues, streams, or external metrics.

This version includes a KEDA-style plan file but does not install KEDA.

## Scaling Risk

Autoscaling can create more pods.

More pods can consume more CPU, memory, network, and database capacity.

## Build

Inspect:

```bash
sed -n '1,200p' k8s/aois-p/hpa.yaml
sed -n '1,220p' k8s/aois-p/keda-scaledobject.plan.yaml
```

Compile validator:

```bash
python3 -m py_compile examples/validate_autoscaling_plan.py
```

Run validator:

```bash
python3 examples/validate_autoscaling_plan.py
```

Expected:

```json
{
  "kubectl_apply_ran": false,
  "keda_installed": false,
  "max_replicas": 1,
  "status": "pass"
}
```

## Ops Lab

Answer:

1. Which file defines HPA?
2. Which workload does it target?
3. What is the max replica count?
4. Why is KEDA only a plan file here?
5. Which field proves no apply ran?

Answer key:

1. `hpa.yaml`
2. `aois-p-api`
3. `1`
4. installing KEDA changes cluster resources and needs approval
5. `kubectl_apply_ran=false`

## Break Lab

Do not skip this.

### Option A - Raise Max Replicas

In a scratch copy, set `maxReplicas: 5`.

Expected risk:

- portfolio workload could create more pods under load

### Option B - Install KEDA Without Approval

Think through the impact of installing KEDA.

Expected risk:

- CRDs/controllers are added to the cluster
- resource footprint changes
- primary AOIS may be affected

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. max replicas remains `1`
4. no autoscaler is installed
5. no manifest is applied
6. you can explain autoscaling risk

## Common Mistakes

- treating autoscaling as free capacity
- raising max replicas without memory budget
- installing KEDA without understanding CRDs/controllers
- scaling API pods without checking database/backing services
- forgetting primary AOIS priority

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_autoscaling_plan.py
```

Read `missing`, inspect the referenced manifest, and restore the missing control.

If live autoscaling is requested:

- stop
- confirm CPU/RAM budget
- confirm max replicas
- confirm dependency capacity
- get explicit approval
- record resource usage after apply

## Benchmark

Measure:

- validator compile result
- validator status
- max replicas
- whether KEDA was installed
- whether `kubectl apply` ran
- repo disk footprint
- memory snapshot

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can inspect, validate, break, explain, and defend autoscaling plans without scaling. |
| 4/5 | Plan validates, but one autoscaling concept needs review. |
| 3/5 | Files exist, but scaling risk is weak. |
| 2/5 | HPA exists, but resource impact is unclear. |
| 1/5 | Autoscaling still means "more pods automatically." |

Minimum pass: `4/5`.

## Architecture Defense

Why autoscaling after GitOps?

Because scale policy should be part of reviewed desired state.

Why cap max replicas at `1`?

Because this is the portfolio project on a constrained shared server.

Why not install KEDA?

Because KEDA adds cluster components and CRDs that need explicit approval.

## 4-Layer Tool Drill

Tool: HPA

1. Plain English
It changes pod replica count based on metrics.

2. System Role
It would let AOIS scale API capacity under load later.

3. Minimal Technical Definition
It is a Kubernetes autoscaling resource targeting a scalable workload and metric threshold.

4. Hands-on Proof
The validator confirms an HPA exists but max replicas is capped at `1` and no apply ran.

## 4-Level System Explanation Drill

1. Simple English
AOIS now has a safe autoscaling plan.

2. Practical Explanation
I can inspect HPA and KEDA-style plan files and explain why scaling is capped.

3. Technical Explanation
`v9` adds HPA and KEDA ScaledObject plan manifests with local validation and no cluster mutation.

4. Engineer-Level Explanation
AOIS now has autoscaling design separated from autoscaling execution, preserving primary-workload safety while teaching metrics, replica caps, and event-driven scaling concepts.

## Failure Story

Representative failure:

- Symptom: autoscaling creates extra pods and memory pressure returns
- Root cause: max replicas were raised without resource budget
- Fix: cap replicas and require approval before live scaling
- Prevention: validate autoscaling plan and record resource impact
- What this taught me: autoscaling is controlled resource multiplication

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v9` solve in AOIS?
2. What is HPA?
3. What is min replicas?
4. What is max replicas?
5. Why is max replicas `1` here?
6. What is KEDA?
7. Why is KEDA not installed?
8. Why can autoscaling be dangerous on a shared server?
9. Why should scaling policy be reviewed in GitOps?
10. Explain HPA using the 4-layer tool rule.
11. Explain `v9` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v9` solve in AOIS?

It teaches autoscaling and event-driven scaling design without creating extra workloads.

2. What is HPA?

A Kubernetes resource that adjusts replicas based on metrics.

3. What is min replicas?

The minimum number of replicas allowed.

4. What is max replicas?

The maximum number of replicas allowed.

5. Why is max replicas `1` here?

To prevent the portfolio workload from actually scaling on the shared server.

6. What is KEDA?

A Kubernetes event-driven autoscaling system.

7. Why is KEDA not installed?

It adds cluster components and requires explicit approval.

8. Why can autoscaling be dangerous on a shared server?

It can create more pods and consume more CPU, memory, network, and dependency capacity.

9. Why should scaling policy be reviewed in GitOps?

Because scaling changes resource behavior and should be auditable.

10. Explain HPA using the 4-layer tool rule.

- Plain English: it scales pod count from metrics.
- System Role: it controls AOIS API capacity later.
- Minimal Technical Definition: it is a Kubernetes autoscaling object targeting a workload.
- Hands-on Proof: the validator confirms HPA exists but max replicas stays capped and no apply ran.

11. Explain `v9` using the 4-level system explanation rule.

- Simple English: AOIS has a safe scaling plan.
- Practical explanation: I can inspect HPA/KEDA plans and explain the replica cap.
- Technical explanation: `v9` adds autoscaling manifests and a local validator.
- Engineer-level explanation: AOIS now models autoscaling policy without resource multiplication, preserving shared-server safety while preparing for event-driven infrastructure.

## Connection Forward

`v9` completes Phase 3:

`Kubernetes plan -> workload identity -> Helm -> GitOps -> autoscaling plan`

Phase 4 can move into enterprise cloud equivalents only if these resource and review boundaries remain intact.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v9 Introduction](02-introduction.md)
- Next: [v9 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
