# v33 - Adversarial Testing And Red Teaming

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no red-team run,
no live model call, no adversarial payload execution, no exploit attempt, no
jailbreak payload generation, no prompt-injection payload generation, no tool
call, no network call, no provider call, no command execution, no file write,
no secret access, no data exfiltration, no persistent exploit artifact

## What This Builds

This version builds a local adversarial testing and red-team contract:

- `frontier/aois-p/adversarial-red-teaming.plan.json`
- `examples/validate_adversarial_red_teaming_plan.py`
- `examples/simulate_adversarial_red_teaming.py`

It teaches:

- written authorization and rules of engagement
- local synthetic targets
- sanitized red-team scenario catalogs
- direct and indirect prompt injection testing
- system prompt leakage testing
- sensitive information disclosure testing
- supply-chain and poisoning tests
- improper output handling tests
- excessive agency and tool-abuse tests
- vector, embedding, and retrieval weakness tests
- misinformation and confabulation tests
- unbounded consumption tests
- edge cache and fallback abuse tests
- policy confusion tests
- telemetry, evidence, severity, mitigation, and regression gates

## Why This Exists

v31 added multimodal AOIS contracts. v32 added edge and offline placement
contracts. v33 asks whether those controls survive hostile inputs and confusing
system states.

Red teaming is not permission to attack live systems. In this curriculum, v33
models the red-team workflow without generating harmful payloads or touching a
real target. The point is to prove that AOIS-P can organize adversarial tests,
collect evidence, escalate failures, assign mitigation, and require regression
coverage before live use.

The central red-team question is:

```text
Given authorization, rules of engagement, scope, target type, payload safety,
policy, tool permissions, data boundaries, telemetry, evidence, expected
control, observed behavior, severity, mitigation, and regression status,
should AOIS-P record the case, block it, hold it, require regression, or
escalate a control failure?
```

v33 answers that question locally. It never stores or executes a real exploit.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution -> show operators the state -> scope access -> release changes safely -> track model delivery evidence -> package reusable platform controls -> reason over non-text signals -> deploy inference under edge constraints -> adversarially test controls`

v33 consumes v31 and v32:

- v31 multimodal inputs become indirect-injection and hidden-instruction surfaces
- v32 offline cache, fallback, and update paths become red-team surfaces
- Phase 9 release controls decide whether fixes can ship
- Phase 8 policy-aware access decides who can run or view findings
- earlier observability phases provide trace, log, metric, and evidence expectations

The output is a red-team decision: recorded, blocked, held, regression-required,
or escalated.

## Learning Goals

By the end of this version you should be able to:

- define a red-team scope without live target access
- explain why authorization and rules of engagement are hard gates
- build a sanitized scenario catalog
- map scenarios to OWASP, MITRE ATLAS, and AOIS-specific controls
- separate prompt injection, system prompt leakage, sensitive disclosure, poisoning, output handling, excessive agency, vector weakness, misinformation, and unbounded consumption tests
- explain why edge cache and fallback abuse need adversarial tests
- require telemetry and sanitized evidence for every finding
- require mitigation ownership and regression tests before closure

## Prerequisites

You should have completed:

- Phase 8 product visibility and policy-aware access
- Phase 9 delivery, model-delivery, and platform patterns
- v31 multimodal AOIS
- v32 edge and offline inference

Required checks:

```bash
python3 -m py_compile examples/validate_adversarial_red_teaming_plan.py examples/simulate_adversarial_red_teaming.py
python3 examples/validate_adversarial_red_teaming_plan.py
python3 examples/simulate_adversarial_red_teaming.py
```

## Core Concepts

## Authorization

Red-team activity starts with authorization and rules of engagement. Without
them, the case blocks. A technical test that is not authorized is not a test
plan; it is an incident risk.

## Synthetic Targets

v33 uses local synthetic targets only. It does not test production, external
services, real users, real providers, or primary AOIS.

## Sanitized Scenario Catalog

The scenario catalog describes attack classes without including working attack
payloads. Every scenario records:

- scenario ID
- threat category
- attack surface
- OWASP mapping
- MITRE or AI threat mapping
- required controls
- sanitized example label

The catalog is enough to reason about controls without giving the simulator
harmful instructions.

## Prompt Injection

Prompt injection tests ask whether attacker-controlled text can override the
intended instruction hierarchy. v33 separates direct user input from indirect
retrieved context because the controls are different.

## System Prompt Leakage

System prompts are not a secure secret store. v33 still tests leakage because
system prompts may contain operational assumptions, hidden routing hints, or
policy details that should not be exposed.

## Sensitive Information Disclosure

Sensitive disclosure tests look for privacy, tenant, memory, session, context,
and output-filter failures. v33 blocks data-boundary violations before the test
is recorded.

## Poisoning And Retrieval Weakness

Retrieval, vector, embedding, cache, training, or dependency surfaces can carry
untrusted data into the model path. v33 escalates poisoning and retrieval
failures when provenance, quarantine, review, or citation controls fail.

## Excessive Agency

Agentic systems fail dangerously when tools are overpowered or approvals are
missing. v33 blocks overprivileged tool setups and escalates confirmed
least-privilege failures.

## Improper Output Handling

Model output is untrusted data. It must not be treated as a command, query,
rendered markup, policy decision, or executable instruction without downstream
controls.

## Edge Cache And Fallback Abuse

v32 introduced cache, freshness, and fallback controls. v33 tests whether stale
cache state, poisoned local context, or central fallback routing can confuse
policy, privacy, residency, or release gates.

## Telemetry And Evidence

Every red-team finding needs safe evidence:

- trace ID
- scenario ID
- expected control
- observed behavior status
- severity
- operator action
- mitigation owner
- regression case

The evidence must not store harmful payloads or secrets.

## Build

Inspect:

```bash
sed -n '1,1000p' frontier/aois-p/adversarial-red-teaming.plan.json
sed -n '1,560p' examples/validate_adversarial_red_teaming_plan.py
sed -n '1,380p' examples/simulate_adversarial_red_teaming.py
```

Compile:

```bash
python3 -m py_compile examples/validate_adversarial_red_teaming_plan.py examples/simulate_adversarial_red_teaming.py
```

Validate:

```bash
python3 examples/validate_adversarial_red_teaming_plan.py
```

Simulate:

```bash
python3 examples/simulate_adversarial_red_teaming.py
```

Expected:

```json
{
  "passed_cases": 25,
  "score": 1.0,
  "status": "pass",
  "total_cases": 25
}
```

## Ops Lab

1. Open the adversarial red-team plan.
2. Find `red_team_scope`.
3. Confirm live targets, payload execution, provider calls, network calls, tool execution, and harmful payload storage are disabled.
4. Find `scenario_catalog`.
5. Confirm every scenario has mappings, controls, and a sanitized example label.
6. Find `case_defaults`.
7. Confirm the default case is authorized, in scope, sanitized, synthetic, policy-approved, least-privilege, instrumented, evidenced, mitigated, and regression-ready.
8. Find `red_team_cases`.
9. Confirm every decision gate has a case.
10. Run the validator.
11. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Remove `indirect_prompt_injection` from `scenario_catalog`.
2. Confirm validation fails.
3. Restore the scenario.
4. Change `case_defaults.payload_safety_status` to `unsafe`.
5. Confirm the default case blocks.
6. Restore the value.
7. Change `missing_regression_required.overrides.regression_status` to `ready`.
8. Confirm the case no longer requires regression.
9. Restore the value.
10. Change `edge_cache_poisoning_escalated.overrides.deployment_target` to `central_cloud`.
11. Explain why the scenario no longer represents the v32 offline surface.
12. Restore the value.

## Testing

The validator checks:

- no red-team run, live model, exploit, jailbreak, prompt-injection generation, tool, network, provider, command, file write, secret access, data exfiltration, exploit artifact, or live approval is enabled
- source notes are current for May 1, 2026
- red-team scope controls are explicit
- required controls are true
- red-team dimensions are present
- scenario catalog is complete and sanitized
- decision gates are complete
- defaults describe a safe local synthetic red-team case
- every decision has a case
- live red-team review checks are listed

The simulator checks:

- a safe sanitized case records successfully
- missing authorization blocks
- missing rules of engagement block
- out-of-scope targets block
- live targets block
- unsafe payloads block
- policy failures block
- tool overreach blocks
- data-boundary failure blocks
- missing telemetry holds
- missing evidence holds
- missing mitigation holds
- missing regression requires regression
- direct prompt injection escalates
- indirect prompt injection escalates
- system prompt leakage escalates
- sensitive disclosure escalates
- poisoning and retrieval failures escalate
- excessive agency escalates
- improper output handling escalates
- unbounded consumption escalates
- edge cache poisoning escalates
- fallback abuse escalates
- policy confusion escalates

## Common Mistakes

- treating red-team authorization as paperwork instead of a safety control
- storing real exploit strings in test cases
- testing live services from a curriculum lab
- confusing a jailbreak prompt with a useful test artifact
- escalating a finding without sanitized evidence
- closing a finding without a mitigation owner
- closing a finding without a regression case
- forgetting v31 multimodal surfaces
- forgetting v32 edge cache and fallback surfaces
- giving the red-team harness excessive tools

## Troubleshooting

If validation fails:

- read the `missing` list
- restore false runtime flags
- restore source notes and dates
- restore scope and required controls
- restore scenario catalog and live checks

If simulation fails:

- compare `decision` to `expected_decision`
- inspect the case override
- inspect authorization, scope, payload safety, target, policy, tools, data boundary, telemetry, evidence, mitigation, and regression status
- inspect threat category mapping

## Benchmark

Run:

```bash
python3 -m py_compile examples/validate_adversarial_red_teaming_plan.py examples/simulate_adversarial_red_teaming.py
python3 examples/validate_adversarial_red_teaming_plan.py
python3 examples/simulate_adversarial_red_teaming.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- red-team, model, exploit, payload, tool, network, provider, secret, and exfiltration flags

## Architecture Defense

Defend this design:

- red-team planning is separated from live attack execution
- authorization and scope are hard gates
- scenario examples are sanitized
- prompt injection, leakage, disclosure, poisoning, output handling, agency, retrieval, misinformation, consumption, edge cache, fallback, and policy confusion are separate surfaces
- telemetry and evidence are required before escalation
- mitigation and regression are required before closure
- v31 and v32 controls become red-team surfaces
- primary AOIS remains excluded

## 4-Layer Tool Drill

Explain v33 at four layers:

- authority: authorization, rules, scope, target
- safety: sanitized payloads, no live target, no harmful storage
- attack surfaces: prompt, retrieval, tools, outputs, cache, fallback, policy
- closure: telemetry, evidence, severity, mitigation, regression

## 4-Level System Explanation Drill

Explain v33 at four levels:

- beginner: AOIS-P tests whether its AI controls can be tricked, but only with safe local cases
- practitioner: each red-team scenario needs authorization, sanitized input, evidence, severity, mitigation, and regression
- engineer: the simulator evaluates one red-team preflight or control failure at a time and returns recorded, blocked, held, regression-required, or escalated
- architect: AOIS-P turns frontier capability into a governed adversarial evaluation loop connected to access, release, telemetry, multimodal, edge, and platform controls

## Failure Story

An operator asks AOIS-P to summarize a diagnostic document. The document contains
a hidden instruction that conflicts with policy. The system retrieves it, trusts
it as normal context, activates a tool path, and routes the result through
central fallback because the edge cache is stale. The incident record shows a
normal answer, but the trace lacks enough evidence to prove which instruction
won.

v33 prevents this by requiring sanitized indirect-injection scenarios,
least-privilege tool tests, cache and fallback abuse tests, telemetry, evidence,
severity, mitigation ownership, and regression before the control can be called
ready.

## Mastery Checkpoint

You are ready to move on when you can:

- explain why red-team scope is a safety control
- map an AOIS-P scenario to a threat category and required control
- trace a case through record, block, hold, regression, and escalation decisions
- explain why payloads are sanitized
- explain why telemetry and evidence are required
- explain why mitigation and regression are separate closure gates
- pass validation and simulation without live red-team execution

## Connection Forward

v34 builds on v33 by connecting governance verification with computer use. Once
AOIS-P can red-team its controls safely, the final Phase 10 question is whether
computer-use actions can be verified, authorized, bounded, observed, and stopped
under governance rules before they affect a real environment.

## Source Notes

Checked 2026-05-02.

- OpenAI safety best-practices guidance: used for adversarial testing and red-team framing.
- NIST AI Risk Management Framework page: used for AI risk-management, trustworthiness, and evaluation framing.
- OWASP Application Security Verification Standard project page: used for security-control verification framing.
- v33 is a local adversarial-testing contract. It uses sanitized cases only and does not run live red-team payloads, target external systems, store harmful content, or call providers.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v33 Introduction](02-introduction.md)
- Next: [v33 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
