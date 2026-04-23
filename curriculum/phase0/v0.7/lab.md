# v0.7 Lab

## Build Lab

Inspect:

```bash
sed -n '1,220p' examples/raw_llm_request.py
```

## Ops Lab

If configured locally:

```bash
python3 examples/raw_llm_request.py
```

Otherwise, explain the request flow from the file itself.

## Break Lab

```bash
env -u ANTHROPIC_API_KEY python3 examples/raw_llm_request.py
```

Expected:

- runtime error about missing key

## Explanation Lab

Question:
What did the LLM improve compared with `v0.6`?

Answer:
It improved general reasoning over varied language.

Question:
What problem still remains?

Answer:
The output is still free text, not guaranteed structured fields.

## Defense Lab

Why introduce the raw SDK before any wrapper?

Because the raw call exposes the true provider interface and cost/latency/auth reality.
