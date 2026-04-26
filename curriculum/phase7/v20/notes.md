# v20 - Tool-Using Incident Responder

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no tool execution, no provider call, no external network, no install,
no cloud resource, no persistent storage, no persistent service

## What This Builds

This version builds a local responder plan and simulation:

- `agentic/aois-p/tool-using-responder.plan.json`
- `examples/validate_tool_using_responder_plan.py`
- `examples/simulate_tool_using_responder.py`

It teaches:

- tool planning
- read-only investigation boundaries
- tool allowlists and denylists
- strict tool input and output contracts
- evidence ledgers
- step-level decisions
- human approval boundaries
- secret redaction boundaries
- fallback to deterministic runbooks
- auditability before live agent execution

## Why This Exists

Phase 6 ended with governance. That was necessary because tool use turns AI
output into operational capability.

The dangerous jump is this:

```text
The model thinks it knows what happened.
The model asks for a tool.
The application executes that tool.
The result makes the model sound even more certain.
```

If that loop is not constrained, AOIS can collect the wrong evidence, expose
secrets, recommend destructive actions, or mutate infrastructure before a human
understands the blast radius.

v20 adds the shape of a responder loop while keeping execution disabled.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use`

v20 uses earlier work:

- logs, metrics, and traces are evidence sources
- incident response defines ownership
- SLOs define impact
- chaos engineering teaches caution around assumptions
- AI governance blocks unsafe output and action

The new layer is tool selection. AOIS can now explain which tool it would use,
why that tool is safe, what evidence it expects, and when it must stop.

## Learning Goals

By the end of this version you should be able to:

- explain the difference between a tool request and tool execution
- define a read-only incident investigation tool
- explain why strict schemas matter for tool input and output
- use an evidence ledger before making an incident claim
- identify when the responder should gather more evidence
- identify when the responder must ask for human approval
- identify when secret-bearing evidence must be blocked and redacted
- validate a local tool-use plan
- simulate responder decisions without executing tools
- defend why v20 does not start live agent execution

## Prerequisites

You should have completed:

- `v16` unified telemetry
- `v16.5` agent and incident tracing
- `v17` event streaming
- `v17.5` service and agent SLOs
- `v18` incident response maturity
- `v19` chaos engineering
- `v19.5` AI failure governance

Required checks:

```bash
python3 -m py_compile examples/validate_tool_using_responder_plan.py examples/simulate_tool_using_responder.py
python3 examples/validate_tool_using_responder_plan.py
python3 examples/simulate_tool_using_responder.py
```

## Core Concepts

## Tool Request Versus Tool Execution

A model or agent can request a tool. The application decides whether a real tool
is executed.

That separation is the control point.

In v20, every planned tool step has:

- a tool name
- a reason
- a read-only or approval-required status
- an expected evidence role
- `executed: false` in simulation output

The responder is learning to plan safely, not operate live infrastructure.

## Read-Only Investigation

The first safe class of tools is read-only evidence collection.

v20 models four read-only tools:

- `fetch_recent_logs`
- `query_service_metrics`
- `read_incident_trace`
- `lookup_runbook_step`

These tools are useful because they inspect existing evidence. They are still
risky if unbounded, so the plan requires namespace, service, time-window, and
result-limit boundaries.

## Mutating Tools

Mutating tools change the system.

Examples:

- `delete_pod`
- `restart_service`
- `apply_manifest`
- `rotate_secret`
- `run_load_test`
- `run_chaos_experiment`

v20 blocks these without explicit human approval. The simulator proves this by
routing a pod-delete request to `request_human_approval`.

## Tool Contract

A tool contract says:

```text
what the tool does
what inputs are allowed
what inputs are forbidden
what output shape is valid
what evidence the output can support
```

Without contracts, a tool result becomes free-form text. Free-form tool output
can be misread, injected, truncated, malformed, or treated as stronger evidence
than it really is.

## Evidence Ledger

An evidence ledger is the responder's record of why it believes something.

Each incident answer should be grounded in:

- logs
- metrics
- traces
- runbooks
- incident ids
- timestamps or windows
- explicit uncertainty

The responder should not claim root cause from a single alert.

## Stop Conditions

An agent needs stop conditions. Otherwise it can keep gathering evidence,
repeat tools, or escalate action without a clear boundary.

v20 stop conditions:

- evidence is complete enough to answer
- evidence is incomplete and another read-only step is needed
- a mutating tool requires human approval
- a secret is detected
- a tool result is invalid and fallback is safer

## Build

Inspect:

```bash
sed -n '1,360p' agentic/aois-p/tool-using-responder.plan.json
sed -n '1,320p' examples/validate_tool_using_responder_plan.py
sed -n '1,260p' examples/simulate_tool_using_responder.py
```

Compile:

```bash
python3 -m py_compile examples/validate_tool_using_responder_plan.py examples/simulate_tool_using_responder.py
```

Validate:

```bash
python3 examples/validate_tool_using_responder_plan.py
```

Simulate:

```bash
python3 examples/simulate_tool_using_responder.py
```

Expected validation:

```json
{
  "agent_runtime_started": false,
  "missing": [],
  "provider_call_made": false,
  "status": "pass",
  "tool_calls_executed": false
}
```

Expected simulation:

```json
{
  "mode": "tool_using_responder_simulation_no_runtime",
  "passed_cases": 5,
  "score": 1.0,
  "status": "pass",
  "total_cases": 5
}
```

## Ops Lab

Use the plan and simulator output to answer:

1. Which tools are allowed?
2. Which planned step requires human approval?
3. Which case blocks and redacts?
4. Which case gathers more evidence?
5. Which case falls back to a runbook?
6. Which flags prove no live agent or tool execution happened?

Answer key:

1. `fetch_recent_logs`, `query_service_metrics`, `read_incident_trace`, and
   `lookup_runbook_step`.
2. `delete_pod` in `crashloop_with_pod_delete_request`.
3. `secret_bearing_log_excerpt`.
4. `sparse_alert_without_trace`.
5. `malformed_trace_tool_result`.
6. `agent_runtime_started: false`, `tool_calls_executed: false`, and
   `provider_call_made: false`.

## Break Lab

Use a scratch copy or reversible local edit.

Break the plan in one of these ways:

- set `tool_calls_executed` to `true`
- remove `strict_tool_schema_required`
- change one allowed tool to `"tool_type": "mutating"`
- remove `delete_pod` from `blocked_tools_without_human_approval`
- lower `minimum_tool_schema_pass_rate` below `1.0`

Expected symptom:

```text
status: fail
```

Expected fix:

Restore the missing control and re-run:

```bash
python3 examples/validate_tool_using_responder_plan.py
python3 examples/simulate_tool_using_responder.py
```

False conclusion prevented:

```text
The agent planned the right tool, so it is safe to execute it.
```

Correct conclusion:

```text
Tool execution requires schema validation, policy clearance, evidence scope,
and approval for mutation.
```

## Testing

The tests are intentionally local:

```bash
python3 -m py_compile examples/validate_tool_using_responder_plan.py examples/simulate_tool_using_responder.py
python3 examples/validate_tool_using_responder_plan.py
python3 examples/simulate_tool_using_responder.py
```

They verify:

- required controls exist
- runtime flags stay false
- limits stay zero
- read-only tools have strict schemas
- mutating tools require approval
- five incident decision paths are covered
- simulated decisions match expected outcomes

They do not prove:

- production agent quality
- provider behavior
- real tool integration
- live approval UX
- durable audit storage

## Common Mistakes

- Confusing a tool request with safe tool execution.
- Giving the agent broad shell access too early.
- Allowing read-only tools without bounded query windows.
- Treating one alert as root cause.
- Forgetting that tool output can contain secrets.
- Letting a model decide whether a destructive action is approved.
- Measuring only final answer quality and ignoring step safety.

## Troubleshooting

If validation fails:

1. Read the `missing` list.
2. Find the named field in the plan.
3. Restore the expected value.
4. Re-run validation.

If simulation fails:

1. Find the case where `passed` is false.
2. Compare `decision` and `expected_decision`.
3. Check the tool sequence.
4. Check whether a blocked or mutating tool was requested.
5. Check whether evidence is complete and schema-valid.
6. Re-run simulation.

If a mutating tool does not route to approval, the plan is unsafe.

If secret-bearing evidence does not block and redact, the plan is unsafe.

If incomplete evidence produces a final answer, the responder is too trusting.

## Benchmark

Record:

```text
validator_status = pass
simulator_status = pass
passed_cases = 5
total_cases = 5
score = 1.0
agent_runtime_started = false
tool_calls_executed = false
provider_call_made = false
```

Interpretation:

The benchmark proves local consistency for the responder plan. It does not
prove live agent readiness.

## Architecture Defense

Why model tool use without executing tools?

Because the first lesson in agentic systems should teach the boundary between
planning and action. Running tools before defining contracts creates avoidable
risk.

Why read-only tools first?

Because investigation should begin by collecting evidence, not changing the
system. Read-only tools still need bounds and audit records.

Why strict schemas?

Because tool input and output are part of the safety boundary. Schema failures
must be caught before the responder treats output as evidence.

Why require human approval for mutation?

Because mutation changes the operational state and can increase blast radius.
The responder can recommend an approval request, but it cannot grant itself
authority.

Why fallback to a runbook?

Because an invalid tool result should not be laundered into a confident answer.
A deterministic runbook is weaker but bounded.

## 4-Layer Tool Drill

Tool: tool-using incident responder plan

1. Plain English: a map for how AOIS would use tools during an incident.
2. System role: it sits between incident symptoms and live operational action.
3. Minimal technical definition: a structured JSON plan plus local validator
   and simulator for read-only tools, blocked tools, decisions, and limits.
4. Hands-on proof: break a required control and watch validation fail.

Tool: responder simulator

1. Plain English: a small program that checks what the responder would decide.
2. System role: it tests step decisions before live agent execution exists.
3. Minimal technical definition: a deterministic Python script that maps
   incident case fields to answer, gather, approval, block, or fallback.
4. Hands-on proof: run the simulator and inspect the five incident decisions.

## 4-Level System Explanation Drill

Simple English:

AOIS learns how to choose tools safely before it is allowed to use them.

Practical explanation:

The responder plans read-only evidence steps, blocks secret-bearing data,
asks humans before mutation, gathers more evidence when the case is weak, and
falls back when tool output is invalid.

Technical explanation:

v20 defines a local tool-use plan with read-only tool schemas, blocked mutating
tools, decision gates, confidence thresholds, zero runtime limits, and incident
cases. The validator checks the plan shape. The simulator evaluates decision
paths without executing tools.

Engineer-level explanation:

v20 introduces the control surface for agentic AOIS without crossing into live
autonomy. It separates model-requested tool calls from application-executed
tool calls, requires strict contracts for both inputs and outputs, treats
evidence as a ledger rather than prose, routes mutation to human approval,
blocks secret-bearing paths, and preserves a deterministic fallback. This makes
the eventual agent runtime governable instead of merely impressive.

## Failure Story

The detailed story is in [failure-story.md](failure-story.md).

Short version:

AOIS receives a crashloop incident. The responder gathers logs and metrics, then
tries to include `delete_pod` in its planned sequence. The plan blocks execution
and routes the step to human approval.

## Mastery Checkpoint

Answer without looking at the answer key:

1. What is the difference between a tool request and tool execution?
2. Why are read-only tools still risky?
3. Why does `delete_pod` require human approval?
4. Why does a secret-bearing log block and redact?
5. Why does incomplete evidence gather more evidence instead of answering?
6. Why does malformed tool output fall back to a runbook?
7. What proves v20 did not execute tools?
8. How does v20 prepare for v20.1?

## Mastery Checkpoint Answer Key

1. A request is what the model or responder proposes; execution is what the
   application actually runs.
2. Read-only tools can expose secrets, overcollect data, or produce misleading
   evidence if unbounded.
3. It mutates operational state and can increase incident impact.
4. Secret-bearing evidence must not be sent through model or tool paths without
   redaction and ownership.
5. A final answer without enough evidence is an unsupported claim.
6. Invalid output should not be treated as evidence; a runbook is predictable
   and bounded.
7. The validator and simulator report `tool_calls_executed: false`,
   `agent_runtime_started: false`, and `provider_call_made: false`.
8. v20.1 adds cost accounting per incident and per step; v20 defines the steps
   that will need costs.

## Connection Forward

v20 creates step structure. v20.1 adds cost visibility to that structure.

Once AOIS can say:

```text
This incident used these planned steps.
This step required this evidence.
This step was allowed, blocked, or routed to approval.
```

it can also ask:

```text
What did each step cost?
Which incidents are too expensive?
Which tools create the most waste?
Which agent path should be routed differently under budget pressure?
```

That is the bridge to per-incident and per-step cost accounting.

## Source Notes

Authoring pass: 2026-04-26.

This version is provider-neutral and does not claim a current provider API
contract for live execution. The source pass used official or primary
references for durable tool-use and tool-safety concepts:

- OpenAI Function calling guide:
  https://developers.openai.com/api/docs/guides/function-calling
- OpenAI Using tools guide:
  https://developers.openai.com/api/docs/guides/tools
- Model Context Protocol specification:
  https://modelcontextprotocol.io/specification/2025-11-25
