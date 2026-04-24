# v1 Runbook

Authoring status: authored

## Purpose

Use this runbook when `/ai/analyze` fails, provider gating is unclear, or the local API runtime behaves unexpectedly.

## Primary Checks

Compile:

```bash
python3 -m py_compile app/ai_contract.py app/main.py
```

Run server:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

Call the endpoint:

```bash
curl -i -X POST http://127.0.0.1:8006/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx after deploy"}'
```

Check provider gate:

```bash
curl -i -X POST http://127.0.0.1:8006/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx","allow_provider_call":true}'
```

## Recovery Steps

If the route is missing:

- inspect `app/main.py`
- confirm `/ai/analyze` exists
- confirm the server restarted after code changes

If the response is free-form text:

- restore `AIAnalyzeResponse`
- restore structured fields
- rerun the endpoint

If provider forcing does not return `403`:

- restore the `allow_provider_call` guard
- do not continue to `v2`

If dependencies are missing:

- do not install globally
- use the existing `.venv`
- request approval before reinstalling

If the server is still running after the lab:

- stop it with `Ctrl-C`
- confirm no persistent portfolio runtime remains active
