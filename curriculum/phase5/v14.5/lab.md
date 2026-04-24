# v14.5 Lab

Authoring status: authored

## Build Lab

Run:

```bash
python3 -m py_compile examples/validate_performance_caching_plan.py examples/simulate_performance_caching.py
python3 examples/validate_performance_caching_plan.py
python3 examples/simulate_performance_caching.py
```

## Ops Lab

Answer from the simulator:

1. Which layer is the baseline?
2. Which layer has the strongest latency gain?
3. Which layer has the strongest token reduction?
4. Which layer has the highest hit rate?

Answer key:

1. `no-cache-baseline`
2. `response-cache-placeholder`
3. `response-cache-placeholder`
4. `prefix-reuse-placeholder`

## Break Lab

Use a scratch copy only.

Break 1: set `redis_installed` to `true`.

Expected result: validation fails because no live cache infrastructure is approved.

Break 2: remove `tenant_isolation_required`.

Expected result: validation fails because cache state needs tenant boundaries.

Break 3: remove `ttl_required`.

Expected result: validation fails because cached data needs lifecycle control.

## Explanation Lab

Explain:

1. Why cache key design is a security boundary.
2. Why response caching is riskier than prefix reuse.
3. Why TTL and invalidation are both needed.
4. Why hit rate does not prove correctness.
5. Why Redis is a runtime decision, not a default.

## Defense Lab

Defend this decision:

AOIS should not run live caching until backend approval, cache key review, TTL/invalidation review, privacy boundary, tenant isolation, hit-rate baseline, cost baseline, fallback route, rollback, and primary AOIS separation exist.
