# v6.5 Benchmark

Authoring status: authored

## Measurements

Record:

- validator compile result
- validator status
- service account name
- RBAC rule count
- token automount setting
- network policy presence
- whether `kubectl apply` ran
- repo disk footprint

## Score

| Score | Meaning |
|---|---|
| 5 | You can inspect, validate, break, explain, and defend identity controls. |
| 4 | Plan validates, but one identity concept needs review. |
| 3 | Files exist, but RBAC or token reasoning is weak. |
| 2 | Identity manifests exist, but trust boundary is unclear. |
| 1 | Pods still feel like anonymous containers. |

Minimum pass: `4`.

## Interpretation

At `v6.5`, good means:

- service account is explicit
- token automount is disabled
- RBAC grants no permissions yet
- network policy exists
- no live cluster mutation happened
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v6.5 Failure Story](failure-story.md)
- Next: [v6.5 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
