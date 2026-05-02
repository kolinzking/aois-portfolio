# v0.5 Lab

Authoring status: authored

## Build Lab

Build the Python AOIS foundation files:

- `app/models.py`
- `app/analysis.py`
- `app/config.py`
- `examples/analyze_incident.py`

Compile them:

```bash
python3 -m py_compile app/models.py app/analysis.py app/config.py examples/analyze_incident.py
```

Run examples:

```bash
python3 examples/analyze_incident.py "gateway returned 5xx after deploy"
python3 examples/analyze_incident.py "pod OOMKilled exit code 137"
python3 examples/analyze_incident.py "strange message with no match"
```

Success state:

- Python files compile
- known messages produce structured categories
- unknown messages remain `unknown`

## Ops Lab

Run:

```bash
python3 examples/analyze_incident.py "permission denied reading /var/log/app.log"
python3 examples/analyze_incident.py "pod CrashLoopBackOff restarting"
```

Expected learning:

- Python is now AOIS's application logic layer
- `app/models.py` defines structured data
- `app/analysis.py` defines behavior
- the CLI is just one way to use the logic

## Break Lab

Trigger invalid input:

```bash
python3 examples/analyze_incident.py ""
```

Expected result:

- `ValueError`
- the error should say the incident message must not be empty

Trigger an unknown classification:

```bash
python3 examples/analyze_incident.py "the system feels odd"
```

Expected result:

- `category=unknown`
- `severity=unknown`

Explain:

- invalid input should fail clearly
- unknown input should be preserved honestly

## Explanation Lab

Answer:

1. what is a module?
2. what is a function?
3. what is a dataclass?
4. what is an enum?
5. why does AOIS need structured results?

## Defense Lab

Defend:

`Python is the right next step after Bash for AOIS application logic.`

## Benchmark Lab

Score yourself from `1` to `5`:

- `5`: I can run, explain, break, and extend the Python layer without hints.
- `4`: I can complete the lab but one concept needs review.
- `3`: I can run examples but struggle to explain structure.
- `2`: code runs, but models/functions/exceptions are unclear.
- `1`: Python still feels like copied text.

Minimum pass: `4`.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.5 - Python Core For AOIS Logic](03-notes.md)
- Next: [v0.5 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
