# v3 Runbook

Authoring status: authored

## Purpose

Use this runbook when local evaluation fails, trace IDs are missing, or the eval endpoint behaves unexpectedly.

## Primary Checks

Compile:

```bash
python3 -m py_compile app/reliability.py examples/run_eval_baseline.py app/main.py
```

Run local eval:

```bash
python3 examples/run_eval_baseline.py
```

Run API eval only during lab:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
curl -sS http://127.0.0.1:8006/ai/eval/baseline
```

## Recovery Steps

If score is below `1.0`:

- inspect failed cases
- compare expected and actual category
- compare expected and actual severity
- inspect `app/analysis.py`

If trace ID is missing:

- inspect `new_trace_id`
- confirm API responses include trace fields

If provider call is true:

- stop immediately
- remove provider execution
- restore local baseline only

If uvicorn remains running:

- stop it
- confirm port `8006` is clear
