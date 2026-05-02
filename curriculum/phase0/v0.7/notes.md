# v0.7 - LLM Fundamentals Without Provider Dependence

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: no external API call, no key, standard-library dry run

## What This Builds

This version builds `examples/raw_llm_request.py`, a dry-run LLM request builder.

It teaches:

- system prompt
- user prompt
- model choice placeholder
- temperature
- structured-output expectation
- token estimate
- cost estimate
- latency budget

The script intentionally does not call OpenAI, Groq, or any other provider.

## Why This Exists

AI infrastructure work should not begin with blind API calls.

Before sending real requests, you need to understand:

- what you are asking the model to do
- what input you are sending
- how much output you allow
- how token count affects cost and latency
- why structured output is safer than free-form text
- what should be measured before provider integration

This protects both learning quality and server/resource safety.

## AOIS Connection

The AOIS path is now:

`incident signal -> prompt draft -> token/cost estimate -> structured-output expectation -> provider-gated request`

`v0.6` exposed deterministic analysis through an API.
`v0.7` teaches the model-call boundary before any real AI provider is connected.

## Learning Goals

By the end of this version you should be able to:

- explain system prompt versus user prompt
- explain tokens in practical terms
- estimate token cost before sending a request
- explain temperature
- explain latency budget
- explain why structured output matters
- distinguish dry-run request design from real provider execution
- explain why API keys and paid calls require explicit approval

## Resource Gate

No provider call is allowed in this version by default.

Do not use:

- OpenAI API key
- Groq API key
- Anthropic API key
- cloud model endpoint
- paid inference

Real-provider mode requires explicit approval and a tiny request budget.

## Prerequisites

You should have completed:

- `v0.1` Linux inspection
- `v0.2` Bash automation
- `v0.3` Git discipline
- `v0.4` HTTP inspection
- `v0.5` Python logic
- `v0.6` API contracts

Required check:

```bash
python3 -m py_compile examples/raw_llm_request.py
```

## Core Concepts

## System Prompt

A system prompt gives high-level behavior instructions.

In AOIS, it defines the model's operational role:

```text
You are AOIS, an operations analysis assistant.
```

## User Prompt

A user prompt contains the specific task or incident signal.

Example:

```text
Analyze this incident signal: gateway returned 5xx after deploy
```

## Token

A token is a chunk of text used by a model.

This lesson uses a rough estimate:

```text
4 characters ~= 1 token
```

This is not provider-accurate.
It is a learning estimate that helps you reason before making real calls.

## Cost

Model providers usually charge by token usage.

The dry-run estimate uses:

```text
estimated_cost = estimated_total_tokens / 1,000,000 * cost_per_million_tokens
```

The exact price depends on provider and model.

## Latency Budget

Latency budget is how long the system can afford to wait.

For AOIS, latency matters because incident response systems should not wait blindly for slow model calls.

## Structured Output

Structured output means the model should return fields the system can parse.

AOIS expects fields like:

- category
- severity
- confidence
- summary
- recommended_action

Free-form text is easier to read but harder to validate.

## Build

Create or replace `examples/raw_llm_request.py` with the implementation in the repository.

Compile:

```bash
python3 -m py_compile examples/raw_llm_request.py
```

Run:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx after deploy
```

Expected output shape:

```json
{
  "mode": "dry_run_no_provider_call",
  "request": {
    "model": "provider-model-placeholder",
    "response_format": "json_object",
    "system_prompt": "...",
    "temperature": 0.0,
    "user_prompt": "..."
  },
  "estimate": {
    "input_tokens_estimate": 39,
    "max_output_tokens": 300,
    "estimated_total_tokens": 339,
    "estimated_cost_usd": 0.000339,
    "latency_budget_ms": 2000
  }
}
```

Your exact token estimate may differ if prompt text changes.

## Ops Lab

Run:

```bash
python3 examples/raw_llm_request.py pod OOMKilled exit code 137
python3 examples/raw_llm_request.py gateway returned 5xx --max-output-tokens 100
python3 examples/raw_llm_request.py gateway returned 5xx --cost-per-million-tokens 5
```

Questions:

1. Which field proves no provider was called?
2. Which setting changes output budget?
3. Which setting changes estimated cost?
4. Which prompt is stable across incidents?
5. Which prompt changes per incident?

Answer key:

1. `mode=dry_run_no_provider_call`
2. `max_output_tokens`
3. `cost_per_million_tokens`
4. `system_prompt`
5. `user_prompt`

## Break Lab

Do not skip this.

### Option A - Oversized output budget

Run:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx --max-output-tokens 5000
```

Expected symptom:

- estimated total tokens and cost increase

Lesson:

- output limits directly affect cost and latency risk

False conclusion this prevents:

- "only input prompt size matters"

### Option B - Free-form output mode

Run:

```bash
python3 examples/raw_llm_request.py gateway returned 5xx --format text
```

Expected symptom:

- response format changes to `text`

Lesson:

- free-form output may be readable but weaker for system integration

False conclusion this prevents:

- "if a human can read it, the system can safely parse it"

## Testing

The version passes when:

1. the script compiles
2. dry-run output is valid JSON
3. no external provider is called
4. token and cost estimates change when parameters change
5. you can explain system prompt, user prompt, tokens, cost, latency, and structured output

## Common Mistakes

- using API keys before understanding request shape
- ignoring output token budget
- treating rough token estimates as exact provider billing
- confusing prompt design with model reliability
- trusting free-form text as if it were structured data
- forgetting that latency and cost are operational constraints

## Troubleshooting

If the script fails to import:

```bash
python3 -m py_compile examples/raw_llm_request.py
```

If output is not JSON:

- inspect the script
- confirm it uses `json.dumps`

If cost looks too high:

- reduce `--max-output-tokens`
- lower the provider price assumption
- shorten the prompt

If you want to call a real provider:

- stop
- get explicit approval
- define a tiny request budget
- use a provider key outside Git

## Benchmark

Measure:

- can the script compile?
- can you produce a dry-run request?
- can you reduce output budget and explain cost change?
- can you switch output format and explain the tradeoff?
- can you explain why no provider call happened?

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can design, estimate, explain, and defend a model request without calling a provider. |
| 4/5 | You can run the dry-run but one concept needs review. |
| 3/5 | You can run examples but cost/token reasoning needs help. |
| 2/5 | Output appears, but model-call structure is unclear. |
| 1/5 | LLM calls still feel like magic API usage. |

Minimum pass: `4/5`.

## Architecture Defense

Why dry-run before real provider calls?

Because request design, cost estimation, and structured-output expectations should be understood before spending money or sending data to an external system.

Why not use Groq or OpenAI immediately?

Because provider integration is an operational boundary involving API keys, cost, rate limits, latency, and data exposure.
Those require explicit approval and controls.

Why teach structured output now?

Because AOIS is an operations system.
It needs parseable fields, not just impressive paragraphs.

## 4-Layer Tool Drill

Tool: LLM request

1. Plain English
An LLM request asks a model to produce output from instructions and input.

2. System Role
It will become AOIS's reasoning layer after deterministic rules are no longer enough.

3. Minimal Technical Definition
It is a structured payload sent to a model provider, usually including model name, prompts, generation settings, and output constraints.

4. Hands-on Proof
Before calling a provider, changing output tokens changes estimated cost; changing output format changes how safely AOIS could parse the result.

## 4-Level System Explanation Drill

1. Simple English
I learned how to design a model request before sending it.

2. Practical Explanation
I can create a dry-run request, estimate tokens and cost, set an output budget, and describe expected structured fields.

3. Technical Explanation
This version uses a provider-neutral Python script to model prompts, generation settings, token estimates, cost estimates, latency budget, and response format.

4. Engineer-Level Explanation
AOIS now has a model-call planning layer: before adding external inference, the learner can reason about request shape, output contracts, cost, latency, and structured parsing risk, which prevents blind provider integration.

## Failure Story

Representative failure:

- Symptom: estimated cost increased sharply
- Root cause: `max_output_tokens` was set too high
- Fix: reduce output budget to match the actual response need
- Prevention: estimate token budget before provider calls
- What this taught me: output limits are operational controls, not cosmetic settings

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v0.7` solve in AOIS?
2. What is a system prompt?
3. What is a user prompt?
4. What is a token?
5. Why is token estimation useful even when rough?
6. What is a latency budget?
7. Why does output budget affect cost?
8. Why is structured output safer than free-form output?
9. Why are real provider calls gated?
10. Explain an LLM request using the 4-layer tool rule.
11. Explain `v0.7` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v0.7` solve in AOIS?

It teaches how to reason about model-call shape, cost, latency, and output structure before using a real provider.

2. What is a system prompt?

A system prompt gives stable high-level behavior instructions, such as the model's role and output expectations.

3. What is a user prompt?

A user prompt contains the specific task or incident signal for this request.

4. What is a token?

A token is a chunk of text processed by a model.
It is the basic unit behind context size, cost, and often latency.

5. Why is token estimation useful even when rough?

It helps you reason before spending money or waiting on slow calls.
Rough estimates catch bad budgets early.

6. What is a latency budget?

It is the maximum time the system can afford to wait for a model response before the call becomes operationally problematic.

7. Why does output budget affect cost?

Providers usually charge for output tokens as well as input tokens.
Allowing too much output increases possible cost and latency.

8. Why is structured output safer than free-form output?

Structured output gives fields AOIS can validate and parse.
Free-form text may be readable but harder to automate safely.

9. Why are real provider calls gated?

They involve API keys, cost, rate limits, latency, data exposure, and external dependency risk.
They require explicit approval and a budget.

10. Explain an LLM request using the 4-layer tool rule.

- Plain English: it asks a model to produce an answer from instructions and input.
- System Role: it becomes AOIS's reasoning layer after deterministic rules are insufficient.
- Minimal Technical Definition: it is a provider payload with model, prompts, settings, and output constraints.
- Hands-on Proof: changing max output tokens changes estimated cost, and changing response format changes parseability.

11. Explain `v0.7` using the 4-level system explanation rule.

- Simple English: I learned how to plan a model call before sending it.
- Practical explanation: I can build a dry-run request and estimate tokens, cost, and output expectations.
- Technical explanation: `v0.7` models prompts, generation settings, response format, token estimates, cost estimates, and latency budget in Python.
- Engineer-level explanation: AOIS now has a provider-gated model-call planning layer that protects cost, latency, output contracts, and data exposure before any real AI provider is introduced.

## Connection Forward

`v0.7` teaches the seventh AOIS habit:

`estimate before calling the model`

`v0.8` adds Postgres foundations so incidents and analysis results can become persistent data instead of only terminal output.

## Source Notes

This version is provider-neutral and does not make external model calls.

Before adding OpenAI, Groq, or another provider, check the official provider documentation for current:

- request format
- structured output support
- model names
- token accounting
- pricing
- rate limits
- safety and data-use terms
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.7 Introduction](introduction.md)
- Next: [v0.7 Lab](lab.md)
<!-- AOIS-NAV-END -->
