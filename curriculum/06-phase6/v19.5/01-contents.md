# v19.5 Contents

Authoring status: authored

Topic: AI failure engineering and governance enforcement

Safety mode: local policy plan and deterministic simulation only. This version
does not start a governance runtime, policy engine, agent runtime, tool call,
provider call, cloud resource, container, database, or persistent service.

## Start Here

1. Read [02-introduction.md](02-introduction.md) to understand why AI failure
   governance follows chaos engineering.
2. Read [03-notes.md](03-notes.md) for the failure classes, policy gates, tool
   boundaries, human review paths, and fallback model.
3. Inspect `release-safety/aois-p/ai-failure-governance.plan.json`.
4. Run:

```bash
python3 -m py_compile examples/validate_ai_failure_governance_plan.py examples/simulate_ai_failure_governance.py
python3 examples/validate_ai_failure_governance_plan.py
python3 examples/simulate_ai_failure_governance.py
```

Expected result: both scripts pass while all runtime, tool-call, and provider
flags remain false.

## Topic Jumps

- Failure classes and policy gates: [03-notes.md](03-notes.md)
- Hands-on validation and break exercises: [04-lab.md](04-lab.md)
- Recovery procedure: [05-runbook.md](05-runbook.md)
- Measurement checklist: [07-benchmark.md](07-benchmark.md)
- Unsafe remediation failure story: [06-failure-story.md](06-failure-story.md)
- Transition to tool-using agents: [10-next-version-bridge.md](10-next-version-bridge.md)

## Self-Paced Path

1. Explain why AI failure is not only model inaccuracy.
2. Identify the failure classes in the v19.5 governance plan.
3. Run the validator and prove no enforcement runtime started.
4. Run the simulator and explain why each case is allowed, reviewed, blocked,
   or routed to fallback.
5. Break the plan in a scratch edit and use validator output to explain the
   missing control.
6. Explain how policy gates protect tool-using agents before v20.
7. Answer the mastery checkpoint in [03-notes.md](03-notes.md).
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19.5 Start Here](00-start-here.md)
- Next: [v19.5 Introduction](02-introduction.md)
<!-- AOIS-NAV-END -->
