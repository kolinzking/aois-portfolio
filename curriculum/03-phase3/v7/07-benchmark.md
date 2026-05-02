# v7 Benchmark

Authoring status: authored

## Measurements

Record:

- validator compile result
- validator status
- chart name
- namespace value
- provider gate value
- whether Helm install ran
- repo disk footprint
- memory snapshot

## Score

| Score | Meaning |
|---|---|
| 5 | You can inspect, validate, break, explain, and defend a Helm chart without installing. |
| 4 | Chart validates, but one Helm concept needs review. |
| 3 | Files exist, but values or templates are unclear. |
| 2 | Chart exists, but install risk is unclear. |
| 1 | Helm still means blindly installing charts. |

Minimum pass: `4`.

## Interpretation

At `v7`, good means:

- chart structure is clear
- values preserve `aois-p`
- provider calls remain disabled
- limits remain configurable
- no Helm release is installed
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v7 Failure Story](06-failure-story.md)
- Next: [v7 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
