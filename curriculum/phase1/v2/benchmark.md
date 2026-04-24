# v2 Benchmark

Authoring status: authored

## Measurements

Record:

- Python compile result
- default route
- fast route decision
- strong route decision
- low-budget fallback decision
- `provider_call_made` value
- whether uvicorn was stopped
- repo disk footprint
- memory snapshot if checkpointing

## Score

| Score | Meaning |
|---|---|
| 5 | You can compare, break, explain, and defend route decisions without provider execution. |
| 4 | Routing works, but one tradeoff needs review. |
| 3 | Endpoint works, but fallback or budget reasoning is weak. |
| 2 | JSON appears, but route selection is unclear. |
| 1 | Model routing still feels like choosing a favorite model. |

Minimum pass: `4`.

## Interpretation

At `v2`, good means:

- route decision is visible
- fallback route is visible
- provider calls remain false
- budget and latency affect selection
- severity can affect route strength
- the local baseline remains available

## Resource Note

This version uses the existing FastAPI `.venv`.

Expected impact:

- disk: small Python/Markdown edits only
- RAM: short-lived uvicorn only during validation
- external provider calls: none
- persistent runtime: none
