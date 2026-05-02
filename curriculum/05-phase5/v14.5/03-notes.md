# v14.5 - Performance Engineering And Caching Without Runtime

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: caching plan and simulation only, no Redis install, no cache service, no live cache writes, no inference runtime

## What This Builds

This version builds a performance and caching plan:

- `inference/aois-p/performance-caching.plan.json`
- `examples/validate_performance_caching_plan.py`
- `examples/simulate_performance_caching.py`

It teaches:

- no-cache baseline
- prompt caching
- prefix reuse
- response caching
- cache key design
- TTL and invalidation
- privacy and tenant boundaries
- hit-rate and cost-savings measurement
- batching tradeoff review

## Why This Exists

Performance engineering is not random speed work.

AOIS needs to know what work is being avoided, what correctness risk is introduced, and how the improvement is measured.

Caching can reduce latency and cost, but it can also leak data, return stale output, or hide quality regressions if cache policy is weak.

## AOIS Connection

The AOIS path is now:

`high-throughput serving -> cache-aware performance -> adaptation and memory economics`

`v14.5` teaches AOIS to reduce waste without losing correctness boundaries.

## Learning Goals

By the end of this version you should be able to:

- explain no-cache baseline
- explain prompt caching
- explain prefix reuse
- explain response caching
- explain why cache keys are security boundaries
- explain TTL and invalidation
- explain tenant isolation
- compare simulated latency and token savings
- explain why caching needs measurement

## Prerequisites

You should have completed:

- `v14` high-throughput inference serving

Required checks:

```bash
python3 -m py_compile examples/validate_performance_caching_plan.py examples/simulate_performance_caching.py
python3 examples/validate_performance_caching_plan.py
python3 examples/simulate_performance_caching.py
```

## Core Concepts

## No-Cache Baseline

A no-cache baseline is the reference path.

You need it to prove whether caching actually improves latency or token economics.

## Prompt Caching

Prompt caching avoids repeating work for repeated prompt structure.

It must respect data boundaries and freshness.

## Prefix Reuse

Prefix reuse means reusing common initial context across requests.

This can reduce repeated computation when prompts share a stable prefix.

## Response Cache

Response cache stores final outputs.

It is risky for dynamic, sensitive, or user-specific requests unless keys, TTLs, and tenant boundaries are strict.

## Cache Key

A cache key decides what counts as the same request.

A bad cache key can leak data or return wrong outputs.

## TTL And Invalidation

TTL limits how long cached data lives.

Invalidation removes cache entries when they are no longer valid.

## Hit Rate

Hit rate measures how often cache is used.

High hit rate is not enough if the cached result is wrong.

## Build

Inspect:

```bash
sed -n '1,260p' inference/aois-p/performance-caching.plan.json
sed -n '1,280p' examples/validate_performance_caching_plan.py
sed -n '1,220p' examples/simulate_performance_caching.py
```

Compile:

```bash
python3 -m py_compile examples/validate_performance_caching_plan.py examples/simulate_performance_caching.py
```

Validate:

```bash
python3 examples/validate_performance_caching_plan.py
```

Simulate:

```bash
python3 examples/simulate_performance_caching.py
```

Expected validation:

```json
{
  "cache_service_started": false,
  "redis_installed": false,
  "cache_entries_created": false,
  "inference_runtime_started": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer from the plan and simulator:

1. Which layer is the no-cache baseline?
2. Which layer has the highest simulated hit rate?
3. Which layer has zero simulated billed tokens?
4. Which controls protect freshness?
5. Which controls protect privacy?
6. Which controls prove live Redis/cache is not used?

Answer key:

1. `no-cache-baseline`
2. `prefix-reuse-placeholder`
3. `response-cache-placeholder`
4. `ttl_required`, `invalidation_required`, and `freshness_policy_required`
5. `privacy_boundary_required` and `tenant_isolation_required`
6. `redis_installed=false`, `cache_service_started=false`, and `cache_entries_created=false`

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Allow Live Cache

Set:

```json
"approved_for_live_caching": true
```

Expected risk:

- a simulation-only lesson can be mistaken for permission to start cache infrastructure

### Option B - Remove Tenant Isolation

Set:

```json
"tenant_isolation_required": false
```

Expected risk:

- one user's cached data may affect another user's response

### Option C - Remove Invalidation

Set:

```json
"invalidation_required": false
```

Expected risk:

- stale outputs can persist after the source context changes

## Testing

The version passes when:

1. both scripts compile
2. validator returns `status=pass`
3. simulator returns `status=pass`
4. no cache service starts
5. Redis remains uninstalled
6. no cache entries are created
7. cache policy controls remain true
8. batching tradeoff controls remain true
9. live caching remains unapproved

## Common Mistakes

- treating caching as always safe
- missing tenant isolation
- missing TTL or invalidation
- measuring latency but not hit rate
- measuring hit rate but not correctness
- caching sensitive responses without policy
- installing Redis before deciding whether caching belongs in the runtime

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_performance_caching_plan.py
```

Read `missing`, inspect the plan, and restore required fields.

Common fixes:

- restore runtime/cache flags to `false`
- restore cache layers
- restore TTL and invalidation
- restore privacy and tenant isolation
- restore hit-rate and cost-savings measurement
- restore batching tradeoff controls
- restore live checks

## Benchmark

Measure:

- validator compile result
- validator status
- simulator status
- simulated hit rate by layer
- simulated latency by layer
- simulated token reduction by layer
- cache service status
- Redis install status
- repo disk footprint
- memory snapshot

## Architecture Defense

Why require a no-cache baseline?

Because optimization without a baseline is guessing.

Why treat cache keys as security boundaries?

Because cache keys decide whether two requests share data.

Why disallow live cache writes in this lesson?

Because cache state is persistent system behavior and needs policy before use.

## 4-Layer Tool Drill

Tool: response cache

1. Plain English
It stores a previous answer so the system can return it faster later.

2. System Role
It can reduce latency and token cost for repeatable requests.

3. Minimal Technical Definition
It is a lookup layer keyed by request/context identity that returns stored output when policy allows.

4. Hands-on Proof
The simulator compares response-cache placeholder latency and token billing against the no-cache baseline without writing cache entries.

## 4-Level System Explanation Drill

1. Simple English
AOIS compares caching strategies without starting a cache.

2. Practical Explanation
I can compare hit rate, latency, token reduction, TTL, invalidation, tenant isolation, and fallback controls.

3. Technical Explanation
`v14.5` adds a caching plan, validator, and deterministic caching simulator.

4. Engineer-Level Explanation
AOIS now separates caching design from cache execution, requiring cache key review, TTL, invalidation, privacy boundaries, tenant isolation, hit-rate measurement, cost-savings measurement, fallback, rollback, and primary-project separation before live caching is approved.

## Failure Story

Representative failure:

- Symptom: one user's incident summary appears in another user's response
- Root cause: response cache key omitted tenant/user boundary
- Fix: disable the response cache, purge affected entries, restore tenant isolation, and review cache key design
- Prevention: validate cache policy before live cache writes
- What this taught me: cache correctness is security work

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v14.5` solve in AOIS?
2. Why is a no-cache baseline required?
3. What is prompt caching?
4. What is prefix reuse?
5. Why is response caching risky?
6. Why are TTL and invalidation required?
7. Why is tenant isolation required?
8. Why measure hit rate and token reduction?
9. Why is Redis not installed in this lesson?
10. Explain response cache using the 4-layer tool rule.
11. Explain `v14.5` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v14.5` solve in AOIS?

It teaches caching and performance tradeoffs before live cache infrastructure exists.

2. Why is a no-cache baseline required?

It proves whether caching improves latency or token economics.

3. What is prompt caching?

Reuse of repeated prompt structure or context to reduce repeated work.

4. What is prefix reuse?

Reuse of common initial context across requests.

5. Why is response caching risky?

It can return stale, sensitive, or cross-tenant output if keys and policies are wrong.

6. Why are TTL and invalidation required?

They prevent stale cached data from living indefinitely.

7. Why is tenant isolation required?

It prevents one user or tenant from receiving another user's cached data.

8. Why measure hit rate and token reduction?

They prove whether caching reduces work and cost.

9. Why is Redis not installed in this lesson?

The lesson is design and simulation only; live cache infrastructure needs approval.

10. Explain response cache using the 4-layer tool rule.

- Plain English: it stores an answer for later reuse.
- System Role: it reduces latency and token cost when reuse is safe.
- Minimal Technical Definition: it maps request/context identity to stored output.
- Hands-on Proof: the simulator compares response-cache placeholder results without writing cache entries.

11. Explain `v14.5` using the 4-level system explanation rule.

- Simple English: AOIS compares cache strategies without starting a cache.
- Practical explanation: I can explain hit rate, latency, token reduction, TTL, invalidation, privacy, and tenant controls.
- Technical explanation: `v14.5` adds a cache plan, validator, and simulator.
- Engineer-level explanation: AOIS gates live caching behind cache key review, TTL, invalidation, privacy, tenant isolation, hit-rate and cost-savings baselines, fallback, rollback, and primary-project separation.

## Connection Forward

`v14.5` completes the performance-engineering bridge.

`v15` moves into fine-tuning and adaptation, where AOIS must decide when changing model behavior is better than routing, serving, or caching.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v14.5 Introduction](02-introduction.md)
- Next: [v14.5 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
