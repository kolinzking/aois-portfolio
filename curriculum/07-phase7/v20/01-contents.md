# v20 Contents

Authoring status: authored

Topic: Tool-using incident responder

Safety mode: local plan and deterministic simulation only. This version does
not start an agent runtime, execute tools, call a provider, create cloud
resources, open network access, install dependencies, write persistent storage,
or mutate any AOIS workload.

## Start Here

1. Read [02-introduction.md](02-introduction.md) to understand why Phase 7 begins
   with tool planning rather than live tool execution.
2. Read [03-notes.md](03-notes.md) for the responder loop, tool contracts, evidence
   ledger, approval boundary, and fallback path.
3. Inspect `agentic/aois-p/tool-using-responder.plan.json`.
4. Run:

```bash
python3 -m py_compile examples/validate_tool_using_responder_plan.py examples/simulate_tool_using_responder.py
python3 examples/validate_tool_using_responder_plan.py
python3 examples/simulate_tool_using_responder.py
```

Expected result: validation and simulation pass while `agent_runtime_started`,
`tool_calls_executed`, and `provider_call_made` remain false.

## Topic Jumps

- Responder loop and tool contracts: [03-notes.md](03-notes.md)
- Hands-on validation and break exercises: [04-lab.md](04-lab.md)
- Recovery procedure: [05-runbook.md](05-runbook.md)
- Measurement checklist: [07-benchmark.md](07-benchmark.md)
- Unsafe tool-use failure story: [06-failure-story.md](06-failure-story.md)
- Transition to cost accounting: [10-next-version-bridge.md](10-next-version-bridge.md)

## Self-Paced Path

1. Explain the difference between choosing a tool and executing a tool.
2. Identify the read-only tools in the v20 plan.
3. Run the validator and prove no live agent or tool runtime started.
4. Run the simulator and explain the five decisions.
5. Break the plan in a scratch edit and use validator output to restore the
   missing control.
6. Explain why a mutating tool routes to human approval.
7. Answer the mastery checkpoint in [03-notes.md](03-notes.md).
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20 Start Here](00-start-here.md)
- Next: [v20 Introduction](02-introduction.md)
<!-- AOIS-NAV-END -->
