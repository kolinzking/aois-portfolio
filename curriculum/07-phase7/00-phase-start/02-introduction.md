# Phase 7 Introduction

Authoring status: authored

Phase 7 turns AOIS from deterministic incident analysis into governed agentic
operations.

The phase focus is not "let an agent do things." The focus is controlled agent
work:

- plan tool use before execution
- classify tool risk
- account for per-step cost
- route by budget and expected value
- govern MCP tool exposure
- preserve workflow state across pauses, retries, and failures
- evaluate and operate agent loops before trusting them
- coordinate multiple agent roles under a supervisor
- bound execution before any real-world side effect

## Current Progress

Phase 7 is authored through `v25`.

AOIS-P can now model:

- read-only incident tool planning
- mutating tool approval boundaries
- cost accounting
- budget-aware routing
- governed MCP tool registry decisions
- durable workflow checkpoints, approval waits, idempotency, retries, timeouts, and recovery actions
- stateful orchestration loop policy with stop, wait, resume, and action decisions
- connected agent evaluation across route, registry, workflow, orchestration, safety, and budget fields
- runtime autonomy modes with kill switch, rollback, demotion, observability, budget, safety, and approval gates
- supervisor-led multi-agent collaboration with role catalogs, handoff contracts, shared state, conflict escalation, and loop limits
- safe execution boundaries with action categories, approval, sandbox, credential, network, rollback, dry-run, and guardrail gates

## Remaining Work

Phase 7 is complete.

The next corpus step is Phase 8, which turns the governed AOIS-P operating
model into a product surface for human operators.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [Phase 7 Contents](01-contents.md)
- Next: [v20 Start Here](../v20/00-start-here.md)
<!-- AOIS-NAV-END -->
