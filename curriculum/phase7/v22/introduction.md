# v22 Introduction

Authoring status: authored

## What This Version Is About

This version introduces durable agent workflows for AOIS-P.

It does not run Temporal, LangGraph, or any workflow engine. It builds the local
workflow contract that an agentic incident response needs before live execution:

- workflow state
- checkpoints
- pause and resume points
- human approval waits
- idempotency keys
- retry budgets
- timeout policy
- terminal states
- recovery actions

## Why It Matters In AOIS

v21 governed which tools can be exposed to a route. v22 governs how a multi-step
agent process remembers progress and recovers.

Without durable workflow design, a responder can lose context after a crash,
repeat a step after a retry, skip an approval, or leave an incident half-closed.
Durability makes agent work observable, resumable, and bounded.

## How To Use This Version

Work locally and deterministically:

```bash
python3 -m py_compile examples/validate_durable_workflow_plan.py examples/simulate_durable_workflow.py
python3 examples/validate_durable_workflow_plan.py
python3 examples/simulate_durable_workflow.py
```

Expected outcome:

- the validator returns `status: pass`
- the validator returns `missing: []`
- the simulator passes 8 of 8 workflow cases
- no workflow engine starts
- no durable store is created
- no MCP server, tool call, or provider call is used
