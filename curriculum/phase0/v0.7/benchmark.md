# v0.7 Benchmark

Authoring status: authored

## Measurements

Record:

- whether `examples/raw_llm_request.py` compiled
- whether default dry-run output was valid JSON
- whether `mode` proved no provider call happened
- default `estimated_total_tokens`
- default `estimated_cost_usd`
- estimated total tokens with `--max-output-tokens 100`
- estimated total tokens with `--max-output-tokens 5000`
- behavior with `--format text`
- repo disk footprint after the lesson
- whether any persistent runtime was started

## Score

| Score | Meaning |
|---|---|
| 5 | You can design, run, estimate, break, explain, and defend a provider-neutral LLM request. |
| 4 | The dry-run works, but one concept needs review. |
| 3 | The script runs, but token/cost or structured-output reasoning is weak. |
| 2 | Output appears, but the model-call boundary is unclear. |
| 1 | LLM calls still feel like magic provider usage. |

Minimum pass: `4`.

## Interpretation

At `v0.7`, good means:

- no provider was contacted
- token estimate is understood as rough
- output budget is treated as a cost and latency control
- structured output is preferred for AOIS integration
- API keys are understood as an operational and security boundary
- the learner can explain why provider integration comes later

## Resource Note

This version should not materially increase resource usage.

Expected impact:

- disk: small Markdown/Python edits only
- memory: no persistent runtime
- network: none
- external API/cloud usage: none
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.7 Failure Story](failure-story.md)
- Next: [v0.7 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
