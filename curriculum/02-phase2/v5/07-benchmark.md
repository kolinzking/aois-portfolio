# v5 Benchmark

Authoring status: authored

## Measurements

Record:

- Python compile result
- safe input risk level
- prompt-injection risk level
- secret-like input redaction result
- provider-call status
- whether any real secret was added
- repo disk footprint
- memory snapshot if checkpointing

## Score

| Score | Meaning |
|---|---|
| 5 | You can inspect, test, break, explain, and defend local security checks. |
| 4 | Checks work, but one concept needs review. |
| 3 | CLI works, but redaction or provider reasoning is weak. |
| 2 | Output appears, but security boundary is unclear. |
| 1 | Security still means hiding keys after the fact. |

Minimum pass: `4`.

## Interpretation

At `v5`, good means:

- prompt-injection signals are visible
- secret-like content is redacted
- provider calls remain blocked by default
- findings are structured
- real secrets are not added
- security is treated as pre-provider design
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v5 Failure Story](06-failure-story.md)
- Next: [v5 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
