# v13 Benchmark

Authoring status: authored

## Measurements

Record:

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

## Interpretation

A passing benchmark proves the local inference contract is valid.

It does not prove live GPU readiness.

Live readiness requires actual hardware or cloud approval, driver/runtime plan, model artifact approval, memory budget, cost budget, observability, fallback route, and rollback.
