# v0.5 Benchmark

Authoring status: authored

## Measurements

Record:

- could all Python files compile?
- could you run three examples in under 30 seconds?
- could you explain one result field by field?
- could you trigger and explain the empty-message failure?
- could you say what Python improved over Bash?

## Score

| Score | Meaning |
|---|---|
| 5 | Run, explain, break, and extend the Python layer without hints. |
| 4 | Complete the lab with only one concept needing review. |
| 3 | Run examples, but struggle to explain structure. |
| 2 | Code runs, but models/functions/exceptions are unclear. |
| 1 | Python still feels like copied text. |

Minimum pass: `4`.

## Interpretation

At `v0.5`, good means:

- Python files compile
- incident input is structured
- analysis output is structured
- invalid input fails clearly
- deterministic rules are understood as a baseline, not intelligence

## Next Measurement

In `v0.6`, the measurement shifts from local CLI behavior to HTTP API behavior:

- can the Python logic be exposed through FastAPI?
- can request validation fail cleanly?
- can the endpoint be inspected with `curl`?
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.5 Failure Story](06-failure-story.md)
- Next: [v0.5 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
