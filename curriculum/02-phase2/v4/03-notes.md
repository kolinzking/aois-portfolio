# v4 - Containerization Plan Without Building Images

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: Docker artifacts and validation only, no image build, no container run

## What This Builds

This version builds the AOIS portfolio container plan:

- `Dockerfile`
- `.dockerignore`
- `compose.yaml`
- `examples/validate_container_plan.py`

It teaches:

- image definition
- build context
- `.dockerignore`
- non-root runtime
- healthcheck
- localhost port binding
- CPU and memory limits
- why Docker build/run is resource-gated on this server

## Why This Exists

Containerization makes a service portable, but it also consumes disk and memory.

On this shared 16 GB server, the primary AOIS project takes priority.
So `v4` teaches container design before creating images or containers.

## AOIS Connection

The AOIS path is now:

`FastAPI service -> container plan -> resource-limited runtime design -> future deployable unit`

The portfolio service uses `aois-p` naming for server-visible container resources.

## Learning Goals

By the end of this version you should be able to:

- explain what a Dockerfile does
- explain build context
- explain why `.dockerignore` matters
- explain why containers should avoid root by default
- explain localhost port binding
- explain memory and CPU limits
- explain why building/running is gated

## Resource Gate

Do not run these commands by default:

```bash
docker build
docker compose up
docker run
```

Expected impact if later approved:

- disk: potentially hundreds of MB for Python base image and layers
- RAM: app runtime plus container overhead
- ports: `127.0.0.1:8006`
- server-visible names: `aois-p-api`, `aois-p/api:local`

Allowed by default:

- read Docker files
- validate container plan text
- run `python3 examples/validate_container_plan.py`

## Prerequisites

You should have completed Phase 1.

Required check:

```bash
python3 -m py_compile examples/validate_container_plan.py
python3 examples/validate_container_plan.py
```

## Core Concepts

## Dockerfile

A Dockerfile defines how to build an image.

It is not the image itself.
The image is created only when a build runs.

## Build Context

Build context is the directory sent to Docker during build.

If `.venv`, `.git`, or curriculum files are included accidentally, the build becomes larger and slower.

## `.dockerignore`

`.dockerignore` excludes files from build context.

This version excludes:

- `.git`
- `.venv`
- `__pycache__`
- `.env`
- `curriculum`

## Non-Root User

The container runs as `aois`, not root.

This reduces damage if the app process is compromised.

## Resource Limits

`compose.yaml` declares:

- `mem_limit: 256m`
- `cpus: "0.50"`
- `read_only: true`
- `tmpfs` for `/tmp`

These are practice controls before Kubernetes limits arrive later.

## Build

Inspect:

```bash
sed -n '1,220p' Dockerfile
sed -n '1,220p' compose.yaml
sed -n '1,120p' .dockerignore
```

Compile validator:

```bash
python3 -m py_compile examples/validate_container_plan.py
```

Run validator:

```bash
python3 examples/validate_container_plan.py
```

Expected output:

```json
{
  "docker_build_ran": false,
  "mode": "container_plan_validation_no_build",
  "provider_call_made": false,
  "status": "pass"
}
```

## Ops Lab

Answer from the files:

1. Which service name distinguishes portfolio container resources?
2. Which image name is portfolio-owned?
3. Which port binding prevents public exposure?
4. Which file prevents `.venv` from entering the image context?
5. Which setting limits memory?

Answer key:

1. `aois-p-api`
2. `aois-p/api:local`
3. `127.0.0.1:8006:8006`
4. `.dockerignore`
5. `mem_limit: 256m`

## Break Lab

Do not skip this.

### Option A - Missing `.venv` Ignore

In a scratch copy, remove `.venv` from `.dockerignore`.

Expected risk:

- build context may include the local virtual environment
- image build can become larger and slower

### Option B - Public Port Binding

In a scratch copy, change:

```yaml
"127.0.0.1:8006:8006"
```

to:

```yaml
"8006:8006"
```

Expected risk:

- service could bind beyond localhost

Lesson:

- container configuration is operational security

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. no Docker image is built
4. no container is started
5. you can explain Dockerfile, `.dockerignore`, Compose, and resource limits

## Common Mistakes

- building before checking build context
- including `.venv` in the image
- running as root unnecessarily
- binding ports publicly
- omitting memory and CPU limits
- leaving containers running on a shared server

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_container_plan.py
```

Read `missing` and inspect:

- `Dockerfile`
- `.dockerignore`
- `compose.yaml`

If you want to build:

- stop
- estimate disk impact
- confirm primary AOIS will not be affected
- request approval
- record resource usage after build

## Benchmark

Measure:

- validator compile result
- validator status
- whether Docker build ran
- whether any container was started
- repo disk footprint
- memory snapshot

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can inspect, validate, break, explain, and defend the container plan without building. |
| 4/5 | Plan validates, but one container concept needs review. |
| 3/5 | Files exist, but resource/security reasoning is weak. |
| 2/5 | Dockerfile exists, but runtime risk is unclear. |
| 1/5 | Containerization still means "just docker build." |

Minimum pass: `4/5`.

## Architecture Defense

Why container plan before build?

Because image builds can consume disk and runtime can consume memory.
On a shared server, the plan must be correct before resource use begins.

Why `aois-p` names?

Because server-visible resources must not be confused with the primary AOIS project.

Why localhost binding?

Because this is a local portfolio service, not a public deployment.

## 4-Layer Tool Drill

Tool: Dockerfile

1. Plain English
It describes how to package the app.

2. System Role
It turns AOIS into a portable service unit later.

3. Minimal Technical Definition
It is a declarative image build recipe.

4. Hands-on Proof
The validator confirms non-root user, healthcheck, no-cache install, and uvicorn command without building the image.

## 4-Level System Explanation Drill

1. Simple English
AOIS now has a safe container plan.

2. Practical Explanation
I can inspect Docker and Compose files and validate resource/security controls without building.

3. Technical Explanation
`v4` adds a Dockerfile, `.dockerignore`, Compose service, and validator for portfolio-owned container design.

4. Engineer-Level Explanation
AOIS now separates container design from image/runtime execution, preserving shared-server resource control while preparing for portable deployment.

## Failure Story

Representative failure:

- Symptom: a Docker build unexpectedly uses hundreds of MB more than expected
- Root cause: `.venv` and repo extras entered the build context
- Fix: add `.dockerignore` and validate it
- Prevention: inspect build context before building
- What this taught me: container builds are resource events

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v4` solve in AOIS?
2. What is a Dockerfile?
3. What is build context?
4. What does `.dockerignore` protect?
5. Why use a non-root container user?
6. Why bind to `127.0.0.1`?
7. Why are Docker build and run gated?
8. What does `mem_limit: 256m` protect?
9. Why use `aois-p` names?
10. Explain Dockerfile using the 4-layer tool rule.
11. Explain `v4` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v4` solve in AOIS?

It prepares AOIS for portable container packaging without consuming Docker build/runtime resources yet.

2. What is a Dockerfile?

A recipe for building a container image.

3. What is build context?

The files sent to Docker during image build.

4. What does `.dockerignore` protect?

It keeps unnecessary or sensitive files out of the build context.

5. Why use a non-root container user?

To reduce impact if the app process is compromised.

6. Why bind to `127.0.0.1`?

To keep the practice service local instead of public.

7. Why are Docker build and run gated?

They can consume disk, memory, ports, and server-visible resources.

8. What does `mem_limit: 256m` protect?

It prevents the portfolio container from consuming unbounded memory.

9. Why use `aois-p` names?

To distinguish portfolio-owned server-visible resources from primary AOIS.

10. Explain Dockerfile using the 4-layer tool rule.

- Plain English: it packages the app.
- System Role: it prepares AOIS for portable runtime.
- Minimal Technical Definition: it is an image build recipe.
- Hands-on Proof: the validator checks packaging controls without building.

11. Explain `v4` using the 4-level system explanation rule.

- Simple English: AOIS has a container plan.
- Practical explanation: I can inspect and validate Docker files safely.
- Technical explanation: `v4` adds Dockerfile, Compose, `.dockerignore`, and a validator.
- Engineer-level explanation: AOIS now has container packaging design separated from resource-consuming image/runtime execution.

## Connection Forward

`v4` creates the packaging plan.

`v5` adds security discipline so the packaged service is harder to misuse.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v4 Introduction](02-introduction.md)
- Next: [v4 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
