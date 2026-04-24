# v0.6 Benchmark

Authoring status: authored

## Measurements

Record:

- disk footprint before install
- disk footprint after install if approved
- whether `/health` returned `200`
- whether `/analyze` returned structured JSON
- whether invalid input failed validation
- whether the server was stopped after the lab

## Score

| Score | Meaning |
|---|---|
| 5 | Install, run, inspect, break, explain, and stop the API safely. |
| 4 | API works, but one concept needs review. |
| 3 | API runs, but validation or HTTP inspection needs help. |
| 2 | Server starts, but route behavior is unclear. |
| 1 | FastAPI feels like magic. |

Minimum pass: `4`.

## Interpretation

At `v0.6`, good means:

- API contract is visible
- request validation is visible
- response shape is stable
- HTTP inspection habits carry forward
- runtime resources are controlled

## Resource Note

If install is approved, update `RESOURCE-USAGE.md` with:

- `.venv` disk footprint
- repo disk footprint
- whether any process is still running
