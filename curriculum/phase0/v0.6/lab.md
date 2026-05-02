# v0.6 Lab

Authoring status: authored

## Build Lab

Build `app/main.py` as shown in `notes.md`.

Do not install runtime dependencies until the resource gate is approved.

After approval, install:

```bash
python3 -m venv .venv
.venv/bin/pip install --no-cache-dir -r requirements.txt
```

Run the server only for the lab:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

Success state:

- `/health` returns `status=ok`
- `/analyze` returns structured analysis
- the server is stopped after practice

## Ops Lab

Run:

```bash
curl -i http://127.0.0.1:8006/health
curl -i -X POST http://127.0.0.1:8006/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx after deploy"}'
```

Expected learning:

- `curl` from `v0.4` now inspects your own API
- Python logic from `v0.5` now sits behind HTTP
- structured input produces structured output

## Break Lab

Send invalid JSON shape:

```bash
curl -i -X POST http://127.0.0.1:8006/analyze \
  -H "Content-Type: application/json" \
  -d '{"source":"lab"}'
```

Expected result:

- validation error
- no fake analysis

Stop the server and run:

```bash
curl -i http://127.0.0.1:8006/health
```

Expected result:

- connection failure

## Explanation Lab

Answer:

1. what is a route?
2. what is a request model?
3. what is a response model?
4. why does validation matter?
5. why is AI absent in this version?

## Defense Lab

Defend:

`FastAPI before AI is the right order for AOIS.`

## Benchmark Lab

Record:

- disk before install
- disk after install if approved
- health response
- analyze response
- validation failure
- confirmation that server was stopped
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.6 - FastAPI Without AI](notes.md)
- Next: [v0.6 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
