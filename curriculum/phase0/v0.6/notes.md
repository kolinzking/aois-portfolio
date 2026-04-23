# v0.6 - FastAPI Service Boundary Before AI

Estimated time: 3-4 focused hours

## What This Builds

You build the first working AOIS API service using:

- [app/main.py](../../../app/main.py)
- [app/analysis.py](../../../app/analysis.py)
- [app/models.py](../../../app/models.py)

## Why This Exists

Later AOIS versions will call models, route requests, trace latency, and store incident history.
All of that assumes there is a service boundary with:

- endpoints
- request validation
- response models

`v0.6` gives that boundary before any AI logic arrives.

## AOIS Connection

The system path becomes:

`HTTP request -> validated model -> regex analysis -> structured response`

This is the immediate ancestor of `v1`.

## Learning Goals

By the end of this version you should be able to:

- run `uvicorn app.main:app --reload`
- explain what `/health` and `/analyze` do
- explain how FastAPI uses the Pydantic models from `v0.5`
- explain why regex analysis is still brittle even though the API is now structured

## Prerequisites

Run:

```bash
sed -n '1,220p' app/main.py
sed -n '1,220p' app/analysis.py
```

## Core Concepts

### Route

An HTTP path plus method handled by the service.

### Request model

The validated shape of the incoming JSON.

### Response model

The typed structure returned to the caller.

### Regex analyzer

A deterministic interpreter that still lacks true reasoning.

## Build

Inspect the app:

```bash
sed -n '1,220p' app/main.py
sed -n '1,240p' app/analysis.py
```

Start the server:

```bash
uvicorn app.main:app --reload
```

## Ops Lab

With the server running, call it:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"log":"pod OOMKilled exit code 137"}'
```

Expected:

- `/health` returns status and app metadata
- `/analyze` returns structured JSON with summary, severity, suggestion, and source

## Break Lab

Send a bad body:

```bash
curl -s -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"log":"bad"}'
```

Expected:

- validation failure response

Lesson:

- the service boundary now rejects malformed requests before business logic runs

## Testing

Syntax check:

```bash
python3 -m py_compile app/main.py app/analysis.py
```

Logic smoke check:

```bash
python3 - <<'PY'
from app.analysis import analyze_log
print(analyze_log("gateway returned 503"))
PY
```

## Common Mistakes

### Confusing structured output with intelligent output

FastAPI and Pydantic make the response shape clean.
They do not make the interpretation smarter.

### Putting all logic directly in the route

Keep analysis separate from transport.

### Forgetting that rules are still narrow

The service is better structured, but it is still the same brittle idea underneath.

## Troubleshooting

If the server does not start:

```bash
python3 -m py_compile app/main.py app/analysis.py
```

If port 8000 is busy:

```bash
lsof -ti:8000 | xargs kill -9
```

## Benchmark

Measure a few local requests by eye:

```bash
for i in 1 2 3; do curl -s -o /dev/null -w "%{time_total}\n" http://127.0.0.1:8000/health; done
```

The point is to see that the local service boundary is cheap compared with later remote model calls.

## Architecture Defense

Why FastAPI here:

- natural Pydantic integration
- easy local iteration
- later AI service path can reuse the same boundary

Why not wait until `v1`:

- AI should land inside an understood service boundary, not create that boundary and intelligence at the same time

## 4-Layer Tool Drill

### FastAPI

1. Plain English
It turns AOIS into a web service.

2. System Role
It is the first real API boundary for the system.

3. Minimal Technical Definition
It is a Python ASGI web framework built around type-aware request and response handling.

4. Hands-on Proof
Without it, AOIS remains a set of local scripts instead of a callable service.

## 4-Level System Explanation Drill

1. Simple English
`v0.6` makes AOIS into a small API.

2. Practical Explanation
It exposes endpoints that accept a log and return a structured diagnosis.

3. Technical Explanation
It combines FastAPI routes with Pydantic models and a regex-based analysis module.

4. Engineer-Level Explanation
`v0.6` establishes the transport, validation, and response contract layer for AOIS while keeping the analysis implementation intentionally deterministic so the later AI upgrade is measurable.

## Failure Story

The representative failure is thinking the API is "smart" because the JSON looks clean.
It is not.
The logic is still brittle regex classification behind a better service boundary.

## Mastery Checkpoint

You are ready to leave `v0.6` when you can:

1. start the server
2. call both routes with `curl`
3. explain how validation works
4. explain why the service is cleaner than `v0.2` but still limited
5. defend why this version had to happen before AI

## Connection Forward

`v0.7` keeps the service boundary in mind but shows what a raw LLM call changes and what it still does not solve.
