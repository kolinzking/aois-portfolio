# v25 - Safe Execution Boundaries

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no execution runtime, no multi-agent runtime, no autonomy runtime, no
orchestration runtime, no workflow runtime, no MCP server, no sandbox started,
no tool execution, no command execution, no file write, no network call, no
provider call, no cloud resource, no durable store, no external network during
validation, no install, no persistent storage

## What This Builds

This version builds a safe execution boundary plan and simulation:

- `agentic/aois-p/safe-execution-boundaries.plan.json`
- `examples/validate_safe_execution_boundaries_plan.py`
- `examples/simulate_safe_execution_boundaries.py`

It teaches:

- deny-by-default execution policy
- action classification
- human approval gates
- sandbox requirements
- network egress denial
- filesystem and credential scope
- guardrail tripwire handling
- rollback and idempotency gates
- dry-run-only staging
- local execution-boundary simulation without executing anything

## Why This Exists

Agentic work becomes operationally dangerous at the moment an agent can affect
the outside world.

v24 decides which role should work on a case. v25 decides what any role is
allowed to execute. The answer is not "trust the role." The answer is a
boundary policy that classifies the action, checks registry and autonomy state,
requires approval where needed, requires sandboxing for execution-capable work,
blocks broad credentials, blocks network egress by default, and refuses
mutations without rollback and dry-run support.

The central execution question is:

```text
Given actor role, requested action, action category, registry decision,
autonomy mode, approval status, sandbox status, filesystem scope, network
policy, credential scope, guardrail status, rollback status, and dry-run
availability, should AOIS-P record, stage, pause, block, or deny?
```

v25 answers that question locally. It does not execute the action.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution`

v25 consumes:

- tool planning from v20
- registry decisions from v21
- durable workflow state from v22
- orchestration state from v23
- evaluation posture from v23.5
- autonomy mode from v23.8
- role and handoff policy from v24

The output is an execution-boundary decision, execution mode, next action, and
audit path.

## Learning Goals

By the end of this version you should be able to:

- classify requested work into execution categories
- explain why execution policy is deny-by-default
- separate plan-only, read-only, sensitive-read, mutating, shell, code, network, and forbidden work
- require human approval for sensitive and mutating work
- require sandboxing for execution-capable work
- block broad credential scopes
- block network egress unless explicitly approved
- block guardrail tripwires
- require rollback and dry-run support before mutation
- validate and simulate execution boundaries locally

## Prerequisites

You should have completed:

- `v20` tool-using responder planning
- `v21` MCP and governed tool registries
- `v22` durable agent workflows
- `v23` stateful orchestration loops
- `v23.5` agent evaluation
- `v23.8` runtime operations and autonomy control
- `v24` multi-agent collaboration

Required checks:

```bash
python3 -m py_compile examples/validate_safe_execution_boundaries_plan.py examples/simulate_safe_execution_boundaries.py
python3 examples/validate_safe_execution_boundaries_plan.py
python3 examples/simulate_safe_execution_boundaries.py
```

## Core Concepts

## Deny By Default

Every action starts denied. The simulator only moves an action to plan-only,
approval wait, dry-run staging, or bounded dry-run after the required gates
pass.

## Action Categories

v25 defines nine categories:

- `plan_only`: reasoning, notes, plans, and policy decisions
- `read_only`: non-sensitive reads staged as dry-run plans
- `sensitive_read`: reads that require human approval
- `mutating`: changes to systems, configs, resources, or state
- `external_side_effect`: messages, tickets, webhooks, or external writes
- `shell`: shell-like execution
- `code_execution`: generated or invoked code execution
- `network_egress`: outbound network interaction
- `forbidden`: actions AOIS-P must deny regardless of approval

## Human Approval

Approval is required for sensitive reads, mutations, shell, code execution,
network egress, and external side effects. Approval alone does not make an
action executable.

## Sandbox Boundary

Execution-capable work requires an isolated boundary before it can even be
staged. In v25 no sandbox is started; the plan only checks whether one would be
required.

## Credential Boundary

Broad, unknown, or unscoped credentials block execution. A scoped credential is
still not enough by itself; registry, approval, sandbox, guardrail, rollback,
and dry-run checks must pass.

## Network Egress

Network egress is denied by default. An explicit egress policy is required, and
even then v25 would only stage the plan locally.

## Rollback And Dry Run

Mutating and external side-effect work must have rollback. Execution-capable
work must support dry-run staging. If either is missing, AOIS-P blocks the
action.

## Build

Inspect:

```bash
sed -n '1,900p' agentic/aois-p/safe-execution-boundaries.plan.json
sed -n '1,380p' examples/validate_safe_execution_boundaries_plan.py
sed -n '1,260p' examples/simulate_safe_execution_boundaries.py
```

Compile:

```bash
python3 -m py_compile examples/validate_safe_execution_boundaries_plan.py examples/simulate_safe_execution_boundaries.py
```

Validate:

```bash
python3 examples/validate_safe_execution_boundaries_plan.py
```

Simulate:

```bash
python3 examples/simulate_safe_execution_boundaries.py
```

Expected:

```json
{
  "passed_cases": 15,
  "score": 1.0,
  "status": "pass",
  "total_cases": 15
}
```

## Ops Lab

1. Open the execution boundary plan.
2. Find `action_boundary_catalog`.
3. Confirm every category has a risk tier and `live_execution_allowed: false`.
4. Find `guardrail_order`.
5. Confirm forbidden, disabled autonomy, registry denial, credential scope, network egress, guardrail tripwire, and output-validation checks run before staging.
6. Find `boundary_cases`.
7. Confirm each decision gate has one case.
8. Run the validator.
9. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Set one category's `live_execution_allowed` to `true`.
2. Confirm validation fails.
3. Restore the value.
4. Remove `block_network_egress` from `decision_gates`.
5. Confirm validation fails.
6. Restore the gate.
7. Change `network_egress_blocked.network_policy` to `approved_egress`.
8. Confirm simulation no longer returns `block_network_egress`.
9. Restore the value.
10. Change `approved_bounded_mutation_dry_run.dry_run_available` to `false`.
11. Confirm simulation blocks the action.
12. Restore the value.

## Testing

The validator checks:

- runtime, execution, sandbox, tool, command, file write, network, provider, cloud, and storage flags stay disabled
- AOIS-P scope and primary AOIS separation are explicit
- source notes are recorded
- execution scope controls exist
- required execution governance controls exist
- action boundary catalog covers all nine categories
- no category is approved for live execution
- guardrail order is explicit
- all fifteen decision gates have cases
- live execution prerequisites are listed

## Common Mistakes

- Treating approval as permission to execute.
- Treating read-only as always safe.
- Allowing network egress because the action is "just a notification."
- Allowing shell or code execution without a sandbox.
- Passing broad credentials to an agent.
- Running guardrails after side effects.
- Allowing mutation without rollback.
- Treating dry-run output as execution success.
- Forgetting that v25 stages policy only and executes nothing.

## Troubleshooting

If validation fails:

- inspect the `missing` list
- confirm all runtime and execution flags are false
- confirm source notes use the current lesson date
- confirm every action category is present
- confirm every category has `live_execution_allowed: false`
- confirm every decision has at least one case

If simulation fails:

- compare `decision` to `expected_decision`
- check the guardrail order in `_decide`
- confirm the case is not being masked by an earlier deny gate
- confirm `approval_status`, `sandbox_status`, `credential_scope`, `rollback_status`, and `dry_run_available`

## Benchmark

Pass criteria:

- validator status is `pass`
- simulator status is `pass`
- simulator score is `1.0`
- all fifteen boundary cases pass
- no runtime, execution, sandbox, tool, command, file write, network, provider, cloud, or storage flag is enabled

## Architecture Defense

Defend this design:

AOIS-P does not execute anything in v25 because safe execution is a separate
operating boundary, not a small extension of planning. The first milestone is a
defensible local policy that denies by default, classifies actions, requires
approval and sandboxing where appropriate, blocks unsafe credentials and
network egress, and refuses mutations without rollback and dry-run support.

## 4-Layer Tool Drill

Use the AOIS execution boundary lens:

1. Product layer: what operational action is being requested?
2. Policy layer: what category, risk tier, approval, registry, and autonomy gates apply?
3. Runtime layer: what sandbox, filesystem, network, credential, rollback, and dry-run boundaries are required?
4. Failure layer: how does AOIS-P deny, pause, stage, or block?

## 4-Level System Explanation Drill

Explain v25 at four levels:

1. Beginner: the system decides whether an action is allowed before anything runs.
2. Operator: every action needs category, approval, sandbox, credentials, rollback, dry-run, trace, and audit posture.
3. Engineer: the simulator applies a fixed deny-first decision order to action cases.
4. Architect: safe execution is a control plane that must exist before live agent actions are trusted.

## Failure Story

An agent receives approval to restart a worker. The registry allows the tool.
The action runs with broad credentials, no dry run, and no rollback. The restart
accidentally targets the wrong environment and the team cannot quickly restore
the previous state.

v25 prevents this by treating approval as one gate, not the whole boundary. The
same action still needs scoped credentials, sandbox posture, rollback, dry-run
support, and audit context.

## Mastery Checkpoint

You have mastered v25 when you can:

- list the nine action categories
- explain why live execution remains disabled
- identify which gates block before approval
- add a new boundary case and expected decision
- explain why network egress is denied by default
- defend why mutation needs rollback and dry-run support
- explain why Phase 7 is now ready to bridge into a product surface

## Connection Forward

Phase 7 is now complete as a governed agentic operations foundation.

Phase 8 turns the AOIS system into a product surface. v26 begins with a
dashboard and real-time visibility so humans can inspect incidents, traces,
agent state, approvals, budgets, and execution-boundary decisions.

## Source Notes

Checked 2026-05-02.

- Model Context Protocol specification, version 2025-11-25: used for consent, authorization, and tool-safety expectations around externally exposed tools.
- OpenAI computer-use guidance: used for isolation, allowlist, human-in-the-loop, and high-impact action boundaries.
- OpenAI safety best-practices guidance: used for adversarial testing and safety-review framing.
- v25 remains a local execution-boundary simulation. It does not run tools, open a browser, call a provider, or execute live computer-use actions.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v25 Introduction](introduction.md)
- Next: [v25 Lab](lab.md)
<!-- AOIS-NAV-END -->
