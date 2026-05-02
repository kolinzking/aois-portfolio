# v13.5 - GPU Infrastructure Operations Without Applying Resources

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: GPU infrastructure plan and validation only, no operator install, no device plugin install, no `kubectl apply`, no GPU runtime

## What This Builds

This version builds a GPU infrastructure operations plan:

- `inference/aois-p/gpu-infrastructure-operations.plan.json`
- `examples/validate_gpu_infrastructure_plan.py`

It teaches:

- GPU operator awareness
- device plugin awareness
- GPU scheduling controls
- resource requests and limits
- node selectors, taints, and tolerations
- MIG awareness
- GPU observability signals
- why GPU infrastructure is its own discipline

## Why This Exists

`v13` defined the GPU inference service contract.

But a GPU service cannot run safely unless the infrastructure knows how to expose, schedule, isolate, observe, and recover GPU workloads.

GPU infrastructure has failure modes that ordinary CPU services do not:

- missing driver/runtime support
- no device plugin
- GPU resource not advertised
- wrong node selection
- noisy neighbor behavior
- memory exhaustion
- thermal or power issues
- invisible pod-to-GPU mapping

## AOIS Connection

The AOIS path is now:

`GPU inference contract -> GPU infrastructure operations -> high-throughput serving`

`v13.5` teaches the operational layer below inference serving without changing the server or cluster.

## Learning Goals

By the end of this version you should be able to:

- explain the role of a GPU operator
- explain the role of a device plugin
- explain GPU scheduling constraints
- explain why requests and limits matter for GPU workloads
- explain MIG awareness at a high level
- explain GPU observability requirements
- validate the GPU infrastructure plan locally without applying resources

## Prerequisites

You should have completed:

- `v6` Kubernetes manifest planning
- `v6.5` workload identity/RBAC planning
- `v13` GPU inference service planning

Required checks:

```bash
python3 -m py_compile examples/validate_gpu_infrastructure_plan.py
python3 examples/validate_gpu_infrastructure_plan.py
```

## Core Concepts

## GPU Operator

A GPU operator is an operational pattern for managing GPU software components on cluster nodes.

In this lesson, it is a placeholder only. Nothing is installed.

## Device Plugin

A device plugin exposes GPU resources to Kubernetes scheduling.

Without a device plugin, the scheduler cannot reliably assign GPU resources to pods.

## GPU Resource Name

The common Kubernetes GPU resource shape is represented as:

```text
nvidia.com/gpu
```

The lesson validates this as a plan field only.

## Node Selector

A node selector helps send GPU workloads to GPU-capable nodes.

## Taints And Tolerations

Taints keep ordinary workloads off special nodes.

Tolerations allow approved workloads onto those nodes.

## Resource Limits

GPU workloads must request and limit special resources deliberately.

For this lesson, requested GPUs remain zero.

## MIG Awareness

MIG awareness means knowing that a physical GPU may be partitioned into smaller profiles on supported hardware.

This lesson does not configure MIG. It only requires a future strategy review.

## GPU Observability

GPU observability must include:

- utilization
- memory
- temperature
- power
- pod-to-GPU mapping
- scheduling events
- dashboards
- alerts

## Build

Inspect:

```bash
sed -n '1,260p' inference/aois-p/gpu-infrastructure-operations.plan.json
sed -n '1,280p' examples/validate_gpu_infrastructure_plan.py
```

Compile:

```bash
python3 -m py_compile examples/validate_gpu_infrastructure_plan.py
```

Run:

```bash
python3 examples/validate_gpu_infrastructure_plan.py
```

Expected:

```json
{
  "kubectl_apply_ran": false,
  "gpu_operator_installed": false,
  "device_plugin_installed": false,
  "gpu_runtime_started": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

Do not install a GPU operator, device plugin, driver, CUDA stack, or GPU monitoring service. Do not run `kubectl apply`.

## Ops Lab

Answer from the plan:

1. Which field proves no `kubectl apply` ran?
2. Which field proves no GPU operator was installed?
3. Which field proves no device plugin was installed?
4. Which resource name represents GPU scheduling?
5. Which field keeps requested GPUs at zero?
6. Which controls protect GPU node placement?
7. Which observability fields are required?
8. Which live check protects primary AOIS separation?

Answer key:

1. `kubectl_apply_ran=false`
2. `gpu_operator_installed=false`
3. `device_plugin_installed=false`
4. `nvidia.com/gpu`
5. `requested_gpus_for_lesson=0`
6. node selector, taint/toleration, resource limits, and priority class review
7. utilization, memory, temperature, power, pod-to-GPU mapping, scheduling events, dashboard, and alerts
8. `primary_aois_separation_review`

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Pretend Operator Is Installed

Set:

```json
"gpu_operator_installed": true
```

Expected risk:

- the plan misrepresents the server state and may lead to unsafe assumptions

### Option B - Request A GPU

Set:

```json
"requested_gpus_for_lesson": 1
```

Expected risk:

- a plan-only lesson can be mistaken for live GPU scheduling

### Option C - Remove Pod-To-GPU Mapping

Set:

```json
"pod_to_gpu_mapping_required": false
```

Expected risk:

- operators cannot see which workload is consuming GPU capacity

### Option D - Remove MIG Strategy Review

Set:

```json
"mig_strategy_review_required": false
```

Expected risk:

- GPU partitioning may be configured or ignored without workload-level reasoning

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. no `kubectl apply` is recorded
4. no GPU operator is installed
5. no device plugin is installed
6. no GPU runtime started
7. requested GPUs remain zero
8. scheduling controls remain true
9. observability controls remain true
10. primary AOIS separation remains required

## Common Mistakes

- thinking a GPU workload can be scheduled without resource advertisement
- ignoring taints and tolerations
- tracking GPU utilization but not pod-to-GPU mapping
- treating MIG as a switch instead of a capacity strategy
- applying GPU operator manifests before docs, budget, and rollback review
- confusing portfolio GPU infrastructure with primary AOIS

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_gpu_infrastructure_plan.py
```

Read `missing`, inspect the plan, and restore required fields.

Common fixes:

- restore namespace to `aois-p`
- restore `kubectl_apply_ran` to `false`
- restore operator and device plugin install flags to `false`
- restore GPU runtime to `false`
- restore requested GPUs to `0`
- restore scheduling controls
- restore MIG review controls
- restore observability controls
- restore required live checks

## Benchmark

Measure:

- validator compile result
- validator status
- no-apply status
- operator install status
- device plugin install status
- requested GPU count
- observability control count
- repo disk footprint
- memory snapshot

## Architecture Defense

Why plan GPU infrastructure before installing operators?

Because GPU operators and plugins change node behavior. AOIS must understand driver/runtime, scheduling, observability, cost, and rollback before applying anything.

Why require pod-to-GPU mapping?

Because high utilization is not enough; operators must know which workload owns the pressure.

Why keep requested GPUs at zero?

Because this server-side curriculum path is not approved to schedule GPU workloads.

## 4-Layer Tool Drill

Tool: device plugin

1. Plain English
It tells the scheduler that GPU resources exist.

2. System Role
It lets GPU workloads request and receive GPU capacity.

3. Minimal Technical Definition
It is a node-level integration that advertises special hardware resources to the orchestrator.

4. Hands-on Proof
The validator confirms device plugin installation is false while the plan still documents scheduling controls.

## 4-Level System Explanation Drill

1. Simple English
AOIS plans GPU scheduling without installing GPU infrastructure.

2. Practical Explanation
I can explain operator, device plugin, node selection, taints, tolerations, resource limits, MIG review, and GPU metrics.

3. Technical Explanation
`v13.5` adds a GPU infrastructure operations plan and no-apply validator.

4. Engineer-Level Explanation
AOIS now separates GPU infrastructure design from cluster mutation, requiring driver/CUDA planning, device-plugin strategy, scheduling policy, MIG strategy, GPU observability, cost gates, rollback, and primary-project separation before any GPU infrastructure is applied.

## Failure Story

Representative failure:

- Symptom: a GPU pod stays pending and nobody can tell whether the node lacks GPU resources or the scheduler cannot see them
- Root cause: device plugin and scheduling controls were assumed instead of verified
- Fix: inspect GPU resource advertisement, node labels, taints, tolerations, and resource requests
- Prevention: validate the GPU infrastructure plan before applying any operator or workload manifests
- What this taught me: GPU operations fail at the scheduling layer before inference code runs

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v13.5` solve in AOIS?
2. What is a GPU operator?
3. What is a device plugin?
4. Why does the scheduler need a GPU resource name?
5. Why are node selectors useful?
6. Why do taints and tolerations matter?
7. Why does requested GPU count remain zero?
8. What is MIG awareness?
9. What GPU observability signals are required?
10. Explain device plugin using the 4-layer tool rule.
11. Explain `v13.5` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v13.5` solve in AOIS?

It defines GPU infrastructure operations controls before installing GPU operators, plugins, or workloads.

2. What is a GPU operator?

An operational pattern for managing GPU software components on cluster nodes.

3. What is a device plugin?

A node-level integration that advertises GPU resources to the scheduler.

4. Why does the scheduler need a GPU resource name?

So workloads can request GPU capacity explicitly.

5. Why are node selectors useful?

They direct GPU workloads to GPU-capable nodes.

6. Why do taints and tolerations matter?

They keep ordinary workloads off GPU nodes while allowing approved GPU workloads.

7. Why does requested GPU count remain zero?

No live GPU workload scheduling is approved in this lesson.

8. What is MIG awareness?

Awareness that supported GPUs can be partitioned into profiles and need a strategy before live use.

9. What GPU observability signals are required?

Utilization, memory, temperature, power, pod-to-GPU mapping, scheduling events, dashboards, and alerts.

10. Explain device plugin using the 4-layer tool rule.

- Plain English: it tells the scheduler that GPUs exist.
- System Role: it allows GPU workloads to request GPU resources.
- Minimal Technical Definition: it advertises special hardware resources to the orchestrator.
- Hands-on Proof: the validator confirms no plugin is installed while the plan documents required controls.

11. Explain `v13.5` using the 4-level system explanation rule.

- Simple English: AOIS plans GPU scheduling without installing GPU infrastructure.
- Practical explanation: I can explain operator, plugin, scheduling, MIG, and observability requirements.
- Technical explanation: `v13.5` adds a GPU infrastructure plan and no-apply validator.
- Engineer-level explanation: AOIS gates GPU infrastructure mutation behind driver/CUDA planning, device-plugin strategy, scheduling policy, MIG review, GPU observability, cost controls, rollback, and primary-project separation.

## Connection Forward

`v13.5` defines the GPU infrastructure layer.

`v14` moves to high-throughput inference serving, where AOIS starts reasoning about throughput, concurrency, and serving efficiency.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v13.5 Introduction](introduction.md)
- Next: [v13.5 Lab](lab.md)
<!-- AOIS-NAV-END -->
