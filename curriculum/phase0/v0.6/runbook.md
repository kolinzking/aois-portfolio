# v0.6 Runbook

Authoring status: authored

## Purpose

Use this runbook when the FastAPI service will not start or HTTP requests fail.

## Primary Checks

Before runtime:

```bash
du -sh .
python3 --version
python3 -m py_compile app/models.py app/analysis.py app/config.py examples/analyze_incident.py
```

After approved install:

```bash
.venv/bin/python -c "import fastapi, uvicorn; print('fastapi runtime ok')"
```

Run server:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

## Recovery Steps

If dependencies are missing:

- do not keep retrying
- confirm install was approved
- install in `.venv` only

If `curl` cannot connect:

- confirm uvicorn is running
- confirm host is `127.0.0.1`
- confirm port is `8006`

If validation fails:

- inspect JSON
- confirm `message` is present and non-empty

If the server was left running:

- stop it with `Ctrl-C`
- confirm no AOIS portfolio runtime should remain active
