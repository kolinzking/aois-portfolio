# v13 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v13` inference plan to a safe no-runtime state.

Safe state means:

- no GPU runtime started
- no GPU required for the lesson
- no model downloaded
- no network required
- no live GPU approval
- no container image built
- `aois-p` namespace remains active

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_gpu_inference_plan.py examples/simulate_gpu_inference_profile.py
python3 examples/validate_gpu_inference_plan.py
python3 examples/simulate_gpu_inference_profile.py
```

Required result:

- validator `status=pass`
- simulator `status=pass`
- `gpu_runtime_started=false`
- `model_downloaded=false`
- namespace is `aois-p`

## Recovery Steps

If validation fails:

1. Read the `missing` list.
2. Restore namespace to `aois-p`.
3. Restore `gpu_runtime_started` to `false`.
4. Restore `gpu_required_for_this_lesson` to `false`.
5. Restore `model_downloaded` to `false`.
6. Restore `approved_for_live_gpu` to `false`.
7. Restore request and response contract fields.
8. Restore serving options.
9. Restore GPU count and memory to zero.
10. Restore all controls and required live checks.

If live GPU work is requested:

1. Stop.
2. Confirm hardware or cloud GPU approval.
3. Define driver/CUDA plan.
4. Define container image plan.
5. Review model license and size.
6. Approve model download.
7. Define memory and cost budgets.
8. Define fallback route and rollback.
9. Define observability.
10. Verify primary AOIS separation.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v13 Lab](04-lab.md)
- Next: [v13 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
