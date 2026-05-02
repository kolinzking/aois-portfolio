# v0.4 Benchmark

Authoring status: authored

## Measurements

Record:

- could you start the local server in under 60 seconds?
- could you get a `200` response from the probe?
- could you intentionally create and explain a connection failure?
- could you intentionally create and explain a `404`?
- could you identify status code, total time, content type, and body size?

## Score

| Score | Meaning |
|---|---|
| 5 | Run, inspect, break, and explain HTTP behavior without hints. |
| 4 | Complete the lab with only one concept needing review. |
| 3 | Run commands, but failure classification needs help. |
| 2 | Get a response, but cannot explain it. |
| 1 | HTTP still feels like browser magic. |

Minimum pass: `4`.

## Interpretation

At `v0.4`, good means:

- HTTP no longer feels like a browser-only concept
- status codes are visible
- connection failures and HTTP errors are distinct
- local service boundaries are inspectable

## Next Measurement

In `v0.5`, the measurement shifts to Python:

- can you express AOIS logic in typed code?
- can you validate inputs?
- can you handle errors without hiding them?
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.4 Failure Story](06-failure-story.md)
- Next: [v0.4 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
