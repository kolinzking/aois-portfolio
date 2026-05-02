# v7 - Helm Packaging Without Installing A Release

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: Helm chart authoring and local validation only, no `helm install`

## What This Builds

This version builds a Helm chart for AOIS portfolio:

- `charts/aois-p/Chart.yaml`
- `charts/aois-p/values.yaml`
- `charts/aois-p/templates/`
- `examples/validate_helm_plan.py`

It teaches:

- chart structure
- values
- templates
- release configuration
- preserving resource limits and identity controls
- why Helm install is gated

## Why This Exists

Raw Kubernetes YAML becomes hard to reuse as environments change.

Helm packages related manifests and lets values control configuration.
But a Helm install still mutates the cluster, so this lesson stops at chart design and validation.

## AOIS Connection

The AOIS path is now:

`Kubernetes manifests -> Helm chart -> reusable deployment package -> future GitOps input`

`v7` packages the `aois-p` infrastructure plan without installing it.

## Learning Goals

By the end of this version you should be able to:

- explain a Helm chart
- explain `Chart.yaml`
- explain `values.yaml`
- explain templates
- explain why `helm install` is gated
- validate chart structure locally
- defend preserving limits, identity, and provider gates in chart form

## Resource Gate

Do not run:

```bash
helm install
helm upgrade
helm uninstall
```

Allowed:

- read chart files
- run `python3 examples/validate_helm_plan.py`

Running Helm against the cluster requires explicit approval because it creates or changes Kubernetes resources.

## Prerequisites

You should have completed:

- `v6` Kubernetes plan
- `v6.5` workload identity

Required check:

```bash
python3 -m py_compile examples/validate_helm_plan.py
python3 examples/validate_helm_plan.py
```

## Core Concepts

## Helm Chart

A Helm chart packages Kubernetes templates and default values.

## `Chart.yaml`

`Chart.yaml` describes the chart name, version, and app version.

## `values.yaml`

`values.yaml` stores configurable defaults.

This chart keeps:

- namespace `aois-p`
- one replica
- provider calls disabled
- resource limits
- service type `ClusterIP`
- service account token automount disabled

## Template

A template is Kubernetes YAML with placeholders.

Example:

```yaml
name: {{ .Values.app.name }}
```

## Release

A release is an installed chart instance.

This version does not create one.

## Build

Inspect:

```bash
sed -n '1,120p' charts/aois-p/Chart.yaml
sed -n '1,220p' charts/aois-p/values.yaml
find charts/aois-p/templates -maxdepth 1 -type f -print
```

Compile validator:

```bash
python3 -m py_compile examples/validate_helm_plan.py
```

Run validator:

```bash
python3 examples/validate_helm_plan.py
```

Expected:

```json
{
  "chart": "aois-p",
  "helm_install_ran": false,
  "status": "pass"
}
```

## Ops Lab

Answer:

1. Which file names the chart?
2. Which file holds default configuration?
3. Which directory holds templates?
4. Which value disables provider calls?
5. Which command is intentionally not run?

Answer key:

1. `Chart.yaml`
2. `values.yaml`
3. `templates/`
4. `providerCallsEnabled: "false"`
5. `helm install`

## Break Lab

Do not skip this.

### Option A - Remove Resource Limits

In a scratch copy, remove limits from `values.yaml`.

Expected risk:

- chart can render unbounded workloads later

### Option B - Change Namespace

In a scratch copy, change namespace from `aois-p` to `aois`.

Expected risk:

- portfolio deployment becomes ambiguous

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. no Helm install or upgrade runs
4. chart preserves resource, identity, and security controls

## Common Mistakes

- installing a chart before reviewing values
- templating away resource limits
- losing provider gates in chart conversion
- using ambiguous release names
- confusing chart validation with cluster deployment

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_helm_plan.py
```

Read `missing`, inspect the referenced chart file, and restore the missing control.

If you want to install:

- stop
- confirm target cluster and namespace
- confirm rendered resources
- confirm resource budget
- get explicit approval

## Benchmark

Measure:

- validator compile result
- validator status
- whether Helm install ran
- repo disk footprint
- memory snapshot

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can inspect, validate, break, explain, and defend a Helm chart without installing. |
| 4/5 | Chart validates, but one Helm concept needs review. |
| 3/5 | Files exist, but template or values reasoning is weak. |
| 2/5 | Chart exists, but install risk is unclear. |
| 1/5 | Helm still means blindly installing charts. |

Minimum pass: `4/5`.

## Architecture Defense

Why Helm after raw manifests?

Because packaging comes after understanding the underlying resources.

Why not install?

Because install mutates the live cluster and consumes resources.

Why preserve `aois-p` values?

Because packaging must not weaken namespace separation or resource controls.

## 4-Layer Tool Drill

Tool: Helm chart

1. Plain English
It packages Kubernetes resources.

2. System Role
It makes AOIS deployment configuration reusable.

3. Minimal Technical Definition
It is a directory containing chart metadata, default values, and Kubernetes templates.

4. Hands-on Proof
The validator checks chart files and confirms no Helm install ran.

## 4-Level System Explanation Drill

1. Simple English
AOIS now has a Helm package plan.

2. Practical Explanation
I can inspect chart metadata, values, and templates without installing.

3. Technical Explanation
`v7` adds `charts/aois-p` and a local chart validator.

4. Engineer-Level Explanation
AOIS now packages its Kubernetes design into reusable Helm structure while preserving provider gates, identity, network policy, and resource limits before cluster mutation.

## Failure Story

Representative failure:

- Symptom: a Helm chart installs a workload without limits
- Root cause: resource controls were lost during templating
- Fix: keep limits in `values.yaml` and templates
- Prevention: validate chart before install
- What this taught me: packaging must preserve safety controls

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v7` solve in AOIS?
2. What is a Helm chart?
3. What is `Chart.yaml`?
4. What is `values.yaml`?
5. What is a template?
6. What is a release?
7. Why is `helm install` gated?
8. Why preserve provider gates in values?
9. Why preserve resource limits in templates?
10. Explain Helm chart using the 4-layer tool rule.
11. Explain `v7` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v7` solve in AOIS?

It packages Kubernetes resources into reusable Helm chart structure.

2. What is a Helm chart?

A package of Kubernetes templates, metadata, and default values.

3. What is `Chart.yaml`?

The chart metadata file.

4. What is `values.yaml`?

The default configuration file for templates.

5. What is a template?

Kubernetes YAML with Helm placeholders.

6. What is a release?

An installed instance of a Helm chart.

7. Why is `helm install` gated?

It mutates the live cluster and can create resources.

8. Why preserve provider gates in values?

So packaging does not accidentally enable external AI calls.

9. Why preserve resource limits in templates?

So chart users cannot deploy unbounded workloads by default.

10. Explain Helm chart using the 4-layer tool rule.

- Plain English: it packages Kubernetes resources.
- System Role: it makes AOIS deployment reusable.
- Minimal Technical Definition: it is metadata, values, and templates.
- Hands-on Proof: the validator confirms chart safety fields without install.

11. Explain `v7` using the 4-level system explanation rule.

- Simple English: AOIS has a Helm package.
- Practical explanation: I can inspect and validate chart files.
- Technical explanation: `v7` adds chart metadata, values, templates, and a validator.
- Engineer-level explanation: AOIS now has reusable deployment packaging that preserves resource, identity, network, and provider-gating controls before cluster mutation.

## Connection Forward

`v7` packages the deployment plan.

`v8` introduces GitOps flow so deployment intent can be driven by reviewed Git history instead of manual cluster commands.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v7 Introduction](02-introduction.md)
- Next: [v7 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
