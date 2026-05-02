# v0.2 Benchmark

Authoring status: authored

## Measurements

Record:

- did the script feel instant to run?
- could you read the report in under 10 seconds?
- did the script remove enough repetition to feel worth keeping?
- did the analyzer classify known examples correctly?
- did the analyzer preserve unmatched examples as `unknown`?

## Score

Use this scale:

| Score | Meaning |
|---|---|
| 5 | Both scripts run, and you can explain every Bash mechanism and rule limitation. |
| 4 | Both scripts run, and only one explanation needs review. |
| 3 | Scripts run, but diagnosis still needs hints. |
| 2 | One script works, but Bash behavior is mostly copied. |
| 1 | Script execution still feels random. |

Minimum pass: `4`.

## Interpretation

At `v0.2`, good means:

- fast enough to use casually
- clear enough to read quickly
- helpful enough that you would rather run it than type the raw commands every time
- honest enough to say `unknown` when rules do not match

## Next Measurement

In `v0.3`, the benchmark shifts from script behavior to repository discipline:

- can you make small meaningful commits?
- can you inspect history?
- can the repo explain how AOIS changed over time?
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.2 Failure Story](failure-story.md)
- Next: [v0.2 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
