# v1 - Structured AI Endpoint Without Provider Calls

Estimated time: 8-12 focused hours

Authoring status: authored

Resource posture: existing FastAPI runtime only, no external AI provider call

## What This Builds

This version builds the first Phase 1 intelligence endpoint:

```text
POST /ai/analyze
```

It returns a structured AI-shaped response while explicitly blocking real provider execution.

Code added:

- `app/ai_contract.py`
- `/ai/analyze` in `app/main.py`

The endpoint teaches:

- structured AI response contracts
- provider gating
- prompt contract design
- deterministic baseline fallback
- HTTP inspection of an AI-shaped service
- why "AI endpoint" and "provider call" are not the same thing

## Why This Exists

AOIS needs structured intelligence, not impressive paragraphs.

Before calling OpenAI, Groq, or another provider, the service must define:

- accepted request shape
- required response fields
- what happens when provider calls are not approved
- how deterministic analysis remains available as a baseline
- how an operator proves no external call happened

This protects cost, secrets, data exposure, and server reliability.

## AOIS Connection

The AOIS path is now:

`incident -> FastAPI -> structured AI contract -> deterministic baseline -> provider gate`

`v0.7` planned a model request.
`v1` exposes that idea as a real API route while keeping provider execution blocked.

## Learning Goals

By the end of this version you should be able to:

- explain structured output
- explain provider gating
- explain why deterministic baseline still matters
- inspect an AI-shaped endpoint over HTTP
- trigger the provider-call block on purpose
- explain why a future provider call needs budget and key controls
- explain `v1` using the 4-level system explanation rule

## Resource Gate

Do not call an external AI provider in this version.

Allowed by default:

- local Python compilation
- short-lived FastAPI run on `127.0.0.1`
- local `curl` requests

Not allowed without explicit approval:

- OpenAI API call
- Groq API call
- Anthropic API call
- any external model endpoint
- adding secrets
- persistent service runtime

## Prerequisites

You should have completed Phase 0.

Required local checks:

```bash
python3 -m py_compile app/ai_contract.py app/main.py
python3 examples/raw_llm_request.py gateway returned 5xx after deploy
```

Runtime check requires the existing `.venv` from `v0.6`.
Do not reinstall dependencies unless required and approved.

## Core Concepts

## Structured Output

Structured output means the response has stable fields the system can parse.

`v1` requires:

- category
- severity
- confidence
- summary
- recommended_action
- reasoning
- provider_mode
- provider_call_made
- prompt_contract

## Provider Gate

A provider gate blocks external AI calls unless approval exists.

In `v1`, this request is rejected:

```json
{"message":"gateway returned 5xx","allow_provider_call":true}
```

Expected result: `403`.

## Deterministic Baseline

The deterministic analyzer from `v0.5` still runs.

It gives AOIS a baseline result even when external AI is disabled.

## Prompt Contract

A prompt contract describes what a future provider request must contain and return.

It is not a provider call.
It is the service's promise about request intent and response shape.

## Build

Inspect:

```bash
sed -n '1,220p' app/ai_contract.py
sed -n '1,260p' app/main.py
```

Compile:

```bash
python3 -m py_compile app/ai_contract.py app/main.py
```

Run the API only for the lab:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

Call the structured endpoint:

```bash
curl -sS -X POST http://127.0.0.1:8006/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx after deploy","source":"lab"}'
```

Expected output includes:

```json
{
  "provider_mode": "dry_run_structured_contract",
  "provider_call_made": false
}
```

Stop the server after the lab.

## Ops Lab

Run while the server is active:

```bash
curl -i -X POST http://127.0.0.1:8006/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"pod OOMKilled exit code 137","source":"lab"}'
```

Questions:

1. Which route is the Phase 1 structured endpoint?
2. Which field proves no provider call happened?
3. Which field names the provider mode?
4. Which object shows the future prompt contract?
5. Which Phase 0 analyzer is still used as a baseline?

Answer key:

1. `POST /ai/analyze`
2. `provider_call_made=false`
3. `provider_mode`
4. `prompt_contract`
5. the deterministic analyzer from `app/analysis.py`

## Break Lab

Do not skip this.

### Option A - Try To Force Provider Use

Run:

```bash
curl -i -X POST http://127.0.0.1:8006/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx","allow_provider_call":true}'
```

Expected symptom:

- HTTP `403`
- no external provider call

Lesson:

- provider approval is an operational boundary

### Option B - Missing Message

Run:

```bash
curl -i -X POST http://127.0.0.1:8006/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"source":"lab"}'
```

Expected symptom:

- validation error

Lesson:

- structured input protects structured output

## Testing

The version passes when:

1. Python files compile
2. `/ai/analyze` returns structured JSON
3. `provider_call_made` is `false`
4. provider-forcing request returns `403`
5. invalid input fails validation
6. the server is stopped after validation
7. no external AI provider is called

## Common Mistakes

- calling a real provider before the response contract is stable
- treating `allow_provider_call` as a casual flag
- hiding provider behavior from the response
- accepting free-form AI paragraphs instead of stable fields
- removing deterministic baseline too early
- leaving the local server running on the shared machine

## Troubleshooting

If imports fail:

```bash
python3 -m py_compile app/ai_contract.py app/main.py
```

If `curl` cannot connect:

- confirm uvicorn is running
- confirm host is `127.0.0.1`
- confirm port is `8006`

If provider forcing does not return `403`:

- inspect `/ai/analyze`
- restore the `allow_provider_call` guard
- do not proceed until the gate works

If you want real provider integration:

- stop
- choose provider
- define request budget
- define key storage
- define logging and redaction
- get explicit approval

## Benchmark

Measure:

- compile result
- `/ai/analyze` success response
- provider-forcing `403` response
- invalid input validation response
- whether `provider_call_made=false`
- whether server was stopped
- repo disk footprint after checkpoint

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can run, inspect, break, explain, and defend the structured AI endpoint without provider calls. |
| 4/5 | Endpoint works, but one concept needs review. |
| 3/5 | Route works, but provider gating or structured output is unclear. |
| 2/5 | Server runs, but AI boundary is confused. |
| 1/5 | AI endpoint still means "just call a model" in your mind. |

Minimum pass: `4/5`.

## Architecture Defense

Why structured endpoint before provider integration?

Because the service contract should be stable before cost, secrets, latency, and external dependencies are introduced.

Why keep the deterministic baseline?

Because it gives AOIS a known fallback and a comparison point for later AI behavior.

Why return provider metadata?

Because operators must be able to prove whether external AI was used.

## 4-Layer Tool Drill

Tool: structured AI endpoint

1. Plain English
It accepts an incident and returns parseable intelligence fields.

2. System Role
It is AOIS's first intelligence service boundary.

3. Minimal Technical Definition
It is a FastAPI route that validates input, applies a structured response model, and blocks external provider execution unless approved.

4. Hands-on Proof
Calling `/ai/analyze` returns structured JSON; setting `allow_provider_call=true` returns `403`.

## 4-Level System Explanation Drill

1. Simple English
AOIS can now return AI-shaped analysis without calling an AI provider.

2. Practical Explanation
I can run the endpoint, inspect structured fields, and prove the provider call was blocked.

3. Technical Explanation
`v1` adds `app/ai_contract.py` and `/ai/analyze`, wrapping deterministic analysis in a provider-gated structured response contract.

4. Engineer-Level Explanation
AOIS now separates intelligence contract design from provider execution, preserving a deterministic baseline while making cost, secrets, latency, and external dependency risk explicit.

## Failure Story

Representative failure:

- Symptom: a developer sets `allow_provider_call=true` and expects the service to call an external model
- Root cause: provider approval, budget, and key handling were not defined
- Fix: return `403` and keep provider execution disabled
- Prevention: make provider gating visible in request, response, docs, and tests
- What this taught me: AI provider execution is an operational event, not a hidden implementation detail

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v1` solve in AOIS?
2. What is structured output?
3. What is a provider gate?
4. Why does `v1` not call OpenAI or Groq?
5. What does `provider_call_made=false` prove?
6. Why keep deterministic analysis?
7. What is a prompt contract?
8. Why should provider forcing return `403`?
9. Why is free-form text not enough for AOIS?
10. Explain structured AI endpoint using the 4-layer tool rule.
11. Explain `v1` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v1` solve in AOIS?

It creates the first structured intelligence API boundary while keeping real provider calls blocked.

2. What is structured output?

Output with stable fields that code can parse and validate.

3. What is a provider gate?

A control that prevents external AI calls unless approval, budget, key handling, and limits exist.

4. Why does `v1` not call OpenAI or Groq?

Because external AI calls involve cost, secrets, data exposure, latency, and approval.

5. What does `provider_call_made=false` prove?

It proves this response came from the local dry-run structured contract path, not an external provider.

6. Why keep deterministic analysis?

It provides a known baseline and fallback for comparison before AI behavior is introduced.

7. What is a prompt contract?

A structured description of the system prompt, user prompt, required fields, and response format expected from future provider calls.

8. Why should provider forcing return `403`?

Because the request is forbidden until provider execution is explicitly approved.

9. Why is free-form text not enough for AOIS?

AOIS needs parseable, auditable fields for automation and debugging.

10. Explain structured AI endpoint using the 4-layer tool rule.

- Plain English: it returns incident intelligence in predictable fields.
- System Role: it is AOIS's first intelligence API boundary.
- Minimal Technical Definition: it is a FastAPI route with validated request/response models and provider gating.
- Hands-on Proof: normal calls return structured JSON, but forced provider calls return `403`.

11. Explain `v1` using the 4-level system explanation rule.

- Simple English: AOIS can return AI-shaped answers safely.
- Practical explanation: I can call `/ai/analyze` and prove no provider was used.
- Technical explanation: `v1` wraps deterministic analysis in a structured contract response.
- Engineer-level explanation: `v1` separates AI service contract from external inference execution so cost, secrets, latency, data exposure, and reliability risks stay controlled.

## Connection Forward

`v1` creates the structured intelligence boundary.

`v2` will decide how model routing, fallback, latency, and cost choices should work once provider integration is approved.
