# v4 Runbook

Authoring status: authored

## Purpose

Use this runbook when the container plan validator fails or when Docker build/run is being considered.

## Primary Checks

Validate without building:

```bash
python3 examples/validate_container_plan.py
```

Inspect key files:

```bash
sed -n '1,220p' Dockerfile
sed -n '1,220p' compose.yaml
sed -n '1,120p' .dockerignore
```

## Recovery Steps

If validator fails:

- read the `missing` list
- restore the missing Dockerfile, Compose, or ignore rule
- rerun the validator

If someone wants to build:

- stop
- estimate disk impact
- confirm no primary AOIS conflict
- get approval
- record resource usage after build

If a container is running unexpectedly:

- identify it first
- confirm whether it is portfolio-owned
- do not stop primary AOIS containers
- stop only approved portfolio-owned runtime
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v4 Lab](lab.md)
- Next: [v4 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
