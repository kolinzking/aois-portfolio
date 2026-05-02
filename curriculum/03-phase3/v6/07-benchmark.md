# v6 Benchmark

Authoring status: authored

## Measurements

Record:

- validator compile result
- validator status
- namespace name
- quota values
- deployment resource requests/limits
- whether `kubectl apply` ran
- whether any resource was created
- repo disk footprint
- memory snapshot

## Score

| Score | Meaning |
|---|---|
| 5 | You can inspect, validate, break, explain, and defend Kubernetes manifests without applying. |
| 4 | Plan validates, but one Kubernetes concept needs review. |
| 3 | Files exist, but resource or namespace reasoning is weak. |
| 2 | Manifests exist, but cluster risk is unclear. |
| 1 | Kubernetes still means blindly applying YAML. |

Minimum pass: `4`.

## Interpretation

At `v6`, good means:

- namespace is clearly `aois-p`
- quotas and limits exist
- deployment has one replica
- service is `ClusterIP`
- provider calls are disabled
- no live cluster mutation happened
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v6 Failure Story](06-failure-story.md)
- Next: [v6 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
