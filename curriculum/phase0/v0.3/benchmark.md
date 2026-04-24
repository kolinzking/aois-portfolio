# v0.3 Benchmark

Authoring status: authored

## Measurements

Record:

- could you identify clean vs dirty repo state in under 10 seconds?
- could you explain the most recent commit?
- could you inspect what changed in the most recent commit?
- could you write a specific commit message without vague words?
- could you decide whether visible files belonged in one commit?

## Score

| Score | Meaning |
|---|---|
| 5 | Inspect, stage, commit, and explain history without hints. |
| 4 | Complete the workflow with only one concept needing review. |
| 3 | Run commands, but need help with staging decisions. |
| 2 | Commit, but cannot explain what belongs together. |
| 1 | Git still feels like magic or danger. |

Minimum pass: `4`.

## Interpretation

At `v0.3`, good means:

- Git status is readable
- diffs are reviewed before staging
- commits are small and coherent
- messages explain intent
- history makes AOIS easier to inspect

## Next Measurement

In `v0.4`, the measurement shifts from repository history to HTTP and network inspection:

- can you inspect requests?
- can you explain service boundaries?
- can you distinguish local command failure from network failure?
