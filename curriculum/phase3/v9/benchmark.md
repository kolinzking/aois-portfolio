# v9 Benchmark

Authoring status: authored

## Measurements

Record:

- validator compile result
- validator status
- max replicas
- whether KEDA was installed
- whether `kubectl apply` ran
- repo disk footprint
- memory snapshot

## Score

| Score | Meaning |
|---|---|
| 5 | You can inspect, validate, break, explain, and defend autoscaling plans without scaling. |
| 4 | Plan validates, but one scaling concept needs review. |
| 3 | Files exist, but resource multiplication risk is weak. |
| 2 | HPA exists, but runtime impact is unclear. |
| 1 | Autoscaling still means free extra pods. |

Minimum pass: `4`.

## Interpretation

At `v9`, good means:

- HPA target is clear
- max replicas is capped at `1`
- KEDA is plan-only
- no cluster mutation happened
- scaling risk is understood
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v9 Failure Story](failure-story.md)
- Next: [v9 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
