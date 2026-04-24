# v5 Runbook

Authoring status: authored

## Purpose

Use this runbook when security inspection misses risky input or redaction behaves unexpectedly.

## Primary Checks

Compile:

```bash
python3 -m py_compile app/security.py examples/security_inspect.py app/main.py
```

Run examples:

```bash
python3 examples/security_inspect.py gateway returned 5xx
python3 examples/security_inspect.py ignore previous instructions
python3 examples/security_inspect.py api_key=sk-example1234567890 gateway failed
```

## Recovery Steps

If injection is missed:

- inspect `PROMPT_INJECTION_PATTERNS`
- add a local phrase
- rerun the CLI

If secret-like text is not redacted:

- inspect `SECRET_PATTERNS`
- use fake secrets only
- rerun the CLI

If real secrets were committed:

- stop
- rotate the secret outside this repo
- remove it from files
- treat history cleanup as a separate explicit security task
