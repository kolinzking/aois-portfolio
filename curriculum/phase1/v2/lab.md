# v2 Lab

Authoring status: authored

## Build Lab

Inspect:

```bash
sed -n '1,260p' app/model_router.py
```

Compile:

```bash
python3 -m py_compile app/model_router.py app/main.py
```

Run only for the lab:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

Success state:

- `/ai/route` returns selected and fallback routes
- no provider call happens
- server is stopped after validation

## Ops Lab

Compare:

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

Expected learning:

- no budget approval means local route
- enough budget allows fast placeholder
- high severity plus enough budget allows strong placeholder
- route decision is not provider execution

## Break Lab

Use a high-severity incident but remove approval:

```bash
curl -sS -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"pod OOMKilled exit code 137","latency_budget_ms":2000,"max_cost_usd":0.01}'
```

Expected:

- selected route remains `local-baseline`

Use approval but too little budget:

```bash
curl -sS -X POST http://127.0.0.1:8006/ai/route \
  -H "Content-Type: application/json" \
  -d '{"message":"pod OOMKilled exit code 137","provider_budget_approved":true,"latency_budget_ms":100,"max_cost_usd":0.00001}'
```

Expected:

- selected route remains `local-baseline`

## Explanation Lab

Answer:

1. what is model routing?
2. what is fallback?
3. what does `provider_budget_approved` change?
4. why does `provider_call_made` remain false?
5. why should high severity affect route choice?

## Defense Lab

Defend:

`Route planning must be separate from provider execution.`

Your defense must mention:

- cost
- latency
- severity
- fallback
- approval
- observability

## Benchmark Lab

Record:

- compile result
- default local route
- fast placeholder route
- strong placeholder route
- low-budget fallback route
- confirmation that provider calls were not made
- server stopped confirmation
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v2 - Model Routing Without Provider Execution](notes.md)
- Next: [v2 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
