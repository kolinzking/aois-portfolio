# v0.7 - Raw LLM Calls Before Tooling Makes Them Look Clean

Estimated time: 3 focused hours

## What This Builds

You build understanding around the first raw model-call artifact in AOIS:

- [examples/raw_llm_request.py](../../../examples/raw_llm_request.py)

## Why This Exists

If the first time you meet an LLM is through a framework, the system can feel magical.
`v0.7` removes that abstraction layer.

You should see:

- the prompt
- the model name
- the token limit
- the output loop

## AOIS Connection

The system path becomes:

`prompt + model settings -> remote model call -> free-text output`

This is the immediate precursor to `v1`.

## Learning Goals

By the end of this version you should be able to:

- explain what the raw Anthropic request is doing
- explain what `model`, `system`, `messages`, `max_tokens`, and `temperature` mean
- explain why the output is powerful but still awkward for production
- articulate the difference between intelligence and structure

## Prerequisites

Run:

```bash
sed -n '1,220p' examples/raw_llm_request.py
cat .env.example
```

## Core Concepts

### System prompt

The instruction layer that frames how the model should behave.

### Messages

The conversation input sent to the model.

### Temperature

A control over randomness.

### Max tokens

The output-length cap.

### Free-text output

Human-readable, useful, but not yet guaranteed to fit a strict schema.

## Build

Inspect the file:

```bash
sed -n '1,220p' examples/raw_llm_request.py
```

Notice:

- the API key is read from the environment
- the model is named explicitly
- the response is iterated block by block

## Ops Lab

If you have a real key configured locally, run:

```bash
python3 examples/raw_llm_request.py
```

Expected behavior:

- the model returns a plain-language explanation of the OOMKilled log

If you do not have a key:

- inspect the file anyway
- trace what would happen at each step

## Break Lab

Run without a key:

```bash
env -u ANTHROPIC_API_KEY python3 examples/raw_llm_request.py
```

Expected:

- runtime error for missing key

Lesson:

- model calls depend on config, auth, network, and provider behavior
- the failure surface is larger than the local regex analyzer

## Testing

Syntax check:

```bash
python3 -m py_compile examples/raw_llm_request.py
```

## Common Mistakes

### Assuming raw text is production-ready output

It is not.
It still needs structure if the application wants reliable fields.

### Treating prompt text like hidden magic

The prompt is just input.
It is important, but it is still part of system design.

### Ignoring cost and latency

A remote model call is much heavier than a local regex function.

## Troubleshooting

If the file fails immediately:

- check `ANTHROPIC_API_KEY`
- compare `.env` to `.env.example`

If imports fail:

- inspect `requirements.txt`

## Benchmark

The benchmark in this version is comparative rather than numeric:

- local regex path
- remote model path

That tradeoff is the whole reason model routing exists later.

## Architecture Defense

Why show the raw call before `v1`:

- it removes framework mystique
- it makes the later structure problem obvious
- it shows why intelligence and structure are separate issues

## 4-Layer Tool Drill

### Anthropic client

1. Plain English
It sends the prompt to Claude and gets the answer back.

2. System Role
It is the first real model-call interface in AOIS.

3. Minimal Technical Definition
It is a Python SDK client for Anthropic's messages API.

4. Hands-on Proof
Without it, `v0.7` cannot demonstrate the jump from regex rules to model reasoning.

## 4-Level System Explanation Drill

1. Simple English
`v0.7` is AOIS talking to a real model for the first time.

2. Practical Explanation
It sends one infrastructure log and gets back a natural-language explanation.

3. Technical Explanation
It uses the Anthropic SDK to send a system prompt and one user message to Claude and prints the returned text blocks.

4. Engineer-Level Explanation
`v0.7` demonstrates raw model invocation as a remote dependency with explicit prompt, token, and auth settings, while also exposing the lack of structured output guarantees that later versions must solve.

## Failure Story

The representative failure is being impressed by the intelligence and missing the operational problems:

- auth
- cost
- latency
- output variability

## Mastery Checkpoint

You are ready to leave `v0.7` when you can:

1. explain every field in the raw request
2. explain why the result is impressive and still operationally incomplete
3. explain what happens when the API key is missing
4. defend why raw model calls appear only after `v0.6`

## Connection Forward

`v0.8` adds persistence so AOIS can stop acting like a stateless toy and start remembering incidents and analyses.
