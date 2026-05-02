# v3 - Reliability Baseline Without Provider Calls

Estimated time: 8-12 focused hours

Authoring status: authored

Resource posture: local evaluation and short-lived API validation only

## What This Builds

This version builds the first AOIS reliability layer:

- `app/reliability.py`
- `examples/run_eval_baseline.py`
- `GET /ai/eval/baseline`
- `trace_id` fields on AI-shaped responses

It teaches:

- trace IDs
- local evaluation cases
- baseline scoring
- regression awareness
- provider-call visibility
- why reliability must come before real AI scale

## Why This Exists

AI systems fail silently when there is no baseline.

Before adding real providers, AOIS needs to know:

- what current behavior is expected
- how to score simple known cases
- how to identify regressions
- how to correlate outputs with trace IDs
- whether any provider call was made

This version turns "it seems to work" into "we have a measurable local baseline."

## AOIS Connection

The AOIS path is now:

`incident -> structured endpoint -> route decision -> trace id -> eval baseline -> reliability signal`

`v1` made the structured endpoint.
`v2` made route decisions visible.
`v3` makes correctness and traceability visible.

## Learning Goals

By the end of this version you should be able to:

- explain trace IDs
- explain evaluation baseline
- explain regression
- run local eval cases
- inspect score and failures
- explain why provider calls remain disabled
- explain how reliability supports later model integration

## Resource Gate

Do not call external providers in this version.

Allowed:

- local Python compilation
- local eval script
- short-lived FastAPI runtime on `127.0.0.1`
- local `curl` requests

Not allowed without explicit approval:

- provider API calls
- provider SDK installs
- secrets
- persistent service runtime
- cloud resources

## Prerequisites

You should have completed:

- Phase 0
- `v1` structured AI endpoint
- `v2` model routing

Required checks:

```bash
python3 -m py_compile app/reliability.py examples/run_eval_baseline.py app/main.py
python3 examples/run_eval_baseline.py
```

## Core Concepts

## Trace ID

A trace ID is a correlation value attached to output.

It helps answer:

- which request produced this result?
- which logs belong together?
- which evaluation run failed?

This version uses local trace IDs like:

```text
aois-p-abc123def456
```

## Evaluation Case

An evaluation case is a known input with an expected output.

Example:

- message: `pod OOMKilled exit code 137`
- expected category: `memory-pressure`
- expected severity: `high`

## Baseline

A baseline is the current known behavior.

Before improving AOIS, you need to know what behavior must not regress.

## Regression

A regression happens when a change breaks behavior that used to pass.

## Provider Visibility

Every reliability output still reports:

```json
"provider_call_made": false
```

That keeps cost, secrets, and data exposure visible.

## Build

Inspect:

```bash
sed -n '1,260p' app/reliability.py
sed -n '1,120p' examples/run_eval_baseline.py
```

Compile:

```bash
python3 -m py_compile app/reliability.py examples/run_eval_baseline.py app/main.py
```

Run the local baseline:

```bash
python3 examples/run_eval_baseline.py
```

Expected output shape:

```json
{
  "mode": "local_eval_baseline",
  "provider_call_made": false,
  "score": 1.0,
  "total_cases": 4
}
```

Run the API only for the lab:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006
```

Call:

```bash
curl -sS http://127.0.0.1:8006/ai/eval/baseline
```

Stop the server after validation.

## Ops Lab

Run:

```bash
python3 examples/run_eval_baseline.py
```

Questions:

1. Which field correlates the eval run?
2. Which field proves no provider was called?
3. Which field shows the number of cases?
4. Which field shows pass count?
5. Which field shows the score?

Answer key:

1. `trace_id`
2. `provider_call_made=false`
3. `total_cases`
4. `passed_cases`
5. `score`

## Break Lab

Do not skip this.

### Option A - Change An Expected Category In A Scratch Copy

Make a scratch copy:

```bash
cp app/reliability.py /tmp/reliability_broken.py
```

Change one expected category in the scratch copy and inspect why the real baseline would fail if the expected behavior changed incorrectly.

Lesson:

- eval cases encode expectations

### Option B - Think Through A Real Regression

If the analyzer stopped recognizing `OOMKilled`, the `memory_pressure` case would fail.

Expected symptom:

- `passed_cases` drops
- `score` drops below `1.0`

Lesson:

- evaluations turn hidden behavior drift into visible failure

## Testing

The version passes when:

1. Python files compile
2. local eval baseline returns `score=1.0`
3. eval output includes `trace_id`
4. eval output includes `provider_call_made=false`
5. `/ai/eval/baseline` works during short-lived API validation
6. server is stopped after validation
7. no external provider is called

## Common Mistakes

- adding model calls before evaluation exists
- treating one successful manual test as reliability
- ignoring trace IDs
- hiding provider-call status
- updating expected outputs casually
- leaving uvicorn running after validation

## Troubleshooting

If local eval fails:

```bash
python3 examples/run_eval_baseline.py
```

Read the failed case and compare:

- expected category
- actual category
- expected severity
- actual severity

If API eval cannot connect:

- confirm uvicorn is running
- confirm host is `127.0.0.1`
- confirm port is `8006`

If provider call is true:

- stop immediately
- remove provider execution
- restore local baseline only

## Benchmark

Measure:

- compile result
- local eval score
- total cases
- passed cases
- API eval response
- whether provider call remained false
- whether server was stopped

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can run, inspect, break, explain, and defend local reliability baselines. |
| 4/5 | Eval works, but one reliability concept needs review. |
| 3/5 | Script runs, but regression or trace reasoning is weak. |
| 2/5 | Output appears, but baseline value is unclear. |
| 1/5 | Reliability still means "try it once manually." |

Minimum pass: `4/5`.

## Architecture Defense

Why evaluation before real provider scale?

Because model behavior changes are hard to trust without expected cases and regression checks.

Why trace IDs now?

Because even local systems need correlation habits before distributed tracing arrives.

Why no provider call?

Because this version measures local correctness and reliability structure, not model quality.

## 4-Layer Tool Drill

Tool: evaluation baseline

1. Plain English
It checks known examples and reports whether AOIS still behaves as expected.

2. System Role
It protects AOIS from regressions as analysis, routing, and future provider behavior evolve.

3. Minimal Technical Definition
It is a set of input/output test cases with scoring and traceable results.

4. Hands-on Proof
Running `python3 examples/run_eval_baseline.py` returns pass count, score, trace ID, and provider-call status.

## 4-Level System Explanation Drill

1. Simple English
AOIS can now check whether its basic intelligence behavior still works.

2. Practical Explanation
I can run an eval script, inspect pass/fail cases, and use a trace ID to correlate output.

3. Technical Explanation
`v3` adds local evaluation cases, scoring, trace IDs, and a FastAPI endpoint for the eval baseline.

4. Engineer-Level Explanation
AOIS now has a reliability boundary that measures baseline behavior before provider integration, making regressions, traceability, and provider-call state visible.

## Failure Story

Representative failure:

- Symptom: a later analyzer change stops detecting OOMKilled incidents
- Root cause: no evaluation baseline was run before merging the change
- Fix: add and run baseline cases before changing analysis behavior
- Prevention: treat eval cases as part of the system contract
- What this taught me: reliability requires repeatable checks, not memory

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v3` solve in AOIS?
2. What is a trace ID?
3. What is an eval case?
4. What is a baseline?
5. What is a regression?
6. Why should provider-call status appear in reliability output?
7. Why is one manual success not enough?
8. Why should evals exist before real model integration?
9. What does `score=1.0` mean in this version?
10. Explain eval baseline using the 4-layer tool rule.
11. Explain `v3` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v3` solve in AOIS?

It gives AOIS a local reliability baseline so behavior can be measured and regressions can be detected.

2. What is a trace ID?

A value used to correlate a request, output, or evaluation run.

3. What is an eval case?

A known input with expected output.

4. What is a baseline?

The current expected behavior that future changes should not break.

5. What is a regression?

A new change breaking behavior that previously worked.

6. Why should provider-call status appear in reliability output?

Because cost, secrets, data exposure, and external dependency state must stay visible.

7. Why is one manual success not enough?

It does not prove repeatability or protect against future changes.

8. Why should evals exist before real model integration?

So provider behavior can be compared against known expectations instead of judged by vibes.

9. What does `score=1.0` mean in this version?

All local evaluation cases passed.

10. Explain eval baseline using the 4-layer tool rule.

- Plain English: it checks known examples.
- System Role: it protects AOIS from regressions.
- Minimal Technical Definition: it is a scored set of expected input/output cases.
- Hands-on Proof: running the eval script returns pass count, score, trace ID, and provider status.

11. Explain `v3` using the 4-level system explanation rule.

- Simple English: AOIS can check that its behavior still works.
- Practical explanation: I can run local evals and inspect failures.
- Technical explanation: `v3` adds `app/reliability.py`, `examples/run_eval_baseline.py`, and `/ai/eval/baseline`.
- Engineer-level explanation: AOIS now has a local reliability layer that supports traceability, regression detection, and provider-call visibility before external AI execution.

## Connection Forward

`v3` completes Phase 1's intelligence-core foundation:

`structured endpoint -> model routing -> reliability baseline`

Phase 2 can now focus on containerization and security without losing the provider-gated intelligence contract.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v3 Introduction](introduction.md)
- Next: [v3 Lab](lab.md)
<!-- AOIS-NAV-END -->
