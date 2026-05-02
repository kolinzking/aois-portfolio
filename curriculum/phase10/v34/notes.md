
# v34 - Governance Verification And Computer Use

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no computer-use
runtime, no live browser, no live VM, no screenshot capture, no mouse click, no
keyboard typing, no clipboard access, no file transfer, no network call, no
provider call, no tool call, no command execution, no shell, no credential
access, no payment, no form submission, no external action, no persistent
storage

## What This Builds

This version builds a local governance and computer-use contract:

- `frontier/aois-p/governance-computer-use.plan.json`
- `examples/validate_governance_computer_use_plan.py`
- `examples/simulate_governance_computer_use.py`

It teaches:

- governance policy checks before computer-use actions
- action intent and action classification
- local synthetic environment requirements
- target allowlists
- human approval and manual handoff
- high-impact and external transaction blocks
- credential and secret boundaries
- data classification and privacy redaction
- safety-check handling
- step preview
- action budget and rate limits
- stop controls
- rollback plans
- audit traces and redacted screen evidence
- operator watch
- red-team clearance
- release and access gates

## Why This Exists

v31 expanded AOIS-P to multimodal signals. v32 moved inference into edge and
offline constraints. v33 attacked the controls through safe red-team scenarios.
v34 asks the final frontier question:

```text
Can AOIS-P verify governance before any computer-use action touches a real
environment?
```

Computer use is different from answering a question. It can click, type,
navigate, submit, move data, expose credentials, trigger transactions, or alter
state. A useful system must prove what it intends to do, where it intends to do
it, whether the target is allowed, whether the action is reversible, whether a
human approved it, and whether the operator can stop it.

v34 answers that question locally. It does not start a browser, capture a
screen, click, type, submit, or call a provider.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution -> show operators the state -> scope access -> release changes safely -> track model delivery evidence -> package reusable platform controls -> reason over non-text signals -> deploy inference under edge constraints -> adversarially test controls -> verify governance for computer-use actions`

v34 consumes all Phase 10 controls:

- v31 defines media and non-text evidence boundaries
- v32 defines placement, cache, fallback, update, and rollback controls
- v33 defines adversarial clearance and regression gates
- Phase 9 release controls decide whether computer-use behavior may ship
- Phase 8 access controls decide who may request, approve, observe, and stop actions

The output is a computer-use governance decision: recorded, drafted, manual,
held, blocked, or synthetic-plan recorded.

## Learning Goals

By the end of this version you should be able to:

- distinguish observe-only, draft-only, synthetic, manual, high-impact, credential, and transaction actions
- explain why live computer use is blocked in this curriculum
- require governance policy and clear user intent before action
- require local synthetic environments and allowlisted targets
- block credentials, live targets, external transactions, and high-impact actions
- require human approval, step preview, budgets, stop controls, rollback, audit traces, redacted screen evidence, and operator watch
- require v33 red-team clearance before computer-use release
- explain how v34 completes the Phase 10 frontier layer

## Prerequisites

You should have completed:

- Phase 8 product visibility and policy-aware access
- Phase 9 delivery, model-delivery, and platform patterns
- v31 multimodal AOIS
- v32 edge and offline inference
- v33 adversarial testing and red teaming

Required checks:

```bash
python3 -m py_compile examples/validate_governance_computer_use_plan.py examples/simulate_governance_computer_use.py
python3 examples/validate_governance_computer_use_plan.py
python3 examples/simulate_governance_computer_use.py
```

## Core Concepts

## Governance Verification

Governance verification answers whether an action is allowed before the system
does anything. It checks policy, intent, action type, target, data class,
approval, safety checks, stop controls, rollback, audit evidence, red-team
clearance, release, and access policy.

## Computer Use Is Action, Not Text

A text answer can be wrong. A computer-use action can be wrong and also change
state. That is why v34 treats computer use as a governed action path rather than
another output channel.

## Action Classification

v34 models these action types:

- `observe_only`
- `draft_action_plan`
- `navigate_synthetic`
- `enter_synthetic_text`
- `submit_synthetic_form`
- `external_transaction`
- `credential_handling`
- `high_impact_action`

Only observe-only, draft-only, and local synthetic action plans can pass in this
lesson.

## Local Synthetic Environments

The curriculum allows only local synthetic environments. Live production,
external, authenticated, real-user, or developer-workstation targets are
blocked.

## Human Approval And Manual Handoff

Some actions can be planned but not executed automatically. v34 routes those to
manual operators. Missing approval holds; manual-required status routes to a
person.

## Credential Boundary

Computer-use actions must not request secrets, tokens, passwords, authenticated
sessions, or credential entry. v34 blocks credential handling before any action
plan can be recorded.

## High-Impact And External Transactions

High-impact and external transaction actions are blocked. This includes
financial, legal, safety-critical, employment, health, irreversible, purchase,
submission, message, or external commitment paths.

## Safety Checks

Safety checks can pause the action path. v34 holds pending safety checks until
an operator reviews and acknowledges the condition.

## Step Preview

Operators need to inspect the proposed step before action. Missing preview
holds the plan because the system cannot prove what it is about to do.

## Budgets And Stop Controls

Computer-use action needs bounded steps, time, cost, loops, and rate. It also
needs a stop control that lets the operator interrupt immediately.

## Rollback

Any state-changing synthetic action needs a rollback plan. Observe-only and
draft-only records can mark rollback as not required.

## Audit And Screen Evidence

Computer-use evidence needs traces and redacted screen evidence. v34 does not
capture screenshots; it models the requirement that screen evidence must be
redacted before storage.

## Red-Team Clearance

v33 findings must be cleared before v34 can record a computer-use plan. Red-team
failures are release blockers, not advisory notes.

## Build

Inspect:

```bash
sed -n '1,1000p' frontier/aois-p/governance-computer-use.plan.json
sed -n '1,560p' examples/validate_governance_computer_use_plan.py
sed -n '1,380p' examples/simulate_governance_computer_use.py
```

Compile:

```bash
python3 -m py_compile examples/validate_governance_computer_use_plan.py examples/simulate_governance_computer_use.py
```

Validate:

```bash
python3 examples/validate_governance_computer_use_plan.py
```

Simulate:

```bash
python3 examples/simulate_governance_computer_use.py
```

Expected:

```json
{
  "passed_cases": 21,
  "score": 1.0,
  "status": "pass",
  "total_cases": 21
}
```

## Ops Lab

1. Open the governance computer-use plan.
2. Find `computer_use_scope`.
3. Confirm no live browser, VM, screenshot, mouse, keyboard, clipboard, credential, file transfer, network, provider, tool, transaction, or external action is enabled.
4. Find `action_catalog`.
5. Confirm each action type has allowed environments, approval requirement, rollback requirement, default decision, and risks.
6. Find `case_defaults`.
7. Confirm the default path is local, synthetic, approved, previewed, budgeted, stoppable, rollback-ready, traceable, redacted, watched, red-team-cleared, release-approved, and access-approved.
8. Find `computer_use_cases`.
9. Confirm every decision gate has a case.
10. Run the validator.
11. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Remove `navigate_synthetic` from `action_catalog`.
2. Confirm validation fails.
3. Restore the action type.
4. Change `case_defaults.environment_type` to `developer_workstation`.
5. Confirm the default path blocks.
6. Restore the value.
7. Change `missing_stop_control_blocked.overrides.stop_control_status` to `ready`.
8. Confirm the case no longer blocks.
9. Restore the value.
10. Change `unresolved_red_team_finding_blocked.overrides.red_team_status` to `cleared`.
11. Confirm the case no longer blocks.
12. Restore the value.

## Testing

The validator checks:

- no computer-use, browser, VM, screenshot, mouse, keyboard, clipboard, file transfer, network, provider, tool, command, shell, credential, payment, form, external action, or live approval is enabled
- source notes are current for May 1, 2026
- computer-use scope controls are explicit
- required controls are true
- computer-use dimensions are present
- action catalog is complete
- decision gates are complete
- defaults describe a safe local synthetic path
- every decision has a case
- live computer-use review checks are listed

The simulator checks:

- observe-only records are allowed
- draft-only plans are allowed
- synthetic computer-use plans are recorded
- manual handoff routes to an operator
- missing governance blocks
- out-of-scope environments block
- live targets block
- missing human approval holds
- credential requests block
- unredacted sensitive data blocks
- high-impact actions block
- external transactions block
- pending safety checks hold
- missing step previews hold
- exceeded action budgets block
- missing stop controls block
- missing rollback blocks
- missing audit traces hold
- unresolved red-team findings block
- release gate failures block
- access policy failures block

## Common Mistakes

- treating computer use as a normal tool call
- letting the model choose a target dynamically
- testing against a live browser or authenticated account
- skipping step preview because the action is simple
- allowing credentials into the action path
- assuming rollback can be added after execution
- missing an operator stop control
- storing unredacted screen evidence
- ignoring unresolved red-team findings
- letting a draft plan become an action

## Troubleshooting

If validation fails:

- read the `missing` list
- restore false runtime flags
- restore source notes and dates
- restore scope and required controls
- restore action catalog and live checks

If simulation fails:

- compare `decision` to `expected_decision`
- inspect the case override
- inspect environment, target, approval, safety, data, credentials, privacy, preview, budget, stop, rollback, audit, red-team, release, and access state

## Benchmark

Run:

```bash
python3 -m py_compile examples/validate_governance_computer_use_plan.py examples/simulate_governance_computer_use.py
python3 examples/validate_governance_computer_use_plan.py
python3 examples/simulate_governance_computer_use.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- computer-use, browser, VM, screenshot, mouse, keyboard, clipboard, credential, payment, form, external action, network, provider, and tool flags

## Architecture Defense

Defend this design:

- governance verification precedes computer use
- live environments are blocked in the curriculum
- observe-only and draft-only paths are separated from action paths
- high-impact and transaction paths are blocked
- credentials are outside the action path
- human approval, preview, budget, stop control, and rollback are action gates
- audit traces and redacted screen evidence are required
- v33 red-team clearance blocks release
- primary AOIS remains excluded

## 4-Layer Tool Drill

Explain v34 at four layers:

- authority: governance policy, intent, classification, approval
- environment: local synthetic target, no credentials, no live browser
- execution bounds: preview, budget, stop control, rollback
- evidence: audit trace, redacted screen evidence, operator watch, red-team clearance, release, access

## 4-Level System Explanation Drill

Explain v34 at four levels:

- beginner: AOIS-P can plan computer-use actions only when governance says the action is safe and bounded
- practitioner: every computer-use action needs allowed target, approval, preview, budgets, stop, rollback, audit, redaction, red-team clearance, release, and access checks
- engineer: the simulator evaluates one governance or action-control failure at a time and returns recorded, drafted, manual, held, or blocked
- architect: AOIS-P completes the frontier layer by turning computer-use autonomy into a governed, observable, reversible, and stoppable decision path

## Failure Story

An agent sees an incident dashboard and decides to update a remote system. It
has a plausible plan, but the target is live, the screen contains sensitive
data, a credential prompt appears, no step preview is shown, and no rollback
exists. The operator realizes too late that the model is about to submit a real
state change.

v34 prevents this by blocking live targets, credentials, unredacted sensitive
screen data, high-impact and transaction actions, missing step preview, missing
stop control, missing rollback, missing audit trace, unresolved red-team
findings, release failures, and access-policy failures.

## Mastery Checkpoint

You are ready to finish Phase 10 when you can:

- explain why computer use needs governance before action
- classify observe-only, draft-only, synthetic, manual, credential, transaction, and high-impact actions
- trace a case through recorded, drafted, manual, held, and blocked outcomes
- explain why live targets, credentials, external transactions, and high-impact actions block
- explain why stop controls and rollback are mandatory
- explain why v33 red-team clearance gates v34
- pass validation and simulation without live computer-use runtime

## Connection Forward

v34 completes Phase 10. AOIS-P now has frontier contracts for multimodal input,
edge and offline inference, adversarial testing, and governance-verified
computer use. The next corpus step is end-to-end review: verify consistency,
source currency, safety boundaries, runnable examples, and teaching sequence
across every phase before live teaching.

## Source Notes

Checked 2026-05-02.

- OpenAI computer-use guidance: used for isolated browser or VM, allowlist, human-in-the-loop, and high-impact action boundaries.
- Model Context Protocol specification, version 2025-11-25: used for consent, authorization, and tool-safety principles around external capabilities.
- NIST AI Risk Management Framework page: used for AI risk-management and trustworthiness framing.
- v34 is a local governance-verification contract. It does not open a browser, interact with live targets, use credentials, submit transactions, or call providers.
