# v0.6 Runbook

## Purpose

Use this when the Phase 0 FastAPI service is not behaving as expected.

## Primary Checks

```bash
python3 -m py_compile app/main.py app/analysis.py
uvicorn app.main:app --reload
curl -s http://127.0.0.1:8000/health
```

## Recovery Steps

If import errors appear:

- inspect `app/__init__.py`
- run from the repo root

If requests fail:

- confirm the server is running
- inspect port `8000`
- re-send with `curl`
