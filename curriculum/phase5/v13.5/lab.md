# v13.5 Lab

Authoring status: authored

## Build Lab

Goal: validate GPU infrastructure operations without applying resources.

Run:

```bash
python3 -m py_compile examples/validate_gpu_infrastructure_plan.py
python3 examples/validate_gpu_infrastructure_plan.py
```

## Ops Lab

Answer from the validator and plan:

1. Which field proves no apply happened?
2. Which two fields prove no GPU operator or device plugin was installed?
3. Which field names the GPU resource?
4. Which field keeps the lesson from requesting GPUs?
5. Which fields prove GPU observability is required?

Answer key:

1. `kubectl_apply_ran=false`
2. `gpu_operator_installed=false` and `device_plugin_installed=false`
3. `gpu_resource_name=nvidia.com/gpu`
4. `requested_gpus_for_lesson=0`
5. GPU utilization, memory, temperature, power, pod-to-GPU mapping, scheduling events, dashboard, and alerts

## Break Lab

Use a scratch copy only.

Break 1: set `device_plugin_installed` to `true`.

Expected result: validation fails because this lesson must not claim live installation.

Break 2: set `requested_gpus_for_lesson` to `1`.

Expected result: validation fails because no GPU scheduling is approved.

Break 3: remove `scheduling_events_required`.

Expected result: validation fails because scheduling failures must be observable.

## Explanation Lab

Explain:

1. Why a GPU service can fail before its app code starts.
2. Why the scheduler needs GPU resource advertisement.
3. Why taints and tolerations protect GPU nodes.
4. Why pod-to-GPU mapping matters.
5. Why MIG needs a strategy before live use.

## Defense Lab

Defend this decision:

AOIS should not apply GPU operator or device plugin resources until driver/CUDA planning, docs review, node pool budget, scheduling policy, MIG strategy, observability, rollback, and primary AOIS separation are complete.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v13.5 - GPU Infrastructure Operations Without Applying Resources](notes.md)
- Next: [v13.5 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
