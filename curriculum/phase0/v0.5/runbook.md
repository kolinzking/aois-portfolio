# v0.5 Runbook

Authoring status: authored

## Purpose

Use this runbook when the Python analyzer fails to run or returns confusing output.

## Primary Checks

Run from the repo root:

```bash
pwd
python3 --version
python3 -m py_compile app/models.py app/analysis.py app/config.py examples/analyze_incident.py
```

Then run:

```bash
python3 examples/analyze_incident.py "gateway returned 5xx"
```

## Recovery Steps

If imports fail:

1. confirm you are in the repo root
2. confirm `app/__init__.py` exists
3. run the script as `python3 examples/analyze_incident.py "..."`

If compilation fails:

1. read the file path and line number
2. fix the syntax error
3. rerun `python3 -m py_compile ...`

If empty input fails:

- that is expected
- pass a non-empty incident message

If the category is `unknown`:

- inspect the message wording
- inspect `app/analysis.py`
- preserve the raw signal rather than pretending the message is safe
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.5 Lab](lab.md)
- Next: [v0.5 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
