# v2 Introduction

Authoring status: authored

## What This Version Is About

`v2` is model routing without provider execution.

AOIS learns how to choose between local baseline, fast external placeholder, and strong external placeholder routes using severity, latency, cost, and provider-budget approval.

## Why It Matters In AOIS

AI systems need routing discipline.

Not every incident deserves the strongest model, and not every budget allows an external provider.
This version makes route selection explainable before any real provider call exists.

## How To Use This Version

1. inspect `app/model_router.py`
2. compile the Python files
3. run `/ai/route` locally
4. compare route decisions under different budgets
5. prove `provider_call_made=false`
6. stop the server after validation
