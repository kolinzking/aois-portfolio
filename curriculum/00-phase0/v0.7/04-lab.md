# v0.7 Lab

Authoring status: authored

## Build Lab

Build `examples/raw_llm_request.py` as shown in `03-notes.md`.

This lab must remain provider-neutral:

- no API key
- no OpenAI call
- no Groq call
- no cloud endpoint
- no paid inference

Compile:

```bash
python3 -m py_compile examples/raw_llm_request.py
```

Run:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx after deploy
```

Success state:

- output is valid JSON
- `mode` is `dry_run_no_provider_call`
- `request` contains system and user prompts
- `estimate` contains token, cost, and latency fields
- `expected_structured_fields` lists parseable AOIS fields

## Ops Lab

Run these commands and compare the estimates:

```bash
python3 examples/raw_llm_request.py pod OOMKilled exit code 137
python3 examples/raw_llm_request.py gateway returned 5xx --max-output-tokens 100
python3 examples/raw_llm_request.py gateway returned 5xx --cost-per-million-tokens 5
python3 examples/raw_llm_request.py gateway returned 5xx --latency-budget-ms 500
```

Expected learning:

- the same request shape can carry different incident messages
- lower output budget lowers estimated maximum token exposure
- higher assumed provider price raises estimated cost
- latency budget is an operational limit, not a model feature
- no external provider is contacted

## Break Lab

Break the request plan on purpose.

### Invalid Output Budget

Run:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx --max-output-tokens 0
```

Expected result:

- the script rejects the value
- no dry-run request is produced

### Invalid Temperature

Run:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx --temperature 9
```

Expected result:

- the script rejects the value
- you learn that model settings need boundaries

### Free-Form Output

Run:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx --format text
```

Expected result:

- `response_format` changes to `text`
- the request becomes weaker for automated AOIS parsing

## Explanation Lab

Answer without looking at the answer key first:

1. what is a system prompt?
2. what is a user prompt?
3. what does `max_output_tokens` protect?
4. why is token estimation useful before a real provider call?
5. why is `json_object` safer for AOIS than free-form text?
6. which output field proves the script did not call a provider?
7. why should API keys not be introduced in this version?

## Defense Lab

Defend:

`A dry-run LLM request builder belongs before real OpenAI, Groq, or other provider integration.`

Your defense must mention:

- cost
- latency
- API keys
- data exposure
- structured output
- operational debugging

## Benchmark Lab

Record:

- repo disk footprint before and after this version
- whether the script compiled
- one default dry-run JSON output
- one output-budget comparison
- one free-form output comparison
- confirmation that no external provider was called
- confirmation that no persistent process was started
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.7 - LLM Fundamentals Without Provider Dependence](03-notes.md)
- Next: [v0.7 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
