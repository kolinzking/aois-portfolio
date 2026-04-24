# v2 Runbook

Authoring status: authored

## Purpose

Use this runbook when `/ai/route` does not return the expected route or when route planning is confused with provider execution.

## Primary Checks

Compile:

```bash
python3 -m py_compile app/model_router.py app/main.py
```

Run server:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

Call default route:

```bash
curl -i -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx"}'
```

## Recovery Steps

If route is local when you expected external:

- confirm `provider_budget_approved=true`
- confirm `latency_budget_ms` is high enough
- confirm `max_cost_usd` is high enough
- confirm severity is high enough for strong route

If provider call is true:

- stop immediately
- remove provider execution
- restore route planning only

If the server was left running:

- stop uvicorn
- confirm port `8006` is no longer listening

If dependencies are missing:

- do not install globally
- use `.venv`
- request approval before reinstalling
