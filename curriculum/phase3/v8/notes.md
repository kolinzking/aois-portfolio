# v8 - GitOps And ArgoCD Flow Without Cluster Sync

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: GitOps manifest authoring and local validation only, no ArgoCD app creation or sync

## What This Builds

This version builds the AOIS portfolio GitOps plan:

- `gitops/argocd/aois-p-application.yaml`
- `gitops/argocd/README.md`
- `examples/validate_gitops_plan.py`

It teaches:

- desired state
- ArgoCD Application
- source path
- destination namespace
- manual sync posture
- Git review before cluster mutation
- why GitOps sync is gated

## Why This Exists

Manual cluster commands do not scale well.

GitOps makes Git the source of desired state, so deployment changes can be reviewed, versioned, and audited.
But ArgoCD sync still mutates the cluster, so this lesson stops at plan validation.

## AOIS Connection

The AOIS path is now:

`Helm chart -> GitOps Application -> reviewed desired state -> future controlled sync`

`v7` packaged the workload.
`v8` defines how that package would be connected to GitOps.

## Learning Goals

By the end of this version you should be able to:

- explain GitOps
- explain ArgoCD Application
- explain source and destination
- explain manual sync posture
- explain why automated sync is disabled in this plan
- validate GitOps intent without applying anything
- defend Git review as deployment control

## Resource Gate

Do not run:

```bash
kubectl apply -f gitops/argocd/aois-p-application.yaml
argocd app create
argocd app sync
```

Allowed:

- read GitOps manifests
- run `python3 examples/validate_gitops_plan.py`

Live GitOps use requires explicit approval because it can create and sync Kubernetes resources.

## Prerequisites

You should have completed:

- `v6` Kubernetes plan
- `v6.5` workload identity
- `v7` Helm packaging

Required checks:

```bash
python3 -m py_compile examples/validate_gitops_plan.py
python3 examples/validate_gitops_plan.py
```

## Core Concepts

## GitOps

GitOps means Git stores desired infrastructure/application state.

The cluster is reconciled toward what Git says should exist.

## ArgoCD Application

An ArgoCD Application tells ArgoCD:

- which repo to read
- which path to use
- which revision to track
- which cluster and namespace to target
- how sync should behave

## Source

Source is the Git repo, branch, and path.

This plan points to:

```text
charts/aois-p
```

## Destination

Destination is where ArgoCD would apply the app.

This plan targets namespace:

```text
aois-p
```

## Sync Policy

Sync policy controls how desired state reaches the cluster.

This plan keeps automated sync disabled:

```yaml
automated: null
```

## Build

Inspect:

```bash
sed -n '1,220p' gitops/argocd/aois-p-application.yaml
sed -n '1,160p' gitops/argocd/README.md
```

Compile validator:

```bash
python3 -m py_compile examples/validate_gitops_plan.py
```

Run validator:

```bash
python3 examples/validate_gitops_plan.py
```

Expected:

```json
{
  "application": "aois-p",
  "argocd_sync_ran": false,
  "kubectl_apply_ran": false,
  "status": "pass"
}
```

## Ops Lab

Answer:

1. Which file defines the ArgoCD Application?
2. Which chart path does it use?
3. Which namespace does it target?
4. Which field disables automated sync?
5. Which value proves no sync ran?

Answer key:

1. `gitops/argocd/aois-p-application.yaml`
2. `charts/aois-p`
3. `aois-p`
4. `automated: null`
5. `argocd_sync_ran=false`

## Break Lab

Do not skip this.

### Option A - Automated Sync Too Early

In a scratch copy, enable automated sync.

Expected risk:

- Git changes could mutate the cluster without a deliberate manual gate

### Option B - Wrong Namespace

In a scratch copy, target namespace `aois`.

Expected risk:

- portfolio deployment becomes ambiguous and may conflict with primary AOIS conventions

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. no ArgoCD app is created
4. no ArgoCD sync runs
5. no `kubectl apply` runs
6. you can explain source, destination, sync policy, and Git review

## Common Mistakes

- treating GitOps manifest creation as cluster deployment
- enabling automated sync before approval
- pointing ArgoCD at the wrong namespace
- losing provider gates in chart values
- skipping Git review because "Argo will fix it"
- applying an Application without checking target cluster

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_gitops_plan.py
```

Read `missing`, inspect the referenced GitOps file, and restore the missing control.

If live sync is requested:

- stop
- confirm repo URL
- confirm target cluster
- confirm namespace `aois-p`
- confirm sync policy
- get explicit approval
- record resource usage after sync

## Benchmark

Measure:

- validator compile result
- validator status
- whether `kubectl apply` ran
- whether ArgoCD sync ran
- repo disk footprint
- memory snapshot

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can inspect, validate, break, explain, and defend GitOps flow without syncing. |
| 4/5 | Plan validates, but one GitOps concept needs review. |
| 3/5 | Files exist, but source/destination or sync policy is weak. |
| 2/5 | Application exists, but cluster mutation risk is unclear. |
| 1/5 | GitOps still means "Argo magically deploys things." |

Minimum pass: `4/5`.

## Architecture Defense

Why GitOps after Helm?

Because GitOps needs a deployable package or manifest path to reconcile.

Why disable automated sync?

Because this portfolio shares a constrained server and cluster changes must be deliberate.

Why keep Git as the source?

Because deployment intent should be reviewable and auditable.

## 4-Layer Tool Drill

Tool: ArgoCD Application

1. Plain English
It tells ArgoCD what app state to sync from Git.

2. System Role
It connects AOIS Helm packaging to future cluster reconciliation.

3. Minimal Technical Definition
It is a Kubernetes custom resource describing source repo/path/revision, destination cluster/namespace, and sync policy.

4. Hands-on Proof
The validator confirms source, destination, manual sync posture, and no live apply/sync.

## 4-Level System Explanation Drill

1. Simple English
AOIS now has a GitOps deployment plan.

2. Practical Explanation
I can inspect the ArgoCD Application and explain what would sync later.

3. Technical Explanation
`v8` adds an ArgoCD Application manifest and validator without creating the Application.

4. Engineer-Level Explanation
AOIS now separates GitOps desired-state definition from cluster reconciliation, preserving review, namespace separation, provider gates, and resource controls before any live sync.

## Failure Story

Representative failure:

- Symptom: a Git commit unexpectedly changes live cluster resources
- Root cause: automated sync was enabled before approval and review discipline
- Fix: disable automated sync and require explicit sync approval
- Prevention: validate GitOps plan and review source/destination before apply
- What this taught me: GitOps is powerful because it mutates infrastructure from Git

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v8` solve in AOIS?
2. What is GitOps?
3. What is an ArgoCD Application?
4. What is source?
5. What is destination?
6. What is sync policy?
7. Why is automated sync disabled?
8. Why is live sync gated?
9. Why must namespace remain `aois-p`?
10. Explain ArgoCD Application using the 4-layer tool rule.
11. Explain `v8` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v8` solve in AOIS?

It defines how AOIS would connect Helm-packaged desired state to GitOps without syncing the cluster.

2. What is GitOps?

Using Git as the source of desired infrastructure/application state.

3. What is an ArgoCD Application?

A custom resource describing what ArgoCD should sync from Git and where.

4. What is source?

The repo, revision, and path ArgoCD reads.

5. What is destination?

The target cluster and namespace.

6. What is sync policy?

Rules controlling how desired state is applied to the cluster.

7. Why is automated sync disabled?

To prevent unapproved Git changes from mutating the shared cluster.

8. Why is live sync gated?

It can create/update resources and consume cluster capacity.

9. Why must namespace remain `aois-p`?

To keep portfolio resources unambiguous and separate from primary AOIS.

10. Explain ArgoCD Application using the 4-layer tool rule.

- Plain English: it tells Argo what to deploy from Git.
- System Role: it connects AOIS chart to future cluster reconciliation.
- Minimal Technical Definition: it is a CRD with source, destination, and sync policy.
- Hands-on Proof: the validator confirms the Application is safe and unsynced.

11. Explain `v8` using the 4-level system explanation rule.

- Simple English: AOIS has a GitOps plan.
- Practical explanation: I can inspect source, destination, and sync policy.
- Technical explanation: `v8` adds an ArgoCD Application review manifest and validator.
- Engineer-level explanation: AOIS now has reviewed desired-state deployment structure without cluster reconciliation, preserving resource and approval boundaries.

## Connection Forward

`v8` defines GitOps flow.

`v9` adds autoscaling and event-driven behavior planning so AOIS can later scale with load while respecting strict limits.
