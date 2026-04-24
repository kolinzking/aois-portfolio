# v1 Benchmark

Authoring status: authored

## Measurements

Record:

- Python compile result
- `/ai/analyze` status code
- `provider_mode`
- `provider_call_made`
- provider-forcing status code
- invalid-input status code
- whether server was stopped
- repo disk footprint
- memory snapshot if checkpointing

## Score

| Score | Meaning |
|---|---|
| 5 | You can run, inspect, break, explain, and defend the provider-gated structured endpoint. |
| 4 | Endpoint works, but one concept needs review. |
| 3 | Route works, but provider gate or structured output is unclear. |
| 2 | Server runs, but AI endpoint behavior is unclear. |
| 1 | AI endpoint still means blind provider call. |

Minimum pass: `4`.

## Interpretation

At `v1`, good means:

- the route accepts validated incident input
- the response has stable fields
- provider execution is visibly blocked
- deterministic baseline still works
- the server is not left running
- no external AI service is contacted

## Resource Note

This version uses the existing FastAPI `.venv`.

Expected impact:

- disk: small Python/Markdown edits only
- RAM: short-lived uvicorn only during validation
- external provider calls: none
- persistent runtime: none
