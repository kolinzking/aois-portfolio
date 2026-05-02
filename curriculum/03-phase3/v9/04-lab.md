# v9 Lab

Authoring status: authored

## Build Lab

Inspect:

```bash
sed -n '1,200p' k8s/aois-p/hpa.yaml
sed -n '1,220p' k8s/aois-p/keda-scaledobject.plan.yaml
```

Compile:

```bash
python3 -m py_compile examples/validate_autoscaling_plan.py
```

Run:

```bash
python3 examples/validate_autoscaling_plan.py
```

Success state:

- status is `pass`
- `max_replicas` is `1`
- `kubectl_apply_ran` is `false`
- `keda_installed` is `false`

## Ops Lab

Answer:

1. what object defines CPU-based scaling?
2. what object sketches event-driven scaling?
3. what is max replicas?
4. why is KEDA not installed?
5. why is autoscaling resource-gated?

## Break Lab

Use scratch copies only.

Raise max replicas and explain how resource usage could change.

Pretend KEDA is installed and list what new cluster resources might appear.

## Explanation Lab

Answer:

1. what is HPA?
2. what is KEDA?
3. what is min replicas?
4. what is max replicas?
5. why is max replicas capped here?

## Defense Lab

Defend:

`Autoscaling should be planned before it is enabled on a shared server.`

Your defense must mention:

- CPU
- memory
- primary AOIS priority
- dependency capacity
- GitOps review

## Benchmark Lab

Record:

- validator result
- max replicas
- whether KEDA was installed
- whether apply ran
- repo footprint
- memory snapshot
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v9 - Autoscaling And Event-Driven Planning Without Scaling Resources](03-notes.md)
- Next: [v9 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
