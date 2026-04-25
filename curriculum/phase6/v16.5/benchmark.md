# v16.5 Benchmark

Authoring status: authored

## Measurements

Record:

- validator status
- simulator status
- incident step count
- tool call count
- provider call status
- agent runtime status
- collector/backend status
- repo disk footprint
- memory snapshot

## Interpretation

A passing benchmark proves the local incident trace shape is internally consistent.

It does not prove live agent runtime or telemetry backend readiness.

Live readiness requires step taxonomy, tool-call policy, redaction testing, sampling, storage budget, and approval.
