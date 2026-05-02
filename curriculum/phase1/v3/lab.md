# v3 Lab

Authoring status: authored

## Build Lab

Inspect:

```bash
sed -n '1,260p' app/reliability.py
sed -n '1,120p' examples/run_eval_baseline.py
```

Compile:

```bash
python3 -m py_compile app/reliability.py examples/run_eval_baseline.py app/main.py
```

Run:

```bash
python3 examples/run_eval_baseline.py
```

Success state:

- score is `1.0`
- `provider_call_made` is `false`
- `trace_id` is present
- all cases pass

## Ops Lab

Run the API briefly:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
curl -sS http://127.0.0.1:8006/ai/eval/baseline
```

Expected learning:

- eval can run through the service boundary
- reliability output is structured
- provider calls remain absent
- server must be stopped after validation

## Break Lab

Think through this regression:

If `app/analysis.py` stops matching `OOMKilled`, the `memory_pressure` eval case fails.

Expected result:

- `passed_cases` decreases
- `score` falls below `1.0`

Do not intentionally break committed source unless you are practicing in a scratch copy.

## Explanation Lab

Answer:

1. what is a trace ID?
2. what is an eval case?
3. what is a baseline?
4. what is a regression?
5. why does provider-call status appear in eval output?

## Defense Lab

Defend:

`A reliability baseline belongs before real provider integration.`

Your defense must mention:

- regression detection
- traceability
- provider-call visibility
- repeatability
- future model comparison

## Benchmark Lab

Record:

- compile result
- local eval score
- API eval response
- provider-call status
- server stopped confirmation
- resource footprint
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v3 - Reliability Baseline Without Provider Calls](notes.md)
- Next: [v3 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
