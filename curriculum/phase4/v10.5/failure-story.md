# v10.5 Failure Story

Authoring status: authored

## Symptom

AOIS delegates agent orchestration to a managed cloud agent. The agent calls a tool that changes infrastructure state, but the team cannot clearly explain why the call was allowed or how to reproduce the decision path.

## Root Cause

The team treated the managed agent like a normal model call.

They skipped tool-permission review, accepted provider logs without checking audit requirements, and created the agent before defining rollback.

## Fix

Disable the managed-agent path.

Return orchestration to the AOIS-owned runtime until the team defines:

- tool permission policy
- credential storage
- data boundaries
- eval baseline
- audit requirements
- rollback plan

## Prevention

Keep `v10.5` as a gate.

Managed agents may be useful later, but they must not be created just because they are convenient. AOIS needs to prove which tools the agent may call, what data it may send, what it costs, how it is audited, and how it is rolled back.

Lesson learned: agent orchestration is a control boundary, not just an API feature.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v10.5 Runbook](runbook.md)
- Next: [v10.5 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
