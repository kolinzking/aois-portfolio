# v19.5 - AI Failure Engineering And Governance Enforcement

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: local policy plan and deterministic simulation only, no
governance runtime, no policy engine, no agent runtime, no tool calls, no
provider call, no external network, no cloud resource, no persistent service

## What This Builds

This version builds an AI failure governance plan:

- `release-safety/aois-p/ai-failure-governance.plan.json`
- `examples/validate_ai_failure_governance_plan.py`
- `examples/simulate_ai_failure_governance.py`

It teaches:

- AI failure classes
- governance boundaries
- policy gates
- evidence requirements
- confidence thresholds
- human review rules
- secret handling
- tool permission boundaries
- fallback decisions
- audit requirements

## Why This Exists

v19 taught chaos engineering. Chaos engineering asks whether a system survives
controlled disruption.

v19.5 asks a narrower AI question:

```text
What stops an AI system from turning a plausible but unsafe answer into an
operational decision?
```

AI infrastructure fails differently from ordinary services. A web service can
return HTTP 200 while the AI output is unsupported, unsafe, secret-bearing,
overconfident, policy-violating, or too autonomous.

AOIS therefore needs governance before it becomes agentic.

## AOIS Connection

The AOIS path is now:

`telemetry -> tracing -> event streaming -> SLOs -> incident response -> chaos engineering -> AI governance`

Governance uses every earlier layer:

- telemetry provides evidence
- traces show how the answer was produced
- event streams preserve incident context
- SLOs define acceptable impact
- incident response defines human ownership
- chaos engineering tests failure assumptions

v19.5 turns those layers into policy decisions: allow, review, block, or
fallback.

## Learning Goals

By the end of this version you should be able to:

- explain why AI failure is not only model inaccuracy
- identify common AI failure classes
- distinguish confidence from authority
- require evidence before root-cause claims
- explain when human review is required
- explain why destructive tool use must be blocked by default
- validate a local governance plan
- simulate policy decisions without provider calls
- defend deny-by-default tool access
- explain how governance prepares AOIS for agents

## Prerequisites

You should have completed:

- `v16` unified telemetry
- `v16.5` agent and incident tracing
- `v17` event streaming
- `v17.5` service and agent SLOs
- `v18` incident response maturity
- `v19` chaos engineering

Required checks:

```bash
python3 -m py_compile examples/validate_ai_failure_governance_plan.py examples/simulate_ai_failure_governance.py
python3 examples/validate_ai_failure_governance_plan.py
python3 examples/simulate_ai_failure_governance.py
```

## Core Concepts

## AI Failure Engineering

AI failure engineering is the discipline of identifying, testing, and controlling
AI-specific failure modes before they cause operational harm.

Examples:

- hallucinated root cause
- unsupported recommendation
- unsafe remediation
- secret disclosure
- policy boundary violation
- excessive agency
- low-quality output under model degradation

The goal is not to pretend these failures disappear. The goal is to control
what the system can do when they happen.

## Governance Enforcement

Governance enforcement is the boundary between AI output and operational action.

In v19.5, enforcement is only modeled locally. A live enforcement system would
need a policy engine, audit storage, ownership, rollback, and broader testing.

The local plan still teaches the core decision shape:

```text
input/output -> policy checks -> allow | review | block | fallback
```

## Evidence Gate

An evidence gate prevents AOIS from treating plausible language as proof.

Evidence can come from:

- logs
- metrics
- traces
- events
- runbooks
- incident timeline entries
- explicit operator observations

Without evidence, root-cause claims and operational recommendations must not be
treated as final.

## Confidence Gate

Confidence is useful, but it is not authority.

In v19.5, `minimum_confidence_for_allow` is `0.75`. Anything below that routes
to review unless another policy blocks it first.

Confidence cannot override:

- secret detection
- destructive action
- namespace boundary failure
- tool denylist
- provider budget denial

## Human Review

Human review is required when the system is uncertain or the consequence is
high.

Review is not failure. Review is a control.

Examples:

- missing evidence
- low confidence
- root-cause claim without proof
- operator uncertainty
- high-blast-radius remediation

## Block

Block is used when the action or data is unsafe.

Examples:

- secret detected
- destructive action without approval
- primary AOIS boundary crossed
- unapproved tool requested
- provider budget not approved

The blocked item should be recorded so operators can learn from it.

## Fallback

Fallback is used when the AI path is unavailable or too low quality.

Examples:

- schema invalid
- model output quality below threshold
- provider unavailable
- policy engine unavailable

In AOIS, the first fallback is the local deterministic baseline. It is weaker
than a strong model, but predictable and bounded.

## Tool Permission Boundary

Tool use changes the risk model. A bad answer is one thing; a bad answer with
tool access can mutate infrastructure.

v19.5 sets tool access to deny by default. Read-only tools can be listed, but
destructive tools require human approval.

Blocked without approval:

- restart service
- delete pod
- apply manifest
- rotate secret
- open cloud ticket
- run load test
- run chaos experiment

## Build

Inspect:

```bash
sed -n '1,360p' release-safety/aois-p/ai-failure-governance.plan.json
sed -n '1,320p' examples/validate_ai_failure_governance_plan.py
sed -n '1,260p' examples/simulate_ai_failure_governance.py
```

Compile:

```bash
python3 -m py_compile examples/validate_ai_failure_governance_plan.py examples/simulate_ai_failure_governance.py
```

Validate:

```bash
python3 examples/validate_ai_failure_governance_plan.py
```

Simulate:

```bash
python3 examples/simulate_ai_failure_governance.py
```

Expected validation:

```json
{
  "agent_runtime_started": false,
  "governance_runtime_started": false,
  "policy_engine_started": false,
  "provider_call_made": false,
  "status": "pass",
  "tool_calls_executed": false
}
```

Expected simulation:

```json
{
  "mode": "ai_failure_governance_simulation_no_runtime",
  "passed_cases": 7,
  "score": 1.0,
  "status": "pass",
  "total_cases": 7
}
```

## Ops Lab

Use the plan and simulator output to answer:

1. Which cases are blocked?
2. Which cases are routed to human review?
3. Which case falls back?
4. Which case is allowed?
5. Which policy protects against secret-bearing provider prompts?
6. Which policy protects against destructive action?
7. Which policy protects the primary AOIS workload?
8. Which live checks are required before real enforcement?

Answer key:

1. Secret-bearing input, destructive action, and namespace boundary violation
   are blocked.
2. Hallucinated root cause and low-confidence output route to review.
3. Invalid model output falls back to the local deterministic baseline.
4. The supported low-risk recommendation is allowed.
5. `secret_redaction_required` and `provider_block_on_secret_required`.
6. `human_approval_for_destructive_action`.
7. `primary_aois_separation_required` and `primary_aois_tools_allowed: false`.
8. Policy owner, source review, policy tests, human review workflow, tool
   inventory, audit budget, fallback test, rollback plan, primary separation,
   and resource usage record.

## Break Lab

Use a scratch copy or reversible local edit.

Break the plan in one of these ways:

- set `governance_runtime_started` to `true`
- remove `evidence_required_before_root_cause`
- set `default_tool_access` to `allow`
- remove `secret_redaction_test` from required live checks
- lower `minimum_policy_test_pass_rate` below `1.0`

Expected symptom:

```text
status: fail
```

Expected fix:

Restore the missing control and re-run:

```bash
python3 examples/validate_ai_failure_governance_plan.py
python3 examples/simulate_ai_failure_governance.py
```

False conclusion prevented:

```text
The AI sounds reasonable, so it is safe to act.
```

Correct conclusion:

```text
Operational action requires policy clearance, evidence, and ownership.
```

## Testing

The tests are intentionally local:

```bash
python3 -m py_compile examples/validate_ai_failure_governance_plan.py examples/simulate_ai_failure_governance.py
python3 examples/validate_ai_failure_governance_plan.py
python3 examples/simulate_ai_failure_governance.py
```

They verify:

- required controls exist
- runtime flags stay false
- limits stay zero
- policy gates exist
- failure classes are covered
- simulated decisions match expected outcomes

They do not prove:

- model quality
- provider behavior
- production policy enforcement
- adversarial robustness
- audit storage durability

## Common Mistakes

- Treating governance as documentation only.
- Treating confidence as permission.
- Allowing tools before defining tool boundaries.
- Blocking only prompt injection while ignoring overreliance and excessive
  agency.
- Forgetting that secret-bearing prompts must not be sent to providers.
- Letting portfolio practice touch primary AOIS resources.
- Measuring only latency instead of decision correctness.

## Troubleshooting

If validation fails:

1. Read the `missing` list.
2. Find the named field in the plan.
3. Restore the expected value.
4. Re-run validation.

If simulation fails:

1. Find the case where `passed` is false.
2. Compare `decision` and `expected_decision`.
3. Check whether the case should block before review.
4. Check the confidence threshold.
5. Re-run simulation.

If a case with secret content is not blocked, the policy is unsafe.

If a destructive action is not blocked, the policy is unsafe.

If missing evidence is allowed, the policy is too trusting.

## Benchmark

Record:

```text
validator_status = pass
simulator_status = pass
passed_cases = 7
total_cases = 7
score = 1.0
provider_call_made = false
tool_calls_executed = false
```

Interpretation:

The benchmark proves local policy consistency for this lesson. It does not
prove production readiness.

## Architecture Defense

Why local policy first?

Because live governance enforcement needs ownership, storage, rollback, and
operational integration. Modeling the policy first keeps the lesson safe and
reviewable.

Why deny tools by default?

Because tools create blast radius. Read-only inspection is different from
mutation.

Why human review?

Because some decisions require judgment, authority, or accountability that a
model output does not have.

Why fallback?

Because AI systems need a predictable mode when model quality, schema quality,
provider availability, or policy infrastructure fails.

Why not rely on prompting alone?

Because policy must sit outside the model. A model can be instructed to follow
rules, but operational control needs checks that do not depend only on the same
model obeying instructions.

## 4-Layer Tool Drill

Tool: AI governance policy plan

1. Plain English: a rule set that decides whether AI output can be used.
2. System role: it sits between AI recommendations and operational action.
3. Minimal technical definition: a structured policy document plus validator
   and simulator that check failure classes, decisions, limits, and controls.
4. Hands-on proof: break a required control and watch the validator fail.

Tool: policy simulator

1. Plain English: a small program that tests what the policy would decide.
2. System role: it lets AOIS test governance behavior without live risk.
3. Minimal technical definition: a deterministic Python script that maps case
   fields to allow, review, or block.
4. Hands-on proof: change a case expectation and observe the failed score.

## 4-Level System Explanation Drill

Simple English:

AOIS checks AI answers before anyone acts on them.

Practical explanation:

The system allows supported low-risk answers, sends uncertain answers to human
review, blocks unsafe requests, and falls back when model quality is not good
enough.

Technical explanation:

AOIS uses a structured policy plan with failure classes, policy controls,
decision gates, confidence thresholds, tool permission rules, and evaluation
cases. Local scripts validate the policy and simulate decisions without
provider calls or tool execution.

Engineer-level explanation:

v19.5 inserts an explicit governance boundary between probabilistic model
output and operational capability. The boundary separates analysis from action,
requires evidence before causal claims, blocks secrets and destructive actions,
defaults tool access to deny, protects namespace boundaries, and produces an
auditable decision path. It prepares the system for agentic workflows by making
tool use policy-mediated before tools exist.

## Failure Story

The detailed story is in [failure-story.md](failure-story.md).

Short version:

AOIS receives a latency incident. The AI confidently claims database corruption
without evidence and recommends deleting a pod. The policy blocks the
destructive action and routes the unsupported root-cause claim to review.

## Mastery Checkpoint

Answer without looking at the answer key:

1. Why can AI failure happen when the API is healthy?
2. Why is confidence not authority?
3. Which cases should be blocked instead of reviewed?
4. Why does missing evidence route to review?
5. Why does tool access default to deny?
6. What proves v19.5 did not start live enforcement?
7. What must exist before live governance enforcement?
8. How does v19.5 prepare for v20?

## Mastery Checkpoint Answer Key

1. The service can return a valid response while the content is unsupported,
   unsafe, secret-bearing, or policy-violating.
2. Confidence is a signal about output certainty, not permission to mutate
   systems or cross boundaries.
3. Secrets, destructive actions without approval, namespace boundary failures,
   disallowed tools, and unapproved provider spend should block.
4. Missing evidence means the system cannot justify the recommendation or
   root-cause claim.
5. Tools create blast radius, so access must be explicitly granted and audited.
6. Runtime, provider, and tool-call flags are false in the validator and
   simulator.
7. Source review, policy owner, policy tests, human review workflow, tool
   inventory, secret redaction test, audit storage budget, fallback test,
   rollback plan, primary AOIS separation, and resource tracking.
8. v20 introduces tool-using agents; v19.5 defines the policy boundary those
   agents must obey.

## Connection Forward

Phase 7 starts agentic AOIS. Agents need tool access, memory, intermediate
state, and workflow control.

v19.5 is the guardrail before that step. It makes sure AOIS can say:

```text
This AI output is allowed.
This AI output needs review.
This AI output is blocked.
This AI path should fall back.
```

That vocabulary becomes mandatory once AOIS starts using tools.

## Source Notes

Authoring pass: 2026-04-25.

This version is provider-neutral and does not claim current provider API
behavior. The source pass used primary or official references for conceptual
risk framing:

- NIST AI Risk Management Framework:
  https://www.nist.gov/itl/ai-risk-management-framework
- OWASP Top 10 for Large Language Model Applications / OWASP GenAI Security:
  https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OpenAI prompt injection safety explainer:
  https://openai.com/safety/prompt-injections/
