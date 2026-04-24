# v10.5 Summary Notes

Authoring status: authored

## What Was Built

`v10.5` built a managed-agent tradeoff plan and a local validator:

- `cloud/aws/managed-agent-tradeoff.plan.json`
- `examples/validate_managed_agent_plan.py`

The plan compares AOIS-owned runtime with a managed cloud agent placeholder.

## What Was Learned

Managed model calls and managed agents are different architectural decisions.

A managed model endpoint handles inference. A managed agent may own orchestration, tool calls, memory, retrieval, traces, and action execution.

That makes the managed-agent decision a control decision, not just a convenience decision.

## Core Limitation Or Tradeoff

This version does not test a real managed cloud agent.

That is intentional. The curriculum first teaches how to evaluate the tradeoff safely, then gates live managed-agent work behind docs review, credentials, budget, data boundaries, tool permissions, evals, and rollback.
