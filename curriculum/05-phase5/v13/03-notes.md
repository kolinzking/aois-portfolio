# v13 - GPU-Backed Inference Services Without GPU Runtime

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: inference plan, validator, and local profile simulation only; no GPU runtime, no model download, no container build, no provider calls

## What This Builds

This version builds the first Phase 5 inference engineering artifact set:

- `inference/aois-p/gpu-inference-service.plan.json`
- `examples/validate_gpu_inference_plan.py`
- `examples/simulate_gpu_inference_profile.py`

It teaches:

- GPU-backed inference service shape
- request and response contracts
- latency and throughput budgets
- serving backend choices
- model download and license gates
- memory and cost gates
- fallback route planning
- why API-only AI is different from inference operations

## Why This Exists

AOIS has used local deterministic logic and provider-planning so far.

Frontier AI infrastructure also requires understanding how models are served when you own the inference path.

GPU-backed inference adds new operational concerns:

- GPU memory
- drivers and CUDA
- container images
- model weights
- tokenizer/model compatibility
- latency and throughput
- batch/concurrency behavior
- license and cost constraints

This version introduces those concerns without using a GPU or downloading a model.

## AOIS Connection

The AOIS path is now:

`managed cloud planning -> owned inference path -> GPU service contract -> throughput engineering`

Phase 4 taught how to gate managed cloud usage.
Phase 5 begins the shift from model consumer to inference operator.

`v13` does not make AOIS a GPU platform yet. It defines the contract and readiness checks required before a GPU-backed inference service can exist.

## Learning Goals

By the end of this version you should be able to:

- explain GPU-backed inference
- explain the difference between API consumption and inference operation
- explain the role of NIM-style packaged inference services
- compare NIM-style, Triton-style, and vLLM-style serving paths at a high level
- explain why model download and license review are gated
- explain latency, throughput, and token accounting
- run a local inference profile simulation
- validate that no GPU runtime was started

## Prerequisites

You should have completed:

- Phase 1 structured AI endpoint contract
- Phase 3 container/Kubernetes planning
- Phase 4 cloud/runtime governance

Required checks:

```bash
python3 -m py_compile examples/validate_gpu_inference_plan.py examples/simulate_gpu_inference_profile.py
python3 examples/validate_gpu_inference_plan.py
python3 examples/simulate_gpu_inference_profile.py
```

## Core Concepts

## GPU-Backed Inference

GPU-backed inference means model execution is served by infrastructure that uses GPUs for acceleration.

This can improve throughput and latency for large models, but it introduces hardware, driver, memory, and cost constraints.

## Inference Service

An inference service accepts a request contract and returns a response contract.

For AOIS, the contract includes:

- trace ID
- model route
- prompt
- output
- latency
- token counts
- backend metadata

## NIM-Style Serving

NIM-style serving means using a packaged inference microservice shape for GPU-backed model serving.

In `v13`, it is only a placeholder option. No NVIDIA software is installed or called.

## Triton-Style Serving

Triton-style serving means a multi-model inference server pattern.

In `v13`, it is only a conceptual serving path.

## vLLM-Style Serving

vLLM-style serving means high-throughput LLM serving with attention to batching and token throughput.

Later versions go deeper into throughput engineering.

## Latency

Latency is how long a request takes.

The plan tracks target p50 and p95 latency.

## Throughput

Throughput is how much work the service completes over time.

The plan tracks target tokens per second.

## Model Gate

Model weights are not free operationally.

Before downloading or serving a model, AOIS needs:

- license review
- model size review
- memory budget
- cost budget
- fallback route
- observability
- rollback

## Build

Inspect:

```bash
sed -n '1,260p' inference/aois-p/gpu-inference-service.plan.json
sed -n '1,280p' examples/validate_gpu_inference_plan.py
sed -n '1,220p' examples/simulate_gpu_inference_profile.py
```

Compile:

```bash
python3 -m py_compile examples/validate_gpu_inference_plan.py examples/simulate_gpu_inference_profile.py
```

Validate:

```bash
python3 examples/validate_gpu_inference_plan.py
```

Simulate a local inference profile:

```bash
python3 examples/simulate_gpu_inference_profile.py
```

Expected validation:

```json
{
  "gpu_runtime_started": false,
  "gpu_required_for_this_lesson": false,
  "model_downloaded": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer from the plan and simulator:

1. What file defines the GPU inference service plan?
2. Which field proves no GPU runtime started?
3. Which field proves no model was downloaded?
4. Which request field connects inference to distributed tracing?
5. Which response fields support performance analysis?
6. Which serving options are considered?
7. Which field prevents live concurrency in this lesson?
8. Which required check protects primary AOIS separation?

Answer key:

1. `inference/aois-p/gpu-inference-service.plan.json`
2. `gpu_runtime_started=false`
3. `model_downloaded=false`
4. `trace_id`
5. `latency_ms`, `tokens_in`, `tokens_out`, and `backend_metadata`
6. `nvidia-nim-placeholder`, `triton-style-placeholder`, and `vllm-placeholder`
7. `max_concurrent_requests_for_lesson=0`
8. `primary_aois_separation_review`

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Approve Live GPU Too Early

Set:

```json
"approved_for_live_gpu": true
```

Expected risk:

- plan-only learning can be mistaken for permission to run GPU infrastructure

### Option B - Download Model Too Early

Set:

```json
"model_downloaded": true
```

Expected risk:

- large artifacts may consume disk, violate license requirements, or create unclear provenance

### Option C - Remove Token Accounting

Remove `tokens_in` and `tokens_out` from the response contract.

Expected risk:

- AOIS cannot reason about cost, throughput, or model load

### Option D - Remove Fallback Route

Set:

```json
"fallback_route_required": false
```

Expected risk:

- inference failure has no controlled fallback path

## Testing

The version passes when:

1. both scripts compile
2. validator returns `status=pass`
3. simulator returns `status=pass`
4. GPU runtime remains false
5. model download remains false
6. live GPU approval remains false
7. serving options remain present
8. latency and throughput fields exist
9. primary AOIS separation remains required

## Common Mistakes

- treating GPU inference as only a faster API call
- ignoring model license and size
- downloading model weights before storage planning
- ignoring token accounting
- measuring latency but not throughput
- forgetting fallback routing
- confusing this portfolio inference path with primary AOIS resources

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_gpu_inference_plan.py
```

Read `missing`, inspect the plan, and restore required fields.

Common fixes:

- restore namespace to `aois-p`
- restore `gpu_runtime_started` to `false`
- restore `model_downloaded` to `false`
- restore live GPU approval to `false`
- restore request and response contract fields
- restore serving options
- restore GPU count and memory to zero
- restore required controls and live checks

If live GPU work is requested:

- stop
- identify real hardware or cloud GPU budget
- define driver and CUDA plan
- define container image plan
- review model license and size
- approve model download
- define memory and cost budgets
- define fallback route
- define observability and rollback
- verify primary AOIS separation
- get explicit approval before installing, downloading, building, or running anything

## Benchmark

Measure:

- validator compile result
- validator status
- simulator status
- simulated latency
- simulated tokens in
- simulated tokens out
- GPU runtime status
- model download status
- repo disk footprint
- memory snapshot

## Architecture Defense

Why start with a plan and simulator?

Because GPU inference is expensive and stateful. A local plan teaches contracts and controls before model weights, drivers, images, or GPU processes exist.

Why track tokens?

Because token counts drive latency, throughput, cost, and capacity planning.

Why require fallback route?

Because GPU inference can fail due to capacity, memory, model load, or runtime issues. AOIS needs a safe degradation path.

Why keep `aois-p`?

Because the portfolio inference path must stay distinct from primary AOIS.

## 4-Layer Tool Drill

Tool: GPU inference service

1. Plain English
It runs model requests on GPU-backed infrastructure.

2. System Role
It gives AOIS an owned high-performance model execution path.

3. Minimal Technical Definition
It is a service that receives structured inference requests, executes a model on GPU-backed serving infrastructure, and returns output with latency, token, and backend metadata.

4. Hands-on Proof
The validator and simulator prove the request/response contract and performance budget locally without GPU runtime or model download.

## 4-Level System Explanation Drill

1. Simple English
AOIS plans a GPU inference service without running a GPU.

2. Practical Explanation
I can inspect the service contract, serving options, latency budget, throughput target, and live-use gates.

3. Technical Explanation
`v13` adds a GPU inference service plan, a no-runtime validator, and a local profile simulator.

4. Engineer-Level Explanation
AOIS now separates GPU inference design from GPU inference execution, requiring model license review, model size review, memory budget, cost budget, latency and throughput measurement, fallback route, observability, rollback, and primary-project separation before live GPU serving is approved.

## Failure Story

Representative failure:

- Symptom: a model download fills disk and the server becomes unstable before inference even starts
- Root cause: model size and storage budget were skipped
- Fix: remove the model artifact, restore disk headroom, and require model download approval
- Prevention: keep `model_downloaded=false` until license, size, storage, memory, cost, and rollback are approved
- What this taught me: inference operations begin before the first request is served

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v13` solve in AOIS?
2. What is GPU-backed inference?
3. How is owning inference different from calling a model API?
4. What is the role of a NIM-style serving option in this lesson?
5. Why are model downloads gated?
6. Why are token counts part of the response contract?
7. Why does the plan require latency and throughput measurements?
8. Why is fallback routing required?
9. Why is live GPU approval false?
10. Explain GPU inference service using the 4-layer tool rule.
11. Explain `v13` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v13` solve in AOIS?

It defines the first owned inference service contract and readiness gates without running GPU infrastructure.

2. What is GPU-backed inference?

Model execution served by infrastructure using GPUs for acceleration.

3. How is owning inference different from calling a model API?

Owning inference means AOIS must handle runtime, model artifacts, memory, latency, throughput, observability, cost, and fallback behavior.

4. What is the role of a NIM-style serving option in this lesson?

It represents a packaged GPU inference microservice path for comparison, but it is not installed or run.

5. Why are model downloads gated?

Models can be large, licensed, costly to store, and operationally risky.

6. Why are token counts part of the response contract?

They support cost, throughput, latency, and capacity analysis.

7. Why does the plan require latency and throughput measurements?

Because inference quality includes performance, not just output text.

8. Why is fallback routing required?

AOIS needs a safe path when GPU inference is unavailable or overloaded.

9. Why is live GPU approval false?

No GPU hardware, model download, driver plan, image plan, memory budget, cost budget, or rollback approval exists for this lesson.

10. Explain GPU inference service using the 4-layer tool rule.

- Plain English: it runs model requests on GPU-backed infrastructure.
- System Role: it gives AOIS an owned high-performance model execution path.
- Minimal Technical Definition: it serves structured inference requests and returns output with latency, token, and backend metadata.
- Hands-on Proof: the validator and simulator prove the contract without GPU runtime.

11. Explain `v13` using the 4-level system explanation rule.

- Simple English: AOIS plans GPU inference without running a GPU.
- Practical explanation: I can inspect service shape, serving choices, performance budget, and gates.
- Technical explanation: `v13` adds an inference plan, validator, and local simulator.
- Engineer-level explanation: AOIS now gates live GPU inference behind license, model size, memory, cost, latency, throughput, fallback, observability, rollback, and primary-project separation controls.

## Connection Forward

`v13` defines the GPU inference service boundary.

`v13.5` moves deeper into GPU infrastructure operations: device plugins, scheduling, observability, MIG awareness, and resource constraints.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v13 Introduction](02-introduction.md)
- Next: [v13 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
