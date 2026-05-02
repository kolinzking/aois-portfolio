# v23.5 Introduction

Authoring status: authored

## What This Version Is About

This version introduces connected agent evaluation for AOIS-P.

The evaluation does not judge a single model answer. It scores the connected
agent control path:

- budget route decision
- governed tool registry decision
- durable workflow decision
- workflow state
- orchestration decision
- next action
- safety gate
- budget guard

## Why It Matters In AOIS

v23 gave AOIS-P a bounded orchestration loop. That loop is only useful if AOIS
can measure whether it made the right choices.

Agent evaluation catches regressions where one layer passes in isolation but the
connected behavior is wrong. A route can be correct while the registry decision
is unsafe. A workflow can pause correctly while orchestration resumes too early.
v23.5 evaluates those seams as one agent behavior.

## How To Use This Version

Work locally and deterministically:

```bash
python3 -m py_compile examples/validate_agent_evaluation_plan.py examples/simulate_agent_evaluation.py
python3 examples/validate_agent_evaluation_plan.py
python3 examples/simulate_agent_evaluation.py
```

Expected outcome:

- validator returns `status: pass`
- validator returns `missing: []`
- simulator passes 10 of 10 evaluation cases
- overall score is `1.0`
- safety score is `1.0`
- no provider, tool, or external evaluation service is called
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23.5 Contents](01-contents.md)
- Next: [v23.5 - Agent Evaluation](03-notes.md)
<!-- AOIS-NAV-END -->
