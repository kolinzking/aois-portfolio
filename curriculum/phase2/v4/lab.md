# v4 Lab

Authoring status: authored

## Build Lab

Inspect:

```bash
sed -n '1,220p' Dockerfile
sed -n '1,220p' compose.yaml
sed -n '1,120p' .dockerignore
```

Compile:

```bash
python3 -m py_compile examples/validate_container_plan.py
```

Run:

```bash
python3 examples/validate_container_plan.py
```

Success state:

- status is `pass`
- `docker_build_ran` is `false`
- service name is `aois-p-api`
- memory and CPU limits exist

## Ops Lab

Answer:

1. what file defines image build steps?
2. what file defines Compose runtime plan?
3. what file protects build context?
4. what line limits memory?
5. what line binds the port to localhost?

## Break Lab

Use scratch copies only.

Remove `.venv` from a scratch `.dockerignore` and explain why that is risky.

Change the port binding from localhost-only to public and explain why that is risky.

## Explanation Lab

Answer:

1. what is a Dockerfile?
2. what is build context?
3. why use `.dockerignore`?
4. why use a non-root user?
5. why are build/run commands gated?

## Defense Lab

Defend:

`Container design should be validated before building or running containers on a shared server.`

Your defense must mention:

- disk
- memory
- port exposure
- primary AOIS priority
- `aois-p` naming

## Benchmark Lab

Record:

- validator result
- repo footprint
- whether Docker build ran
- whether container ran
- whether any Docker resource was created
