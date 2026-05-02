# v12 - Managed Runtime Governance Without Cloud Calls

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: governance plan and validation only, no managed cluster, no credentials, no provider calls

## What This Builds

This version builds a managed-runtime governance plan:

- `cloud/aws/managed-runtime-governance.plan.json`
- `examples/validate_managed_runtime_governance_plan.py`

It teaches:

- managed Kubernetes planning
- workload identity boundaries
- least privilege IAM
- observability requirements
- cost controls
- capacity and rollback planning
- separation from the primary AOIS project

## Why This Exists

Managed cloud runtimes can make infrastructure easier to create, but easier creation is not the same as safer operation.

AOIS needs to understand the governance layer before any managed runtime exists.

The key question is:

If AOIS eventually uses a managed cluster or managed runtime, what must be true before it is allowed to run?

## AOIS Connection

The AOIS path is now:

`managed model plan -> managed agent tradeoff -> event workflow -> managed runtime governance`

`v10` planned provider inference.
`v10.5` gated managed agents.
`v11` planned event workflows.
`v12` defines the governance controls required before managed Kubernetes or similar runtime is created.

## Learning Goals

By the end of this version you should be able to:

- explain managed runtime governance
- explain why IAM least privilege is mandatory
- explain why workload identity is safer than static keys
- explain observability as logs, metrics, traces, events, dashboards, alerts, and SLOs
- explain cost controls before live cloud execution
- explain why `aois-p` names protect primary AOIS separation
- validate the governance plan locally without cloud calls

## Prerequisites

You should have completed:

- `v6.5` workload identity and RBAC planning
- `v9` autoscaling and event-driven planning
- `v10` managed model planning
- `v11` event workflow planning

Required checks:

```bash
python3 -m py_compile examples/validate_managed_runtime_governance_plan.py
python3 examples/validate_managed_runtime_governance_plan.py
```

## Core Concepts

## Managed Runtime

A managed runtime is provider-operated infrastructure that runs workloads for you.

For AOIS, this could later mean a managed Kubernetes cluster, managed node pool, managed identity integration, or managed observability target.

In this lesson, those are placeholders only.

## Governance

Governance is the set of rules that decide what can exist, who can access it, what it can spend, how it is observed, and how it is recovered.

## Least Privilege

Least privilege means each workload gets only the permissions it needs.

The plan rejects wildcard admin policy.

## Workload Identity

Workload identity lets a workload receive scoped identity without storing long-lived static keys inside the app or repo.

The plan requires workload identity and rejects secrets in repo files.

## Observability

Observability is the ability to understand system behavior from outputs.

The plan requires:

- logs
- metrics
- traces
- events
- dashboards
- alerts
- SLOs

## Cost Controls

Cost controls prevent cloud resources from growing quietly.

In this lesson:

- budget approval is false
- maximum spend is zero
- maximum clusters is zero
- maximum nodes is zero

## Primary AOIS Separation

This portfolio must not blend into the primary AOIS project.

Every server-visible or cloud-visible placeholder uses the `aois-p` prefix.

## Build

Inspect:

```bash
sed -n '1,260p' cloud/aws/managed-runtime-governance.plan.json
sed -n '1,280p' examples/validate_managed_runtime_governance_plan.py
```

Compile:

```bash
python3 -m py_compile examples/validate_managed_runtime_governance_plan.py
```

Run:

```bash
python3 examples/validate_managed_runtime_governance_plan.py
```

Expected:

```json
{
  "cloud_resources_created": false,
  "credentials_used": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

Do not run cloud provider commands. Do not create a cluster, node pool, identity, budget alarm, log group, dashboard, or runtime resource.

## Ops Lab

Answer from the plan:

1. Which namespace keeps the portfolio separate?
2. Which field proves no managed runtime was created?
3. Which field proves credentials were not used?
4. Which IAM field rejects wildcard admin?
5. Which IAM field rejects static keys?
6. Which observability fields are required?
7. Which cost values keep live cloud use at zero?
8. Which live check protects the primary AOIS project?

Answer key:

1. `aois-p`
2. `cloud_resources_created=false`
3. `credentials_used=false`
4. `wildcard_admin_policy_allowed=false`
5. `long_lived_static_keys_allowed=false`
6. logs, metrics, traces, events, dashboards, alerts, and SLOs
7. `max_spend_usd=0`, `max_clusters=0`, `max_nodes=0`
8. `primary_aois_separation_review`

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Allow Admin Wildcard

Set:

```json
"wildcard_admin_policy_allowed": true
```

Expected risk:

- workloads or operators may receive broad permissions that are hard to audit

### Option B - Allow Static Keys

Set:

```json
"long_lived_static_keys_allowed": true
```

Expected risk:

- leaked keys can outlive the workload and bypass identity controls

### Option C - Approve Budget Too Early

Set:

```json
"budget_approved": true
```

Expected risk:

- plan-only learning can be mistaken for permission to spend

### Option D - Remove Primary AOIS Separation

Remove `primary_aois_separation_review`.

Expected risk:

- portfolio resources may collide with or confuse the primary AOIS project

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. cloud resources created remains false
4. credentials used remains false
5. namespace remains `aois-p`
6. wildcard admin remains disallowed
7. long-lived static keys remain disallowed
8. observability controls remain true
9. cost limits remain zero
10. primary AOIS separation review is required

## Common Mistakes

- treating managed Kubernetes as "just Kubernetes"
- creating clusters before IAM and budget controls exist
- using long-lived keys instead of workload identity
- assuming provider dashboards are enough without SLOs and alerts
- forgetting cost tags and quota reviews
- mixing primary AOIS and portfolio resource names
- skipping rollback and incident-response planning

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_managed_runtime_governance_plan.py
```

Read `missing`, inspect the plan, and restore the required controls.

Common fixes:

- restore `namespace` to `aois-p`
- restore all managed runtime placeholders to the `aois-p-` prefix
- restore `cloud_resources_created` to `false`
- restore `credentials_used` to `false`
- restore `approved_for_live_cloud` to `false`
- restore wildcard admin to `false`
- restore static keys to `false`
- restore observability controls to `true`
- restore cost limits to zero
- restore `primary_aois_separation_review`

If live managed runtime work is requested:

- stop
- check official provider documentation
- define credentials and secret storage
- define IAM least privilege
- define workload identity
- define budget and quota limits
- define observability dashboards, alerts, and SLOs
- define capacity plan
- define rollback plan
- verify separation from primary AOIS
- get explicit approval before creating resources

## Benchmark

Measure:

- validator compile result
- validator status
- namespace
- cloud resources created status
- credentials used status
- budget approval status
- max clusters
- max nodes
- repo disk footprint
- memory snapshot

## Architecture Defense

Why require governance before managed runtime creation?

Because managed infrastructure can still fail, leak data, spend money, over-scale, hide broken signals, or collide with existing projects.

Why require workload identity?

Because long-lived static keys are harder to rotate, easier to leak, and poorly scoped compared with workload-attached identity.

Why require observability before runtime?

Because a system that cannot be observed cannot be operated responsibly.

Why require `aois-p`?

Because this portfolio is secondary to primary AOIS and must stay unambiguous on shared infrastructure.

## 4-Layer Tool Drill

Tool: workload identity

1. Plain English
It gives a workload permission without putting static keys inside the app.

2. System Role
It connects runtime identity to least-privilege cloud permissions.

3. Minimal Technical Definition
It is a provider/runtime mechanism that binds a workload to scoped credentials or roles at execution time.

4. Hands-on Proof
The validator confirms workload identity is required, static keys are disallowed, and no credentials are used in the lesson.

## 4-Level System Explanation Drill

1. Simple English
AOIS plans cloud runtime safety before creating cloud runtime.

2. Practical Explanation
I can show which IAM, cost, observability, capacity, rollback, and naming controls must exist before a managed cluster is allowed.

3. Technical Explanation
`v12` adds a managed-runtime governance JSON plan and local validator that rejects live cloud approval, credentials, broad IAM, static keys, missing observability, and non-`aois-p` runtime names.

4. Engineer-Level Explanation
AOIS now separates managed-runtime design from managed-runtime execution, requiring least privilege, workload identity, observability, cost gates, capacity planning, rollback, incident response, and primary-project separation before any provider-managed runtime is created.

## Failure Story

Representative failure:

- Symptom: a portfolio cluster appears in the provider account, costs rise overnight, and nobody knows whether it belongs to primary AOIS or the training portfolio
- Root cause: live runtime creation happened without `aois-p` naming, budget approval, cost alarms, or primary AOIS separation review
- Fix: delete or quarantine the unmanaged resource after approval, restore the governance plan, and require explicit live-cloud approval
- Prevention: validate the `v12` governance plan and keep managed runtime limits at zero until approvals exist
- What this taught me: managed infrastructure without governance is still operational debt

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v12` solve in AOIS?
2. What is a managed runtime?
3. What is governance?
4. Why is least privilege required?
5. Why is workload identity safer than static keys?
6. What observability signals are required?
7. Why are budget approval and max spend set to zero?
8. Why must runtime placeholders use `aois-p`?
9. What must exist before live managed runtime use?
10. Explain workload identity using the 4-layer tool rule.
11. Explain `v12` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v12` solve in AOIS?

It defines the IAM, observability, cost, capacity, rollback, and separation controls required before managed runtime creation.

2. What is a managed runtime?

Provider-operated infrastructure that runs workloads, such as a managed cluster or managed compute environment.

3. What is governance?

The rules that decide what can exist, who can access it, what it can spend, how it is observed, and how it is recovered.

4. Why is least privilege required?

It limits damage by granting only the permissions needed for the workload.

5. Why is workload identity safer than static keys?

It avoids storing long-lived credentials in apps or repo files and can be scoped to the workload.

6. What observability signals are required?

Logs, metrics, traces, events, dashboards, alerts, and SLOs.

7. Why are budget approval and max spend set to zero?

Because the lesson is validation-only and no live cloud spending is approved.

8. Why must runtime placeholders use `aois-p`?

To keep this portfolio visibly separate from the primary AOIS project.

9. What must exist before live managed runtime use?

Official docs review, credential plan, budget approval, IAM review, workload identity review, network boundary review, observability dashboard, cost alarm review, capacity plan, rollback plan, and primary AOIS separation review.

10. Explain workload identity using the 4-layer tool rule.

- Plain English: it gives a workload permission without app keys.
- System Role: it connects runtime identity to scoped cloud permissions.
- Minimal Technical Definition: it binds workload execution to provider-scoped credentials or roles.
- Hands-on Proof: the validator requires workload identity and rejects static keys.

11. Explain `v12` using the 4-level system explanation rule.

- Simple English: AOIS plans managed-runtime safety before creating cloud runtime.
- Practical explanation: I can explain IAM, observability, cost, capacity, rollback, and naming controls.
- Technical explanation: `v12` adds a governance plan and no-cloud validator.
- Engineer-level explanation: AOIS now gates managed-runtime creation behind least privilege, workload identity, observability, cost limits, capacity planning, rollback, incident response, and primary-project separation.

## Connection Forward

`v12` closes Phase 4 by defining enterprise cloud governance without using cloud resources.

`v13` begins Phase 5, where the curriculum moves from cloud planning into inference and GPU engineering foundations.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v12 Introduction](02-introduction.md)
- Next: [v12 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
