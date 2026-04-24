# v0.7 Introduction

Authoring status: authored

## What This Version Is About

`v0.7` is LLM request design without provider dependence.

This version teaches how a model call is shaped before any external AI provider is used.
You will build and run a dry-run request builder that estimates token count, possible cost, output budget, latency budget, and structured-output expectations.

## Why It Matters In AOIS

AOIS should not become a project that blindly sends prompts to a model and hopes for useful output.

The right order is:

1. understand the request shape
2. understand what data is being sent
3. estimate token and cost exposure
4. define expected structured fields
5. gate real provider calls behind approval, budget, and key management

This keeps the curriculum self-paced while still preparing for serious AI infrastructure work.

## How To Use This Version

1. read the resource gate first
2. inspect `examples/raw_llm_request.py`
3. compile it with `python3 -m py_compile`
4. run the dry-run request examples
5. change output budget, cost assumption, and response format
6. explain the difference between a request plan and a real provider call
7. complete the mastery checkpoint before moving to persistence in `v0.8`
