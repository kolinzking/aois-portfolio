# v0.8 Benchmark

Authoring status: authored

## Measurements

Record:

- `python3 -m py_compile examples/validate_schema.py` result
- `python3 examples/validate_schema.py` result
- `missing` field from validator output
- schema namespace
- number of required checks
- whether Postgres was started
- whether dependencies were installed
- repo disk footprint
- memory snapshot if a checkpoint is being made

## Score

| Score | Meaning |
|---|---|
| 5 | You can inspect, validate, break, explain, and defend the persistence schema safely. |
| 4 | Validator passes, but one database concept needs review. |
| 3 | Validator runs, but relationships or constraints are weak. |
| 2 | Schema exists, but persistence design is unclear. |
| 1 | Database work still feels like magic storage. |

Minimum pass: `4`.

## Interpretation

At `v0.8`, good means:

- `aois_p` clearly separates portfolio database objects
- incidents have durable records
- analysis results link back to incidents
- LLM request plans preserve provider-gating decisions
- constraints protect data quality
- indexes anticipate common lookups
- no database runtime is used without approval

## Resource Note

This version should not materially increase server usage.

Expected impact:

- disk: small SQL/Python/Markdown edits only
- memory: no persistent runtime
- network: none
- external API/cloud usage: none
- database server: none
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.8 Failure Story](06-failure-story.md)
- Next: [v0.8 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
