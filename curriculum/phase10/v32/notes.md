# v32 - Edge And Offline Inference

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no edge runtime,
no offline model load, no model runtime, no model download, no quantization
execution, no device access, no GPU, no NPU, no camera, no microphone, no media
file read, no network call, no provider call, no command execution, no tool
execution, no persistent storage

## What This Builds

This version builds a local edge and offline inference contract:

- `frontier/aois-p/edge-offline-inference.plan.json`
- `examples/validate_edge_offline_inference_plan.py`
- `examples/simulate_edge_offline_inference.py`

It teaches:

- central, edge-online, and offline-edge deployment choices
- device profile constraints
- model format and model size budgets
- quantization review before constrained deployment
- memory, compute, power, and latency budgets
- offline cache and sync readiness
- stale model indicators
- data residency and privacy placement gates
- central fallback from edge failure
- observability buffering during degraded connectivity
- update channel and rollback requirements
- access and release gates for edge deployments

## Why This Exists

v31 added multimodal AOIS contracts. v32 asks what changes when inference does
not always run in a centralized cloud path.

Edge and offline deployment can reduce latency, preserve privacy, keep a site
working during network loss, and support local operational workflows. It also
adds constraints that a central runtime can hide:

- smaller memory budgets
- limited CPU, GPU, NPU, or accelerator capacity
- power limits
- slower or intermittent network
- stale model packages
- local cache correctness
- delayed telemetry
- harder update and rollback paths
- tighter data residency decisions

The central edge question is:

```text
Given deployment target, connectivity, device profile, model format,
model size, quantization state, memory, compute, power, latency, cache,
sync, freshness, residency, privacy, fallback, observability, update,
rollback, access, and release status, should AOIS-P run centrally, run at
the edge, run offline from cache, block, hold, or fall back?
```

v32 answers that question locally. It does not load a model or touch a device.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution -> show operators the state -> scope access -> release changes safely -> track model delivery evidence -> package reusable platform controls -> reason over non-text signals -> deploy inference under edge constraints`

v32 consumes v31 and Phase 9:

- v31 defines what non-text signals may be analyzed
- release controls decide whether an edge model version may ship
- model delivery tracking records which model package is eligible
- platform controls define reusable resource, policy, and observability gates
- policy-aware access still scopes who can see and act on local results

The output is an edge placement decision: central, edge online, offline,
blocked, held, or fallback.

## Learning Goals

By the end of this version you should be able to:

- compare central, edge-online, and offline-edge inference paths
- define a device profile for AOIS-P deployment planning
- explain why model size, memory, compute, power, and latency budgets are separate gates
- explain why offline inference needs cache, sync, and freshness controls
- identify data residency and privacy placement risks
- require observability buffers when connectivity is degraded
- require signed update channels and rollback before live edge deployment
- route to central fallback only when policy, connectivity, privacy, and residency allow it
- keep edge deployment under release and access control

## Prerequisites

You should have completed:

- Phase 8 product visibility and policy-aware access
- Phase 9 delivery, model-delivery, and platform patterns
- v31 multimodal AOIS

Required checks:

```bash
python3 -m py_compile examples/validate_edge_offline_inference_plan.py examples/simulate_edge_offline_inference.py
python3 examples/validate_edge_offline_inference_plan.py
python3 examples/simulate_edge_offline_inference.py
```

## Core Concepts

## Deployment Target

v32 models three targets:

- `central_cloud`: cloud or central cluster inference with online connectivity
- `edge_online`: edge inference while the device can still sync and receive updates
- `offline_edge`: local inference when connectivity is offline or degraded

The target is not a preference label. It changes the dominant constraints.

## Device Profile

A device profile defines what a target can safely run:

- device class
- maximum model size
- memory budget
- latency budget
- quantization requirement
- power sensitivity

Unknown profiles are blocked because the system cannot prove the model fits.

## Model Format And Quantization

v32 records model format and quantization review. It does not quantize a model.
The point is to separate deployment evidence from execution:

- format tells operators what runtime class the package expects
- quantization review tells operators whether constrained targets were considered
- model size tells operators whether the package fits the device profile

## Resource Budgets

Edge inference needs resource evidence before it runs:

- memory budget prevents local exhaustion
- compute budget prevents unmeasured accelerator assumptions
- power budget protects battery and power-sensitive devices
- latency budget protects the operator workflow

Each budget is checked independently because passing one does not imply passing
the others.

## Offline Cache And Sync

Offline inference needs a prepared cache and a sync policy. The cache answers
whether the local package and supporting data are available. The sync policy
answers how results, traces, counters, and operator notes reconcile when the
device reconnects.

## Model Freshness

An offline model can be valid but stale. v32 requires a freshness indicator so
operators know whether the cached model version is still approved for use.

## Residency And Privacy Placement

Edge does not automatically mean private. Results may sync later, logs may
leave the site, and central fallback may cross a residency boundary. v32 blocks
residency failures and unredacted payloads before placement.

## Fallback

Central fallback is allowed only when:

- connectivity is online or degraded
- residency passes
- privacy is redacted or absent
- access policy passes
- release policy passes

Fallback is a governed route, not an escape hatch.

## Observability Buffer

Offline and degraded edge paths need telemetry buffering. Without a buffer,
operators lose traces, model-version evidence, failures, and resource signals.
v32 holds missing buffers before offline execution.

## Update And Rollback

Edge deployments must be updateable and reversible. v32 blocks missing update
channels and missing rollback because a bad model, policy, or runtime package
can remain stranded on a device.

## Build

Inspect:

```bash
sed -n '1,900p' frontier/aois-p/edge-offline-inference.plan.json
sed -n '1,520p' examples/validate_edge_offline_inference_plan.py
sed -n '1,360p' examples/simulate_edge_offline_inference.py
```

Compile:

```bash
python3 -m py_compile examples/validate_edge_offline_inference_plan.py examples/simulate_edge_offline_inference.py
```

Validate:

```bash
python3 examples/validate_edge_offline_inference_plan.py
```

Simulate:

```bash
python3 examples/simulate_edge_offline_inference.py
```

Expected:

```json
{
  "passed_cases": 18,
  "score": 1.0,
  "status": "pass",
  "total_cases": 18
}
```

## Ops Lab

1. Open the edge and offline inference plan.
2. Find `deployment_targets`.
3. Compare central, edge-online, and offline-edge constraints.
4. Find `device_profiles`.
5. Explain why a gateway profile requires quantization review and power review.
6. Find `case_defaults`.
7. Confirm the default path is edge-online, known, budgeted, redacted, observable, updateable, rollback-ready, access-approved, and release-approved.
8. Find `edge_cases`.
9. Confirm every decision gate has a case.
10. Run the validator.
11. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Remove `gateway_edge` from `device_profiles`.
2. Confirm validation fails.
3. Restore the profile.
4. Change `case_defaults.model_size_mb` to `700`.
5. Confirm the default edge path can no longer allow edge inference.
6. Restore the value.
7. Change `offline_cached_inference_allowed.overrides.connectivity_status` to `online`.
8. Explain why the case no longer represents offline operation.
9. Restore the value.
10. Change `rollback_missing_blocked.overrides.rollback_ready` to `true`.
11. Confirm that case no longer blocks.
12. Restore the value.

## Testing

The validator checks:

- no live edge, model, quantization, device, GPU, NPU, camera, microphone, media, network, provider, command, or tool runtime is enabled
- source notes are current for May 1, 2026
- edge scope controls are explicit
- required controls are true
- edge dimensions are present
- deployment targets are complete
- device profiles are complete
- decision gates are complete
- defaults describe a safe edge-online path
- every decision has a case
- live edge review checks are listed

The simulator checks:

- central cloud inference is allowed when central controls pass
- edge-online inference is allowed when device, resource, policy, update, and rollback controls pass
- offline cached inference is allowed when cache, sync, freshness, and buffers are ready
- unknown device profiles are blocked
- model size budget failures are blocked
- memory budget failures are blocked
- compute uncertainty is held when central fallback is unavailable
- power uncertainty is held on power-sensitive targets
- latency budget failures are blocked
- missing offline cache is held
- stale offline model state is held
- data residency violations are blocked
- unredacted payloads are blocked
- eligible edge failures route to central fallback
- missing observability buffers are held
- missing update channels are blocked
- missing rollback is blocked
- policy boundary failures are blocked

## Common Mistakes

- assuming edge is always safer than central inference
- treating device class as documentation instead of a hard gate
- checking model size but not memory
- checking memory but not power
- checking latency only after deployment
- calling an offline cache ready without sync policy
- ignoring stale model indicators
- logging sensitive local payloads before redaction
- allowing fallback across a residency boundary
- shipping edge packages without rollback

## Troubleshooting

If validation fails:

- read the `missing` list
- restore false runtime flags
- restore source notes and dates
- restore scope and required controls
- restore deployment targets, device profiles, and live checks

If simulation fails:

- compare `decision` to `expected_decision`
- inspect the case override
- inspect device profile and budgets
- inspect fallback eligibility
- inspect cache, sync, freshness, observability, update, rollback, access, and release status

## Benchmark

Run:

```bash
python3 -m py_compile examples/validate_edge_offline_inference_plan.py examples/simulate_edge_offline_inference.py
python3 examples/validate_edge_offline_inference_plan.py
python3 examples/simulate_edge_offline_inference.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- edge runtime, model runtime, device, GPU, NPU, media, network, and provider flags

## Architecture Defense

Defend this design:

- edge deployment is modeled before device access
- central, edge, and offline paths are separate decisions
- device profile gates precede runtime assumptions
- model format and quantization review are recorded before deployment
- resource budgets are independent gates
- offline cache, sync, and freshness are required together
- telemetry buffering is part of offline safety
- fallback is policy-aware
- update and rollback are release controls
- primary AOIS remains excluded

## 4-Layer Tool Drill

Explain v32 at four layers:

- placement: central, edge-online, offline-edge
- resources: model size, memory, compute, power, latency
- continuity: cache, sync, freshness, observability buffer
- governance: residency, privacy, fallback, update, rollback, access, release

## 4-Level System Explanation Drill

Explain v32 at four levels:

- beginner: AOIS-P decides whether inference should run centrally, at the edge, offline, or not at all
- practitioner: edge inference needs known devices, fitted models, budgets, privacy controls, telemetry buffers, updates, and rollback
- engineer: the simulator evaluates one placement failure mode at a time and returns central, edge, offline, blocked, held, or fallback
- architect: AOIS-P expands deployment topology while preserving release, access, model-delivery, observability, and governance contracts

## Failure Story

An incident site loses connectivity. A gateway keeps running a cached model, but
the package is stale, telemetry is not buffered, and no signed update channel
exists. When the site reconnects, central operators cannot explain which model
made the local recommendation or why the result differs from the current
release.

v32 prevents this by requiring cache readiness, sync policy, freshness
indicators, observability buffers, approved update channels, rollback, privacy,
residency, access, and release gates before edge or offline inference.

## Mastery Checkpoint

You are ready to move on when you can:

- explain the difference between central, edge-online, and offline-edge inference
- define device profiles and resource budgets
- trace an edge case through block, hold, fallback, central, edge, and offline outcomes
- explain why offline inference needs cache, sync, freshness, and buffered telemetry
- explain why update and rollback are mandatory for live edge deployment
- pass validation and simulation without device or model runtime

## Connection Forward

v33 builds on v32 by attacking the system instead of only placing it. Once
AOIS-P can model multimodal signals and constrained deployment paths, the next
frontier question is whether adversarial prompts, poisoned inputs, malicious
tool instructions, policy confusion, and red-team scenarios can break those
controls before live use.

## Source Notes

Checked 2026-05-02.

- Kubernetes node documentation: used for resource, placement, and workload-location vocabulary.
- vLLM documentation: used for inference-serving and resource-budget vocabulary at a conceptual level.
- OpenAI safety best-practices guidance: used for safety-review and constrained deployment framing.
- v32 is a local edge/offline placement contract. It does not run a model, start device software, deploy Kubernetes workloads, sync updates, or call providers.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v32 Introduction](introduction.md)
- Next: [v32 Lab](lab.md)
<!-- AOIS-NAV-END -->
