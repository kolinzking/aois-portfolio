# v15.5 Lab

Authoring status: authored

## Build Lab

Run:

```bash
python3 -m py_compile examples/validate_quantization_plan.py examples/simulate_quantization_tradeoffs.py
python3 examples/validate_quantization_plan.py
python3 examples/simulate_quantization_tradeoffs.py
```

## Ops Lab

Answer:

1. Which option has the lowest memory?
2. Which option has the highest quality score?
3. Which option has the highest speed index?
4. Which field proves no quantization job started?

Answer key:

1. `int4-placeholder`
2. `fp16-baseline`
3. `int4-placeholder`
4. `quantization_job_started=false`

## Break Lab

Use a scratch copy only.

Break 1: set `approved_for_live_quantization` to `true`.

Expected result: validation fails because live quantization is not approved.

Break 2: remove `task_regression_eval_required`.

Expected result: validation fails because precision changes need task eval.

Break 3: set `max_model_artifact_mb` to `1`.

Expected result: validation fails because no artifact creation is approved.

## Explanation Lab

Explain:

1. Why memory reduction can cost quality.
2. Why calibration data matters.
3. Why fallback precision is required.
4. Why quantization must be benchmarked on AOIS tasks.
5. Why this lesson does not download model artifacts.

## Defense Lab

Defend this decision:

AOIS should not quantize or serve a lower-precision artifact until model approval, method review, calibration review, quality eval, task regression eval, memory benchmark, latency benchmark, fallback precision, rollback, and primary AOIS separation exist.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v15.5 - Quantization And Memory Economics Without Runtime](03-notes.md)
- Next: [v15.5 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
