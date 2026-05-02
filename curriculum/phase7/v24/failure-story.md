# v24 Failure Story

Authoring status: authored

## Symptom

An incident response agent hands work to an evidence specialist and a safety
specialist at the same time. The evidence specialist works from an older trace.
The safety specialist works from a newer registry decision. The response
specialist merges both findings and produces a confident recommendation.

The operator sees one final answer, not the state mismatch that created it.

## Root Cause

The system treated "more agents" as redundancy instead of coordination. It had
no supervisor-owned shared state, no context freshness check, no serial handoff
rule, and no conflict escalation path.

## Fix

v24 fixes this by requiring:

- one supervisor-owned role catalog
- explicit allowed targets
- minimal role-scoped context
- serial specialist handoffs
- a shared state contract
- handoff loop limits
- human escalation for conflicting findings

## Prevention

Before adding live multi-agent execution, prove the local plan:

```bash
python3 examples/validate_multi_agent_collaboration_plan.py
python3 examples/simulate_multi_agent_collaboration.py
```

Then review any new specialist role for owner, allowed targets, context scope,
audit behavior, and no direct tool/provider capability.
