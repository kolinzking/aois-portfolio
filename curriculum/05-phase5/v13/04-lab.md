# v13 Lab

Authoring status: authored

## Build Lab

Goal: inspect and validate a GPU inference service plan without GPU runtime.

Run:

```bash
python3 -m py_compile examples/validate_gpu_inference_plan.py examples/simulate_gpu_inference_profile.py
python3 examples/validate_gpu_inference_plan.py
python3 examples/simulate_gpu_inference_profile.py
```

## Ops Lab

Answer from the outputs:

1. Which mode proves validation is no-runtime?
2. Which simulator field shows the fake backend?
3. Which response fields support performance tracking?
4. Which live checks block model download and GPU runtime?

Answer key:

1. `gpu_inference_plan_validation_no_runtime`
2. `backend_metadata.backend=no-runtime-simulation`
3. `latency_ms`, `tokens_in`, and `tokens_out`
4. `model_download_approval`, `gpu_hardware_or_cloud_approval`, `driver_and_cuda_plan`, and `container_image_plan`

## Break Lab

Use a scratch copy only.

Break 1: remove `trace_id` from the request contract.

Expected result: validation fails because inference must remain traceable.

Break 2: set `gpu_count` to `1`.

Expected result: validation fails because this lesson has no approved GPU capacity.

Break 3: remove `model_license_review_required`.

Expected result: validation fails because model licensing must be reviewed before serving.

## Explanation Lab

Explain:

1. Why a GPU inference service needs a contract.
2. Why model download is an operational event.
3. Why latency and throughput are separate measurements.
4. Why token accounting matters.
5. Why fallback routing is required.

## Defense Lab

Defend this decision:

AOIS should not run GPU inference until hardware/cloud approval, driver plan, image plan, model license review, model download approval, memory budget, cost budget, observability, fallback route, rollback, and primary AOIS separation exist.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v13 - GPU-Backed Inference Services Without GPU Runtime](03-notes.md)
- Next: [v13 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
