# v8 Lab

Authoring status: authored

## Build Lab

Inspect:

```bash
sed -n '1,220p' gitops/argocd/aois-p-application.yaml
sed -n '1,160p' gitops/argocd/README.md
```

Compile:

```bash
python3 -m py_compile examples/validate_gitops_plan.py
```

Run:

```bash
python3 examples/validate_gitops_plan.py
```

Success state:

- status is `pass`
- `kubectl_apply_ran` is `false`
- `argocd_sync_ran` is `false`

## Ops Lab

Answer:

1. what chart path is referenced?
2. what namespace is targeted?
3. what disables automated sync?
4. why is `CreateNamespace=false` used?
5. why is live sync gated?

## Break Lab

Use scratch copies only.

Enable automated sync and explain why that is risky on this shared server.

Change destination namespace to `aois` and explain why that breaks portfolio clarity.

## Explanation Lab

Answer:

1. what is GitOps?
2. what is an ArgoCD Application?
3. what is source?
4. what is destination?
5. what is sync policy?

## Defense Lab

Defend:

`GitOps should be reviewable before it is allowed to sync a shared cluster.`

Your defense must mention:

- Git history
- cluster mutation
- namespace separation
- resource control
- manual sync gate

## Benchmark Lab

Record:

- validator result
- whether apply ran
- whether sync ran
- repo footprint
- memory snapshot
