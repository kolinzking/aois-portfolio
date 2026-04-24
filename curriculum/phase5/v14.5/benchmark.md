# v14.5 Benchmark

Authoring status: authored

## Measurements

Record:

- validator status
- simulator status
- hit rate by layer
- latency by layer
- token reduction by layer
- cache service status
- Redis install status
- repo disk footprint
- memory snapshot

## Interpretation

A passing benchmark proves the local cache simulation is consistent.

It does not prove production cache safety.

Production caching requires live workload data, cache key review, privacy review, invalidation testing, and approval.
