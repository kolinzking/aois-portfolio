# v0.6 - FastAPI Without AI

Estimated time: 8-12 focused hours

Authoring status: authored

Resource posture: install-gated, short-lived local server only

## What This Builds

This version wraps the Python analyzer from `v0.5` in a FastAPI service.

You will build:

- `GET /health`
- `POST /analyze`
- request validation
- response models
- terminal inspection with `curl`

This is still not an AI service.
It is a deterministic API that prepares AOIS for AI integration later.

## Why This Exists

AOIS needs a service boundary before it needs AI.

A service boundary lets another system send an incident signal and receive structured output.

FastAPI is introduced here because it teaches:

- route design
- request bodies
- response bodies
- validation failure
- OpenAPI documentation
- local service runtime
- HTTP inspection with tools from `v0.4`

## AOIS Connection

The AOIS path is now:

`signal -> HTTP request -> FastAPI route -> Python analysis -> structured HTTP response`

`v0.5` built the Python logic.
`v0.6` exposes it as an API.
`v1` will later replace or augment deterministic analysis with real AI-backed structured output.

## Learning Goals

By the end of this version you should be able to:

- explain what FastAPI adds beyond plain Python functions
- run a local API server
- inspect `/health` with `curl`
- send JSON to `/analyze`
- explain request and response models
- trigger and interpret validation failure
- explain why AI is intentionally not added yet
- stop the server after validation

## Resource Gate

Do not install dependencies until approved.

Expected impact if approved:

- disk: about `40-100 MB` with a local virtual environment and `--no-cache-dir`
- RAM: about `50-150 MB` while the local server runs
- runtime: short-lived only
- binding: `127.0.0.1` only

Do not run this service persistently on the shared server.

## Prerequisites

You should have completed:

- `v0.1` Linux inspection
- `v0.2` Bash automation
- `v0.3` Git discipline
- `v0.4` HTTP inspection
- `v0.5` Python logic

Required before runtime:

```bash
python3 --version
python3 -m py_compile app/models.py app/analysis.py app/config.py examples/analyze_incident.py
```

Required only after install approval:

```bash
python3 -m venv .venv
.venv/bin/pip install --no-cache-dir -r requirements.txt
```

## Core Concepts

## API

An API is a boundary where other systems can send requests and receive responses.

In this version, AOIS exposes:

- `/health` for basic service status
- `/analyze` for deterministic incident analysis

## Route

A route maps an HTTP method and path to Python behavior.

Examples:

- `GET /health`
- `POST /analyze`

## Request Model

A request model defines what input the API accepts.

In `app/main.py`, `AnalyzeRequest` requires:

- `message`
- optional `source`

## Response Model

A response model defines what output the API promises.

`AnalyzeResponse` returns:

- category
- severity
- confidence
- summary
- recommended action

## Validation

Validation rejects bad input before it reaches business logic.

If the request body is missing `message`, FastAPI should return a validation error instead of pretending analysis succeeded.

## Build

Create or replace `app/main.py` with the FastAPI app in the repository.

Install only after approval:

```bash
python3 -m venv .venv
.venv/bin/pip install --no-cache-dir -r requirements.txt
```

Run the server only for the lab:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

In another terminal:

```bash
curl -sS http://127.0.0.1:8006/health
```

Expected output:

```json
{"status":"ok","environment":"local"}
```

Analyze an incident:

```bash
curl -sS -X POST http://127.0.0.1:8006/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx after deploy","source":"lab"}'
```

Expected output shape:

```json
{
  "category": "service-error",
  "severity": "medium",
  "confidence": 0.7,
  "summary": "...",
  "recommended_action": "..."
}
```

Stop the server with `Ctrl-C` after the lab.

## Ops Lab

Run while the server is active:

```bash
curl -i http://127.0.0.1:8006/health
curl -i -X POST http://127.0.0.1:8006/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"pod OOMKilled exit code 137"}'
```

Questions:

1. Which route proves the service is alive?
2. Which route uses the Python analyzer from `v0.5`?
3. Which status code means the request succeeded?
4. Where is the request body?
5. Where is the response body?

Answer key:

1. `GET /health`
2. `POST /analyze`
3. `200`
4. The JSON after `-d`
5. The JSON returned by the server

## Break Lab

Do not skip this.

### Option A - Missing field

Run:

```bash
curl -i -X POST http://127.0.0.1:8006/analyze \
  -H "Content-Type: application/json" \
  -d '{"source":"lab"}'
```

Expected symptom:

- validation error
- no fake analysis result

Lesson:

- request validation protects the analysis layer

False conclusion this prevents:

- "the analyzer can handle any request shape"

### Option B - Server stopped

Stop the server and run:

```bash
curl -i http://127.0.0.1:8006/health
```

Expected symptom:

- connection failure

Lesson:

- this is different from API validation failure

False conclusion this prevents:

- "the API returned an error" when no server answered

## Testing

The version passes when:

1. the app imports after dependencies are installed
2. `/health` returns status `ok`
3. `/analyze` returns structured analysis for a valid message
4. invalid request body returns validation failure
5. the server is stopped after the lab
6. you can explain why AI is still absent

## Common Mistakes

- adding AI before the API contract is clear
- leaving the server running
- binding to `0.0.0.0` instead of `127.0.0.1` during local practice
- confusing validation failure with analyzer failure
- skipping `curl` because browser docs are available
- installing dependencies without tracking disk impact

## Troubleshooting

If `app.main` raises a dependency error:

- FastAPI has not been installed yet
- complete the approved install gate

If `curl` cannot connect:

- confirm `uvicorn` is running
- confirm host is `127.0.0.1`
- confirm port is `8006`

If validation fails:

- inspect the JSON body
- confirm `message` is present and non-empty

If server is still running after the lab:

- stop it with `Ctrl-C`
- confirm no persistent `uvicorn` was left for AOIS portfolio work

## Benchmark

Measure:

- disk footprint before install
- disk footprint after install if approved
- can `/health` respond?
- can `/analyze` classify a known incident?
- can invalid input fail clearly?
- was the server stopped afterward?

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can install, run, inspect, break, explain, and stop the API safely. |
| 4/5 | The API works, but one concept needs review. |
| 3/5 | The API runs, but validation or HTTP inspection needs help. |
| 2/5 | The server starts, but the route behavior is unclear. |
| 1/5 | FastAPI feels like magic. |

Minimum pass: `4/5`.

## Architecture Defense

Why FastAPI before AI?

Because AI behavior needs a stable service contract.
Without request and response structure, AI integration becomes a demo instead of an operable system.

Why bind to `127.0.0.1`?

Because this is local practice on a shared server.
There is no reason to expose the lab service publicly.

Why stop the server?

Because the primary AOIS workload takes priority and this portfolio service is not meant to consume runtime resources.

## 4-Layer Tool Drill

Tool: FastAPI

1. Plain English
FastAPI turns Python functions into HTTP API endpoints.

2. System Role
It exposes AOIS analysis logic as a service boundary.

3. Minimal Technical Definition
FastAPI is a Python web framework built around ASGI, type hints, validation, routing, and OpenAPI generation.

4. Hands-on Proof
If FastAPI is not running, `curl` cannot reach `/health`; if request validation fails, bad input is rejected before analysis.

## 4-Level System Explanation Drill

1. Simple English
I turned AOIS Python logic into a local API.

2. Practical Explanation
I can run a local server, call `/health`, send incident JSON to `/analyze`, and inspect validation errors with `curl`.

3. Technical Explanation
This version uses FastAPI routes, Pydantic request/response models, and uvicorn to expose deterministic Python analysis over HTTP.

4. Engineer-Level Explanation
AOIS now has an API contract layer: incident signals can cross an HTTP boundary, be validated, routed into deterministic domain logic, and returned as structured responses before introducing AI providers, persistence, auth, or deployment.

## Failure Story

Representative failure:

- Symptom: `POST /analyze` returned validation error
- Root cause: request body omitted required `message`
- Fix: send a valid JSON body with `message`
- Prevention: keep request models explicit and inspect failed requests with `curl -i`
- What this taught me: API boundaries should reject malformed input before business logic runs

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v0.6` solve in AOIS?
2. What is an API route?
3. What is a request model?
4. What is a response model?
5. Why does validation matter?
6. Why is AI intentionally absent?
7. Why bind to `127.0.0.1`?
8. Why must the server be stopped after practice?
9. How does this build on `v0.4` and `v0.5`?
10. Explain FastAPI using the 4-layer tool rule.
11. Explain `v0.6` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v0.6` solve in AOIS?

It turns AOIS Python logic into an HTTP API so other systems can send incident signals and receive structured analysis.

2. What is an API route?

A route maps an HTTP method and path to behavior, such as `GET /health` or `POST /analyze`.

3. What is a request model?

A request model defines the expected input shape.
In this version, `AnalyzeRequest` defines the JSON body accepted by `/analyze`.

4. What is a response model?

A response model defines the output shape the API promises.
`AnalyzeResponse` defines the structured fields returned by AOIS.

5. Why does validation matter?

Validation rejects malformed input before business logic runs.
That prevents fake analysis, hidden errors, and ambiguous behavior.

6. Why is AI intentionally absent?

The API contract must be clear before AI is added.
AI integration without stable request/response boundaries is hard to test, observe, and operate.

7. Why bind to `127.0.0.1`?

This is local practice on a shared server.
Binding locally avoids exposing the lab API publicly.

8. Why must the server be stopped after practice?

AOIS portfolio is secondary work on a resource-constrained server.
Stopping the server prevents unnecessary CPU/RAM use and avoids interfering with the primary AOIS workload.

9. How does this build on `v0.4` and `v0.5`?

`v0.4` taught HTTP inspection with `curl`.
`v0.5` built Python analysis logic.
`v0.6` combines them by exposing the Python logic over HTTP.

10. Explain FastAPI using the 4-layer tool rule.

- Plain English: FastAPI turns Python functions into web API endpoints.
- System Role: it exposes AOIS analysis through an HTTP service boundary.
- Minimal Technical Definition: it is an ASGI Python web framework with routing, validation, type-hint integration, and OpenAPI support.
- Hands-on Proof: `/health` works only when the server is running, and bad `/analyze` input is rejected before analysis.

11. Explain `v0.6` using the 4-level system explanation rule.

- Simple English: I made AOIS callable over HTTP.
- Practical explanation: I can start the API, call health, post incident JSON, and inspect validation errors.
- Technical explanation: `v0.6` uses FastAPI, Pydantic models, uvicorn, and the Python analyzer from `v0.5`.
- Engineer-level explanation: AOIS now has a local API contract layer that validates incident signals, routes them into deterministic analysis, and returns structured responses, preparing the system for AI integration, persistence, auth, deployment, and observability.

## Connection Forward

`v0.6` teaches the sixth AOIS habit:

`expose logic through a contract`

`v0.7` introduces LLM fundamentals so AOIS can begin using model calls behind a contract instead of raw prompt experiments.

## Source Notes

FastAPI and Pydantic behavior can change over time.
Before runtime teaching, check official FastAPI documentation:

- <https://fastapi.tiangolo.com/>

This authoring pass did not install or run FastAPI because runtime practice is gated by the shared-server resource policy.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.6 Introduction](02-introduction.md)
- Next: [v0.6 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
