# v7 Lab

Authoring status: authored

## Build Lab

Inspect:

```bash
sed -n '1,120p' charts/aois-p/Chart.yaml
sed -n '1,220p' charts/aois-p/values.yaml
find charts/aois-p/templates -maxdepth 1 -type f -print
```

Compile:

```bash
python3 -m py_compile examples/validate_helm_plan.py
```

Run:

```bash
python3 examples/validate_helm_plan.py
```

Success state:

- status is `pass`
- `helm_install_ran` is `false`
- chart name is `aois-p`

## Ops Lab

Answer:

1. what file names the chart?
2. what file holds defaults?
3. what directory holds templates?
4. what value disables provider calls?
5. what command is gated?

## Break Lab

Use scratch copies only.

Remove resource limits from `values.yaml` and explain why the chart becomes unsafe.

Change namespace from `aois-p` to `aois` and explain why it becomes ambiguous.

## Explanation Lab

Answer:

1. what is a chart?
2. what is a value?
3. what is a template?
4. what is a release?
5. why is install gated?

## Defense Lab

Defend:

`Helm packaging should preserve the safety controls from raw manifests.`

Your defense must mention:

- namespace
- resource limits
- identity
- network policy
- provider gates

## Benchmark Lab

Record:

- validator result
- whether Helm install ran
- chart name
- repo footprint
- memory snapshot
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v7 - Helm Packaging Without Installing A Release](notes.md)
- Next: [v7 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
