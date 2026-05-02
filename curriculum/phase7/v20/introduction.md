# v20 Introduction

Authoring status: authored

## What This Version Is About

v20 starts Phase 7: Agentic AOIS.

The new capability is a tool-using incident responder. It can plan which
observability tools would be useful, attach a reason to each step, evaluate
bounded tool results, and decide whether to answer, gather more evidence, ask
for human approval, block and redact, or fall back to a runbook.

This lesson deliberately stays local and deterministic. It models tool use
without executing tools.

## Why It Matters In AOIS

Before v20, AOIS could analyze incidents, define reliability targets, trace
behavior, test failure assumptions, and enforce AI governance policy.

That is still not agentic operation.

Agentic operation begins when the system can choose actions. Even read-only
actions increase risk because they can expose sensitive data, create misleading
evidence, or make a weak answer look authoritative.

v20 teaches the safe first move:

```text
plan -> choose read-only tool -> validate result -> decide -> stop or continue
```

The live version of this pattern would require a real tool runtime, approval
workflow, audit storage, provider budget, and rollback plan. This lesson keeps
those disabled and proves they are disabled.

## How To Use This Version

Work through the files in this order:

1. `notes.md`
2. `agentic/aois-p/tool-using-responder.plan.json`
3. `examples/validate_tool_using_responder_plan.py`
4. `examples/simulate_tool_using_responder.py`
5. `lab.md`
6. `runbook.md`

The important proof is not that a tool was executed. The important proof is
that AOIS can describe a tool step, limit it to read-only evidence collection,
reject unsafe actions, and produce an auditable decision.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20 Contents](CONTENTS.md)
- Next: [v20 - Tool-Using Incident Responder](notes.md)
<!-- AOIS-NAV-END -->
