# v6.5 - Workload Identity And Trust Boundaries Without Applying Resources

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: identity manifests and local validation only, no `kubectl apply`

## What This Builds

This version extends the `aois-p` Kubernetes plan with identity and trust controls:

- `k8s/aois-p/service-account.yaml`
- `k8s/aois-p/role.yaml`
- `k8s/aois-p/role-binding.yaml`
- `k8s/aois-p/network-policy.yaml`
- deployment `serviceAccountName`
- `examples/validate_k8s_identity_plan.py`

It teaches:

- ServiceAccount
- RBAC Role
- RoleBinding
- automount service account token control
- NetworkPolicy
- least privilege
- trust boundary thinking

## Why This Exists

Kubernetes workloads are not only containers.

They also have identity, permissions, and network reach.
AOIS needs those boundaries before real cluster deployment.

## AOIS Connection

The AOIS path is now:

`namespace -> workload -> service account -> RBAC -> network policy -> trust boundary`

`v6` created a workload plan.
`v6.5` makes the workload identity explicit and minimal.

## Learning Goals

By the end of this version you should be able to:

- explain ServiceAccount
- explain RBAC Role and RoleBinding
- explain least privilege
- explain why automatic service account tokens can be risky
- explain NetworkPolicy
- validate identity manifests without applying them
- explain trust boundaries using the 4-layer rule

## Resource Gate

Do not run:

```bash
kubectl apply
kubectl create
helm install
```

Allowed:

- read manifests
- run local validators

Applying identity or network policy resources requires explicit approval because it changes live cluster behavior.

## Prerequisites

You should have completed `v6`.

Required checks:

```bash
python3 -m py_compile examples/validate_k8s_identity_plan.py
python3 examples/validate_k8s_identity_plan.py
```

## Core Concepts

## ServiceAccount

A ServiceAccount is a Kubernetes identity for pods.

This version uses:

```text
aois-p-api
```

## RBAC

RBAC controls what an identity can do.

This version starts with:

```yaml
rules: []
```

That means no Kubernetes API permissions are granted yet.

## RoleBinding

A RoleBinding attaches a Role to a subject.

Here it binds the minimal empty Role to the `aois-p-api` ServiceAccount.

## Automount Token

Service account tokens can let pods call the Kubernetes API.

This plan disables automatic token mounting:

```yaml
automountServiceAccountToken: false
```

## NetworkPolicy

NetworkPolicy controls pod network traffic.

This plan keeps the service local to cluster traffic and denies egress by default.

## Build

Inspect:

```bash
sed -n '1,160p' k8s/aois-p/service-account.yaml
sed -n '1,160p' k8s/aois-p/role.yaml
sed -n '1,200p' k8s/aois-p/network-policy.yaml
```

Compile:

```bash
python3 -m py_compile examples/validate_k8s_identity_plan.py
```

Run:

```bash
python3 examples/validate_k8s_identity_plan.py
```

Expected:

```json
{
  "kubectl_apply_ran": false,
  "namespace": "aois-p",
  "service_account": "aois-p-api",
  "status": "pass"
}
```

## Ops Lab

Answer:

1. Which file defines workload identity?
2. Which file defines permissions?
3. Which file attaches identity to permissions?
4. Which field disables automatic API token mounting?
5. Which file limits pod network reach?

Answer key:

1. `service-account.yaml`
2. `role.yaml`
3. `role-binding.yaml`
4. `automountServiceAccountToken: false`
5. `network-policy.yaml`

## Break Lab

Do not skip this.

### Option A - Add Broad Permissions

In a scratch copy, replace `rules: []` with broad permissions.

Expected risk:

- compromised pod can do more inside the cluster

### Option B - Enable Token Automount

In a scratch copy, remove `automountServiceAccountToken: false`.

Expected risk:

- pod may receive API credentials it does not need

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. no manifest is applied
4. you can explain ServiceAccount, Role, RoleBinding, token automount, and NetworkPolicy

## Common Mistakes

- giving pods permissions "just in case"
- forgetting service account tokens exist
- treating network reach as harmless
- applying RBAC changes without review
- confusing identity with authentication to external providers

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_k8s_identity_plan.py
```

Read `missing`, inspect the referenced file, and restore the missing control.

If you want to apply:

- stop
- confirm cluster target
- confirm namespace `aois-p`
- confirm RBAC scope
- confirm network policy impact
- get explicit approval

## Benchmark

Measure:

- validator compile result
- validator status
- whether `kubectl apply` ran
- repo disk footprint
- memory snapshot

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can inspect, validate, break, explain, and defend workload identity controls. |
| 4/5 | Plan validates, but one identity concept needs review. |
| 3/5 | Files exist, but RBAC or token reasoning is weak. |
| 2/5 | Identity manifests exist, but trust boundary is unclear. |
| 1/5 | Pods still feel like anonymous containers. |

Minimum pass: `4/5`.

## Architecture Defense

Why identity before deployment?

Because workloads should have explicit identity and minimal permissions before they run.

Why empty Role?

Because the app does not need Kubernetes API access yet.

Why deny token automount?

Because unused credentials increase risk.

## 4-Layer Tool Drill

Tool: ServiceAccount

1. Plain English
It gives a pod a Kubernetes identity.

2. System Role
It identifies AOIS portfolio workloads inside the cluster.

3. Minimal Technical Definition
It is a Kubernetes API object used as pod identity for API authentication and policy binding.

4. Hands-on Proof
The validator confirms the deployment uses `aois-p-api` and token automount is disabled.

## 4-Level System Explanation Drill

1. Simple English
AOIS pods now have a planned identity.

2. Practical Explanation
I can inspect service account, RBAC, and network policy manifests.

3. Technical Explanation
`v6.5` adds ServiceAccount, empty Role, RoleBinding, NetworkPolicy, and deployment identity wiring.

4. Engineer-Level Explanation
AOIS now separates workload execution from workload trust, defining minimal identity and permissions before any cluster mutation occurs.

## Failure Story

Representative failure:

- Symptom: a compromised pod can read Kubernetes API data it does not need
- Root cause: broad RBAC and automatic service account token mounting
- Fix: use minimal Role and disable token automount
- Prevention: validate identity controls before apply
- What this taught me: workload identity is part of infrastructure security

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v6.5` solve in AOIS?
2. What is a ServiceAccount?
3. What is RBAC?
4. What is a Role?
5. What is a RoleBinding?
6. Why use `rules: []`?
7. Why disable service account token automount?
8. What does NetworkPolicy do?
9. Why is applying identity manifests gated?
10. Explain ServiceAccount using the 4-layer tool rule.
11. Explain `v6.5` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v6.5` solve in AOIS?

It adds planned workload identity, minimal permissions, and network boundaries to the Kubernetes design.

2. What is a ServiceAccount?

A Kubernetes identity for pods.

3. What is RBAC?

Role-based access control for Kubernetes API permissions.

4. What is a Role?

A namespace-scoped set of permissions.

5. What is a RoleBinding?

An object that attaches a Role to a subject such as a ServiceAccount.

6. Why use `rules: []`?

Because the app does not need Kubernetes API permissions yet.

7. Why disable service account token automount?

To avoid giving pods credentials they do not need.

8. What does NetworkPolicy do?

It controls pod network traffic.

9. Why is applying identity manifests gated?

Because RBAC and network policy can change live cluster behavior.

10. Explain ServiceAccount using the 4-layer tool rule.

- Plain English: it gives a pod identity.
- System Role: it identifies AOIS workloads inside the cluster.
- Minimal Technical Definition: it is a Kubernetes identity object for pods.
- Hands-on Proof: the validator confirms service account wiring and disabled token automount.

11. Explain `v6.5` using the 4-level system explanation rule.

- Simple English: AOIS has a planned pod identity.
- Practical explanation: I can inspect RBAC and network policy safely.
- Technical explanation: `v6.5` adds ServiceAccount, Role, RoleBinding, NetworkPolicy, and deployment wiring.
- Engineer-level explanation: AOIS now has a least-privilege workload trust design before any cluster resources are applied.

## Connection Forward

`v6.5` adds identity and trust.

`v7` packages the manifests into a Helm chart so deployment configuration can become reusable without losing these controls.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v6.5 Introduction](introduction.md)
- Next: [v6.5 Lab](lab.md)
<!-- AOIS-NAV-END -->
