# v6 Lab

Authoring status: authored

## Build Lab

Inspect:

```bash
find k8s/aois-p -maxdepth 1 -type f -print
sed -n '1,220p' k8s/aois-p/deployment.yaml
```

Compile:

```bash
python3 -m py_compile examples/validate_k8s_plan.py
```

Run:

```bash
python3 examples/validate_k8s_plan.py
```

Success state:

- status is `pass`
- namespace is `aois-p`
- `kubectl_apply_ran` is `false`

## Ops Lab

Answer:

1. which file defines namespace?
2. which file caps namespace resources?
3. which file sets default limits?
4. which file defines the app pod?
5. which file defines in-cluster access?

## Break Lab

Use scratch copies only.

Remove the deployment memory limit and explain why that is unsafe.

Change namespace from `aois-p` to `aois` and explain why that is confusing.

## Explanation Lab

Answer:

1. what is a namespace?
2. what is ResourceQuota?
3. what is LimitRange?
4. what is a Deployment?
5. what is a Service?
6. why are probes useful?

## Defense Lab

Defend:

`Kubernetes manifests should be validated before applying them on a shared server.`

Your defense must mention:

- primary AOIS priority
- namespace separation
- CPU and memory limits
- live cluster mutation
- rollback difficulty

## Benchmark Lab

Record:

- validator result
- repo footprint
- whether `kubectl apply` ran
- whether any namespace/resource was created
- memory snapshot
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v6 - Kubernetes Plan Without Applying Resources](03-notes.md)
- Next: [v6 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
