# v1 Lab

Authoring status: authored

## Build Lab

Inspect:

```bash
sed -n '1,220p' app/ai_contract.py
sed -n '1,280p' app/main.py
```

Compile:

```bash
python3 -m py_compile app/ai_contract.py app/main.py
```

Run only for the lab:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

Success state:

- `/health` still works
- `/analyze` still works
- `/ai/analyze` returns structured JSON
- `provider_call_made` is `false`
- server is stopped after validation

## Ops Lab

Call:

```bash
curl -sS -X POST http://127.0.0.1:8006/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx after deploy","source":"lab"}'
```

Expected learning:

- the route is AI-shaped
- the response is structured
- the deterministic analyzer still provides the baseline
- provider execution is explicitly absent

## Break Lab

Force provider execution:

```bash
curl -i -X POST http://127.0.0.1:8006/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx","allow_provider_call":true}'
```

Expected result:

- `403`
- no provider call

Send invalid input:

```bash
curl -i -X POST http://127.0.0.1:8006/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"source":"lab"}'
```

Expected result:

- validation error

## Explanation Lab

Answer:

1. what is the route?
2. what fields make the response structured?
3. why is `provider_call_made` important?
4. why does forced provider use return `403`?
5. why does deterministic analysis remain?

## Defense Lab

Defend:

`The correct first AI endpoint is a structured, provider-gated endpoint, not a blind provider call.`

Your defense must mention:

- cost
- secrets
- latency
- data exposure
- structured output
- deterministic fallback

## Benchmark Lab

Record:

- compile result
- successful `/ai/analyze` response
- provider-forcing `403`
- invalid input validation error
- server stopped confirmation
- resource footprint after the checkpoint
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v1 - Structured AI Endpoint Without Provider Calls](03-notes.md)
- Next: [v1 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
