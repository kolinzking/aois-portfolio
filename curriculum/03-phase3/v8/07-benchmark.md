# v8 Benchmark

Authoring status: authored

## Measurements

Record:

- validator compile result
- validator status
- Application name
- source path
- destination namespace
- whether `kubectl apply` ran
- whether ArgoCD sync ran
- repo disk footprint
- memory snapshot

## Score

| Score | Meaning |
|---|---|
| 5 | You can inspect, validate, break, explain, and defend GitOps flow without syncing. |
| 4 | Plan validates, but one GitOps concept needs review. |
| 3 | Files exist, but source/destination or sync policy is weak. |
| 2 | Application exists, but sync risk is unclear. |
| 1 | GitOps still feels like magic deployment. |

Minimum pass: `4`.

## Interpretation

At `v8`, good means:

- desired state is reviewable
- source path is clear
- destination namespace is `aois-p`
- automated sync is disabled
- no live ArgoCD action occurred
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v8 Failure Story](06-failure-story.md)
- Next: [v8 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
