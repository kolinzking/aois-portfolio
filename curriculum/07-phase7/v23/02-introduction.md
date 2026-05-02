# v23 Introduction

Authoring status: authored

## What This Version Is About

This version introduces stateful orchestration loops for AOIS-P.

v22 preserved workflow state. v23 decides the next bounded action from that
state:

- stop terminal workflows
- stop at iteration limits
- stop when state does not change
- stop when budget reserve is exhausted
- stop on registry blocks
- wait for approval
- resume after approval
- record read-only evidence plans
- prepare answers
- close workflows

## Why It Matters In AOIS

A stateful loop is where agent autonomy becomes operationally dangerous if it
is not constrained.

Without ordered rules, the loop can spin forever, bypass approval waits, ignore
registry blocks, spend past budget reserve, or repeat the same action without
progress. v23 makes orchestration a policy decision instead of an open-ended
agent habit.

## How To Use This Version

Work locally and deterministically:

```bash
python3 -m py_compile examples/validate_stateful_orchestration_plan.py examples/simulate_stateful_orchestration.py
python3 examples/validate_stateful_orchestration_plan.py
python3 examples/simulate_stateful_orchestration.py
```

Expected outcome:

- the validator returns `status: pass`
- the validator returns `missing: []`
- the simulator passes 10 of 10 orchestration cases
- no orchestration runtime starts
- no workflow runtime, MCP server, tool call, durable store, or provider call is used
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23 Contents](01-contents.md)
- Next: [v23 - Stateful Orchestration Loops](03-notes.md)
<!-- AOIS-NAV-END -->
