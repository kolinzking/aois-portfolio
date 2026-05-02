# v3 Benchmark

Authoring status: authored

## Measurements

Record:

- Python compile result
- local eval score
- total cases
- passed cases
- trace ID presence
- API eval response
- provider-call status
- whether uvicorn was stopped
- repo disk footprint
- memory snapshot if checkpointing

## Score

| Score | Meaning |
|---|---|
| 5 | You can run, inspect, break, explain, and defend the reliability baseline. |
| 4 | Eval works, but one concept needs review. |
| 3 | Script runs, but regression or trace reasoning is weak. |
| 2 | Output appears, but baseline purpose is unclear. |
| 1 | Reliability still means one manual test. |

Minimum pass: `4`.

## Interpretation

At `v3`, good means:

- local evals are repeatable
- trace IDs are present
- provider calls remain false
- known cases pass
- failures would be visible
- server runtime is controlled

## Resource Note

This version uses existing Python and FastAPI dependencies.

Expected impact:

- disk: small Python/Markdown edits only
- RAM: short-lived uvicorn only during validation
- external provider calls: none
- persistent runtime: none
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v3 Failure Story](06-failure-story.md)
- Next: [v3 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
