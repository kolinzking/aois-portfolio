# v14 Lab

Authoring status: authored

## Build Lab

Run:

```bash
python3 -m py_compile examples/validate_high_throughput_serving_plan.py examples/simulate_high_throughput_serving.py
python3 examples/validate_high_throughput_serving_plan.py
python3 examples/simulate_high_throughput_serving.py
```

## Ops Lab

Answer from the simulator:

1. Which mode is the baseline?
2. Which mode has the highest simulated throughput?
3. Which mode has the lowest simulated p95 latency?
4. Which metric shows gain versus serial serving?

Answer key:

1. `serial-baseline`
2. `cache-aware-placeholder`
3. `serial-baseline`
4. `throughput_gain_vs_serial`

## Break Lab

Use a scratch copy only.

Break 1: set `approved_for_live_serving` to `true`.

Expected result: validation fails because live serving is not approved.

Break 2: set `max_queue_depth_for_lesson` to `10`.

Expected result: validation fails because live queueing is not approved.

Break 3: remove `concurrency_limit_required`.

Expected result: validation fails because serving needs bounded concurrency.

## Explanation Lab

Explain:

1. Why batching changes both throughput and latency.
2. Why p95 latency is more useful than average latency for overload.
3. Why queues need timeout and load shedding.
4. Why cache policy belongs in performance engineering.
5. Why speculative decoding requires review.

## Defense Lab

Defend this decision:

AOIS should not run high-throughput serving until capacity, model download, runtime selection, batching policy, concurrency limits, latency SLO, throughput SLO, cache policy, fallback route, rollback, and primary AOIS separation are approved.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v14 - High-Throughput Inference Serving Without Runtime](03-notes.md)
- Next: [v14 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
