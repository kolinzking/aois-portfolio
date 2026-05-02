# v0.7 Failure Story

Authoring status: authored

## Symptom

The estimated request cost jumped sharply during dry-run practice.

## Root Cause

`--max-output-tokens` was set far higher than the incident response needed.

The input prompt was small, but the output budget allowed a large maximum response.

## Fix

Reduce output budget:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx --max-output-tokens 100
```

Keep output structured:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx --format json_object
```

## Prevention

Estimate before provider calls.

Set an output budget that matches the task:

- short triage: small budget
- detailed diagnosis: larger budget
- production automation: strict structured fields and validation

## What This Taught Me

Output limits are operational controls.

A prompt can look harmless while still creating cost and latency risk if output budget is uncontrolled.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.7 Runbook](05-runbook.md)
- Next: [v0.7 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
