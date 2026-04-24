# v2 - Model Routing Without Provider Execution

Estimated time: 8-12 focused hours

Authoring status: authored

Resource posture: route planning only, no external model call

## What This Builds

This version builds provider-neutral model routing:

- `app/model_router.py`
- `POST /ai/route`

The endpoint decides which route AOIS would use under cost, latency, severity, and provider-budget constraints.

It still does not call OpenAI, Groq, Anthropic, or any external model endpoint.

## Why This Exists

Real AI systems should not send every request to the same model.

AOIS needs to reason about:

- local fallback
- fast external route
- stronger external route
- severity
- latency budget
- cost budget
- whether provider budget was approved

This version teaches routing decisions before routing execution.

## AOIS Connection

The AOIS path is now:

`incident -> structured endpoint -> route decision -> fallback plan -> future provider execution`

`v1` made provider gating visible.
`v2` decides what route would be selected if provider execution is approved.

## Learning Goals

By the end of this version you should be able to:

- explain model routing
- explain fallback
- explain cost budget
- explain latency budget
- explain why high severity may justify a stronger route
- explain why provider budget approval still does not mean a provider call happened
- inspect route decisions over HTTP

## Resource Gate

Do not call external providers in this version.

Allowed:

- local Python compilation
- short-lived FastAPI runtime on `127.0.0.1`
- local `curl` requests

Not allowed without explicit approval:

- real provider SDKs
- provider API keys
- paid inference
- persistent runtime
- cloud resources

## Prerequisites

You should have completed:

- Phase 0
- `v1` structured AI endpoint

Required checks:

```bash
python3 -m py_compile app/model_router.py app/main.py
```

## Core Concepts

## Model Routing

Model routing chooses which analysis path should handle a request.

Routes in this version:

- `local-baseline`
- `fast-external-placeholder`
- `strong-external-placeholder`

## Fallback

A fallback is the route AOIS can use when the selected path is unavailable, too expensive, too slow, or not approved.

## Latency Budget

Latency budget is the maximum time the system can afford to wait.

Small budgets should avoid slow routes.

## Cost Budget

Cost budget is the maximum estimated spend for a request.

Small budgets should avoid expensive routes.

## Provider Budget Approval

`provider_budget_approved` lets the router consider external routes.

It does not make a provider call.
It only changes the decision plan.

## Build

Inspect:

```bash
sed -n '1,240p' app/model_router.py
sed -n '1,340p' app/main.py
```

Compile:

```bash
python3 -m py_compile app/model_router.py app/main.py
```

Run the API only for the lab:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

Default route:

```bash
curl -sS -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx after deploy"}'
```

Expected:

- selected route is `local-baseline`
- `provider_call_made=false`

Provider-budget-approved route plan:

```bash
curl -sS -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"pod OOMKilled exit code 137","provider_budget_approved":true,"latency_budget_ms":2000,"max_cost_usd":0.01}'
```

Expected:

- high severity can select `strong-external-placeholder`
- provider call still is not made

Stop the server after validation.

## Ops Lab

Run three route plans:

```bash
curl -sS -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx"}'

curl -sS -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"gateway returned 5xx","provider_budget_approved":true,"latency_budget_ms":600,"max_cost_usd":0.001}'

curl -sS -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"pod OOMKilled exit code 137","provider_budget_approved":true,"latency_budget_ms":2000,"max_cost_usd":0.01}'
```

Questions:

1. Which field shows the selected route?
2. Which field shows the fallback route?
3. Which field proves no provider call happened?
4. Which input allows external routes to be considered?
5. Why does high severity change the routing decision?

Answer key:

1. `selected_route`
2. `fallback_route`
3. `provider_call_made=false`
4. `provider_budget_approved=true`
5. high severity may justify higher latency and cost when budget allows

## Break Lab

Do not skip this.

### Option A - Provider Budget Not Approved

Run a high-severity request without provider budget:

```bash
curl -sS -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"pod OOMKilled exit code 137","latency_budget_ms":2000,"max_cost_usd":0.01}'
```

Expected:

- route stays `local-baseline`

Lesson:

- budget approval is a gate

### Option B - Budget Too Small

Run:

```bash
curl -sS -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"pod OOMKilled exit code 137","provider_budget_approved":true,"latency_budget_ms":100,"max_cost_usd":0.00001}'
```

Expected:

- route stays `local-baseline`

Lesson:

- approval alone is not enough if latency or cost budget is too small

## Testing

The version passes when:

1. Python files compile
2. `/ai/route` returns structured JSON
3. default route is local
4. approved high-severity route can select strong placeholder
5. provider call is never made
6. server is stopped after validation

## Common Mistakes

- treating route planning as route execution
- assuming provider approval removes cost limits
- ignoring fallback route
- routing low-severity incidents to expensive paths
- hiding latency and cost assumptions
- leaving the local server running

## Troubleshooting

If route is missing:

- inspect `app/main.py`
- restart uvicorn

If external route is never selected:

- check `provider_budget_approved`
- check `latency_budget_ms`
- check `max_cost_usd`
- check severity

If a provider call happens:

- stop immediately
- remove provider execution
- restore `provider_call_made=false`
- record the issue

## Benchmark

Measure:

- compile result
- default route response
- fast route response
- strong route response
- low-budget fallback response
- whether provider call remained false
- whether server was stopped

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can run, compare, break, explain, and defend routing decisions without provider execution. |
| 4/5 | Routing works, but one tradeoff needs review. |
| 3/5 | Endpoint works, but fallback or budget reasoning is weak. |
| 2/5 | Route JSON appears, but the decision is unclear. |
| 1/5 | Model routing still feels like picking a favorite model. |

Minimum pass: `4/5`.

## Architecture Defense

Why route before provider execution?

Because model use is an operational decision involving severity, cost, latency, approval, and fallback.

Why keep local baseline?

Because AOIS needs a safe path when external calls are blocked, too expensive, or too slow.

Why return the fallback route?

Because operators need to know what the system can do if the selected path fails.

## 4-Layer Tool Drill

Tool: model router

1. Plain English
It chooses the best analysis route for an incident.

2. System Role
It sits between structured AI request handling and future provider execution.

3. Minimal Technical Definition
It is logic that selects a route from operational constraints such as severity, latency budget, cost budget, and approval state.

4. Hands-on Proof
Changing budget and severity changes selected route while `provider_call_made` remains false.

## 4-Level System Explanation Drill

1. Simple English
AOIS can now decide which model path it would use.

2. Practical Explanation
I can call `/ai/route`, compare local, fast, and strong route plans, and explain the fallback.

3. Technical Explanation
`v2` adds `app/model_router.py` and `/ai/route`, returning route decisions from severity, latency, cost, and provider-budget constraints.

4. Engineer-Level Explanation
AOIS now separates model route selection from model execution, making cost, latency, severity, fallback, and approval state visible before any external inference call is possible.

## Failure Story

Representative failure:

- Symptom: every incident routes to the strongest external model
- Root cause: severity, cost, latency, and approval were ignored
- Fix: route through explicit constraints and keep local fallback
- Prevention: test low-budget and no-provider cases
- What this taught me: routing is policy, not enthusiasm

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v2` solve in AOIS?
2. What is model routing?
3. What is fallback?
4. What is latency budget?
5. What is cost budget?
6. What does `provider_budget_approved` do?
7. Why does route planning not mean provider execution?
8. Why keep `local-baseline`?
9. Why can high severity justify a stronger route?
10. Explain model router using the 4-layer tool rule.
11. Explain `v2` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v2` solve in AOIS?

It teaches AOIS how to choose an analysis route from severity, cost, latency, approval, and fallback constraints.

2. What is model routing?

Choosing which model or analysis path should handle a request.

3. What is fallback?

The backup route used if the selected path is unavailable, blocked, too slow, or too expensive.

4. What is latency budget?

The maximum acceptable wait time for the route.

5. What is cost budget?

The maximum acceptable estimated spend for the route.

6. What does `provider_budget_approved` do?

It lets the router consider external placeholders.
It does not make a provider call.

7. Why does route planning not mean provider execution?

Planning returns a decision.
Execution would contact a provider, use secrets, spend money, and create external dependency risk.

8. Why keep `local-baseline`?

It is safe, free, fast, and available when external providers are blocked.

9. Why can high severity justify a stronger route?

High-severity incidents may need better analysis when budget and latency allow it.

10. Explain model router using the 4-layer tool rule.

- Plain English: it chooses an analysis path.
- System Role: it connects structured AI requests to future provider execution.
- Minimal Technical Definition: it selects routes from severity, latency, cost, and approval constraints.
- Hands-on Proof: changing budgets changes route decisions while no provider call happens.

11. Explain `v2` using the 4-level system explanation rule.

- Simple English: AOIS can choose which model path it would use.
- Practical explanation: I can compare route decisions over HTTP.
- Technical explanation: `v2` adds a route planner and `/ai/route`.
- Engineer-level explanation: AOIS now has provider-neutral routing policy that exposes cost, latency, fallback, severity, and approval state before execution.

## Connection Forward

`v2` makes routing decisions visible.

`v3` will add reliability checks: validation, tracing, prompt iteration, and evaluation baseline.
