# v6.5 Lab

Authoring status: authored

## Build Lab

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

Success state:

- status is `pass`
- `kubectl_apply_ran` is `false`
- service account is `aois-p-api`

## Ops Lab

Answer:

1. what object gives the pod identity?
2. what object defines permissions?
3. what object attaches permissions?
4. what disables token automount?
5. what object controls pod network traffic?

## Break Lab

Use scratch copies only.

Add broad RBAC rules and explain why that is dangerous.

Remove `automountServiceAccountToken: false` and explain why that increases risk.

## Explanation Lab

Answer:

1. what is a ServiceAccount?
2. what is RBAC?
3. what is least privilege?
4. what is NetworkPolicy?
5. why are identity manifests gated?

## Defense Lab

Defend:

`Workload identity belongs before live cluster deployment.`

Your defense must mention:

- least privilege
- service account tokens
- network reach
- primary AOIS protection
- cluster mutation

## Benchmark Lab

Record:

- validator result
- whether `kubectl apply` ran
- whether RBAC grants permissions
- whether token automount is disabled
- repo footprint
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v6.5 - Workload Identity And Trust Boundaries Without Applying Resources](notes.md)
- Next: [v6.5 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
