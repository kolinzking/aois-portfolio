# v4 Benchmark

Authoring status: authored

## Measurements

Record:

- validator compile result
- validator status
- whether Docker build ran
- whether Docker container ran
- repo disk footprint
- `.venv` footprint
- memory snapshot

## Score

| Score | Meaning |
|---|---|
| 5 | You can inspect, validate, break, explain, and defend the container plan without building. |
| 4 | Plan validates, but one concept needs review. |
| 3 | Files exist, but resource/security reasoning is weak. |
| 2 | Dockerfile exists, but build/runtime risk is unclear. |
| 1 | Docker still means blindly building images. |

Minimum pass: `4`.

## Interpretation

At `v4`, good means:

- packaging plan is clear
- build context is controlled
- runtime naming is unambiguous
- memory and CPU limits are declared
- service binds to localhost
- no Docker resources are created without approval
