# v5 Summary Notes

Authoring status: authored

## What Was Built

Local security inspection:

- prompt-injection signal detection
- secret-like redaction
- structured findings
- CLI inspection
- API inspection route

## What Was Learned

LLM security begins before model calls.

Inputs can contain instructions and secrets, so AOIS needs inspection before provider, log, and deployment boundaries.

## Core Limitation Or Tradeoff

Pattern matching is not complete security.

It is a first guardrail that prepares AOIS for stronger policy, red-teaming, and runtime controls later.
