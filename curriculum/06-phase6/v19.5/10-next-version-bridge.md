# v19.5 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v19.5 gives AOIS a policy boundary for AI behavior. The system can now describe
when an AI recommendation is allowed, reviewed, blocked, or routed to fallback.

This matters because the next phase introduces agents.

## Why The Next Version Exists

v20 starts Phase 7: tool-using AOIS responders.

A tool-using agent is more powerful than an analysis endpoint. It can gather
evidence, inspect logs, call tools, maintain intermediate state, and move
through an incident workflow.

The danger is also larger:

- a bad recommendation can become a bad action
- missing evidence can lead to wrong tool use
- prompt injection can redirect work
- excessive agency can cross policy boundaries
- costs and blast radius can grow step by step

v19.5 exists so v20 does not start from trust. It starts from controls.

The next lesson asks:

```text
How does AOIS let an agent investigate incidents while keeping every tool use
visible, bounded, reviewable, and reversible?
```
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19.5 Looking Forward](09-looking-forward.md)
- Next: [Phase 6 Looking Forward](../zz-phase-end/01-looking-forward.md)
<!-- AOIS-NAV-END -->
