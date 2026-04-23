# v0.7 Runbook

## Purpose

Use this when the raw model-call example is unclear or failing.

## Primary Checks

```bash
sed -n '1,220p' examples/raw_llm_request.py
python3 -m py_compile examples/raw_llm_request.py
cat .env.example
```

## Recovery Steps

If the key is missing:

- create `.env` from `.env.example`
- export or load `ANTHROPIC_API_KEY`

If the call is not supposed to run in this environment:

- still inspect the request anatomy and explain the flow
