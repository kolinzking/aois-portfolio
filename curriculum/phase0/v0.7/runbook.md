# v0.7 Runbook

Authoring status: authored

## Purpose

Use this runbook when the dry-run LLM request builder fails, produces confusing estimates, or appears to risk a real provider call.

## Primary Checks

Compile:

```bash
python3 -m py_compile examples/raw_llm_request.py
```

Run a default dry-run:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx after deploy
```

Confirm these fields exist:

- `mode`
- `request`
- `estimate`
- `expected_structured_fields`

Confirm `mode` is:

```text
dry_run_no_provider_call
```

Confirm there is no API key usage:

```bash
grep -n "API_KEY\|OPENAI\|GROQ\|ANTHROPIC" examples/raw_llm_request.py
```

## Recovery Steps

If the script does not compile:

- read the Python error line
- fix syntax first
- rerun `python3 -m py_compile`

If the script rejects arguments:

- confirm `--max-output-tokens` is at least `1`
- confirm `--latency-budget-ms` is at least `1`
- confirm `--cost-per-million-tokens` is not negative
- confirm `--temperature` is between `0` and `2`

If the cost estimate looks wrong:

- compare `estimated_total_tokens`
- compare `max_output_tokens`
- compare `cost_per_million_tokens`
- remember that this lesson uses rough token estimation, not provider billing

If output format is `text`:

- switch back to `--format json_object`
- explain why parseable output is safer for AOIS automation

If you are about to add a real provider call:

- stop
- define the provider
- define the budget
- confirm key storage
- get explicit approval
- update resource and source-currency notes
