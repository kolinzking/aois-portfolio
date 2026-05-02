# v14 - High-Throughput Inference Serving Without Runtime

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: serving plan and local simulation only, no inference runtime, no GPU runtime, no model download, no container build

## What This Builds

This version builds a high-throughput serving plan:

- `inference/aois-p/high-throughput-serving.plan.json`
- `examples/validate_high_throughput_serving_plan.py`
- `examples/simulate_high_throughput_serving.py`

It teaches:

- serial serving baseline
- continuous batching awareness
- concurrency limits
- queue and backpressure policy
- cache-aware serving path
- latency versus throughput tradeoff
- speculative decoding review gate
- why high throughput is not automatically better

## Why This Exists

GPU inference is expensive.

The next frontier is not only "run a model." It is "serve more useful tokens with controlled latency, predictable cost, and safe overload behavior."

High-throughput serving introduces tradeoffs:

- batching can increase throughput but raise tail latency
- concurrency can improve utilization but overload memory
- queues can smooth bursts but hide delay
- cache reuse can reduce work but needs correctness boundaries
- speculative decoding may improve speed but needs model/runtime review

## AOIS Connection

The AOIS path is now:

`GPU inference contract -> GPU infrastructure operations -> high-throughput serving`

`v14` teaches AOIS to compare serving modes before running any serving runtime.

## Learning Goals

By the end of this version you should be able to:

- explain serial serving versus batched serving
- explain concurrency limits
- explain queue depth, timeout, backpressure, and load shedding
- explain why p95 latency matters
- explain throughput in tokens per second
- explain cache-aware serving at a high level
- explain why speculative decoding is review-gated
- run a local throughput-mode simulation

## Prerequisites

You should have completed:

- `v13` GPU inference service planning
- `v13.5` GPU infrastructure operations planning

Required checks:

```bash
python3 -m py_compile examples/validate_high_throughput_serving_plan.py examples/simulate_high_throughput_serving.py
python3 examples/validate_high_throughput_serving_plan.py
python3 examples/simulate_high_throughput_serving.py
```

## Core Concepts

## Serial Baseline

Serial serving processes one request at a time.

It is simple and predictable but may underuse available compute.

## Continuous Batching

Continuous batching groups work so the serving runtime can process tokens more efficiently.

It can improve throughput, but it must be measured against tail latency.

## Concurrency Limit

Concurrency limit controls how many requests can be active at once.

Too low wastes capacity. Too high creates contention, memory pressure, and timeouts.

## Queue Policy

Queue policy controls waiting work.

AOIS needs queue depth, timeout, backpressure, and load shedding.

In this lesson, live queue depth remains zero.

## Cache-Aware Serving

Cache-aware serving reuses prior computation or prompt structure when safe.

`v14` only introduces the concept. `v14.5` goes deeper into caching.

## Speculative Decoding Awareness

Speculative decoding can improve generation speed by using a draft/target model pattern.

In this lesson, it is review-gated only. No runtime is configured.

## Build

Inspect:

```bash
sed -n '1,260p' inference/aois-p/high-throughput-serving.plan.json
sed -n '1,280p' examples/validate_high_throughput_serving_plan.py
sed -n '1,220p' examples/simulate_high_throughput_serving.py
```

Compile:

```bash
python3 -m py_compile examples/validate_high_throughput_serving_plan.py examples/simulate_high_throughput_serving.py
```

Validate:

```bash
python3 examples/validate_high_throughput_serving_plan.py
```

Simulate:

```bash
python3 examples/simulate_high_throughput_serving.py
```

Expected validation:

```json
{
  "inference_runtime_started": false,
  "gpu_runtime_started": false,
  "model_downloaded": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer from the plan and simulator:

1. Which mode is the serial baseline?
2. Which mode has the highest simulated tokens per second?
3. Which field shows p95 latency?
4. Which field prevents live queueing in this lesson?
5. Which controls enforce overload behavior?
6. Which review gate covers speculative decoding?

Answer key:

1. `serial-baseline`
2. `cache-aware-placeholder`
3. `simulated_p95_latency_ms`
4. `max_queue_depth_for_lesson=0`
5. backpressure and load shedding
6. `speculative_decoding_review_required`

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Approve Live Serving

Set:

```json
"approved_for_live_serving": true
```

Expected risk:

- a simulation-only lesson can be mistaken for permission to run model serving

### Option B - Remove Backpressure

Set:

```json
"backpressure_required": false
```

Expected risk:

- overload becomes hidden queue growth or timeout storms

### Option C - Remove Latency Budget

Set:

```json
"latency_budget_required": false
```

Expected risk:

- throughput optimization can harm users without a tail-latency guardrail

### Option D - Remove Fallback Route

Set:

```json
"fallback_route_required": false
```

Expected risk:

- overload or runtime failure has no safe degradation path

## Testing

The version passes when:

1. both scripts compile
2. validator returns `status=pass`
3. simulator returns `status=pass`
4. inference runtime remains false
5. GPU runtime remains false
6. model download remains false
7. serving modes remain present
8. queue depth remains zero
9. latency, throughput, batching, concurrency, cache, fallback, and observability controls remain true

## Common Mistakes

- optimizing throughput without p95 latency
- increasing concurrency without memory budget
- letting queue depth hide overload
- treating cache reuse as always safe
- treating speculative decoding as a toggle instead of a serving design decision
- ignoring fallback route
- confusing simulation gains with production benchmarks

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_high_throughput_serving_plan.py
```

Read `missing`, inspect the plan, and restore required fields.

Common fixes:

- restore namespace to `aois-p`
- restore runtime flags to `false`
- restore serving modes
- restore queue depth to zero
- restore backpressure and load shedding
- restore performance controls
- restore required live checks

## Benchmark

Measure:

- validator compile result
- validator status
- simulator status
- simulated tokens per second by mode
- simulated p95 latency by mode
- throughput gain versus serial baseline
- runtime status
- model download status
- repo disk footprint
- memory snapshot

## Architecture Defense

Why simulate serving modes?

Because throughput engineering can be learned safely before a real model server exists.

Why is higher throughput not automatically better?

Because users experience latency, timeouts, quality, and fallback behavior, not raw tokens per second alone.

Why require queue and backpressure policy?

Because overload must be controlled instead of hidden.

## 4-Layer Tool Drill

Tool: continuous batching

1. Plain English
It groups inference work so the server uses compute more efficiently.

2. System Role
It improves throughput for model serving.

3. Minimal Technical Definition
It is a serving scheduler technique that combines active generation work across requests to improve hardware utilization.

4. Hands-on Proof
The simulator compares serial, batching, and cache-aware modes without starting a runtime.

## 4-Level System Explanation Drill

1. Simple English
AOIS compares serving throughput modes without running a model server.

2. Practical Explanation
I can compare tokens per second, p95 latency, batching, concurrency, queueing, cache awareness, and fallback controls.

3. Technical Explanation
`v14` adds a high-throughput serving plan, validator, and deterministic mode simulator.

4. Engineer-Level Explanation
AOIS now separates throughput design from runtime execution, requiring latency SLOs, throughput SLOs, token budgets, batching policy, concurrency limits, cache policy, speculative decoding review, backpressure, load shedding, fallback, observability, rollback, and primary-project separation before live serving.

## Failure Story

Representative failure:

- Symptom: throughput improves in a benchmark, but users see timeout spikes
- Root cause: batching and concurrency were increased without p95 latency, queue timeout, and backpressure controls
- Fix: restore concurrency limits, enforce queue timeout, add load shedding, and compare p95 latency
- Prevention: validate the `v14` serving plan before live runtime tuning
- What this taught me: throughput without tail-latency control is not reliability

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v14` solve in AOIS?
2. What is a serial serving baseline?
3. What is continuous batching?
4. Why does concurrency need a limit?
5. Why does queue depth need a policy?
6. What is backpressure?
7. Why does p95 latency matter?
8. Why is cache-aware serving not automatically safe?
9. Why is speculative decoding review-gated?
10. Explain continuous batching using the 4-layer tool rule.
11. Explain `v14` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v14` solve in AOIS?

It teaches AOIS to compare high-throughput serving modes before running a model server.

2. What is a serial serving baseline?

A simple mode that processes one request at a time.

3. What is continuous batching?

A serving technique that groups active inference work to improve utilization.

4. Why does concurrency need a limit?

Unlimited concurrency can cause memory pressure, contention, and timeout storms.

5. Why does queue depth need a policy?

Queues hide overload unless timeout, backpressure, and load-shedding rules exist.

6. What is backpressure?

A mechanism that slows or rejects incoming work when the system is overloaded.

7. Why does p95 latency matter?

It shows tail latency that average latency can hide.

8. Why is cache-aware serving not automatically safe?

Cache reuse must preserve correctness, data boundaries, and freshness.

9. Why is speculative decoding review-gated?

It changes serving behavior and model/runtime assumptions, so it needs design review before live use.

10. Explain continuous batching using the 4-layer tool rule.

- Plain English: it groups inference work to use compute better.
- System Role: it improves serving throughput.
- Minimal Technical Definition: it combines generation work across active requests to improve utilization.
- Hands-on Proof: the simulator compares batching against serial serving.

11. Explain `v14` using the 4-level system explanation rule.

- Simple English: AOIS compares fast serving modes without running a model server.
- Practical explanation: I can inspect throughput, latency, queueing, batching, cache, and fallback controls.
- Technical explanation: `v14` adds a serving plan, validator, and deterministic simulator.
- Engineer-level explanation: AOIS gates live high-throughput serving behind latency and throughput SLOs, token budgets, batching policy, concurrency limits, cache policy, speculative decoding review, backpressure, load shedding, fallback, observability, rollback, and primary-project separation.

## Connection Forward

`v14` introduces high-throughput serving tradeoffs.

`v14.5` goes deeper into performance engineering and caching, including prefix reuse, cache correctness, and latency/throughput tradeoffs.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v14 Introduction](introduction.md)
- Next: [v14 Lab](lab.md)
<!-- AOIS-NAV-END -->
