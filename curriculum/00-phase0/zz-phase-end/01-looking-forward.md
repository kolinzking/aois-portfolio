# Phase 0 Looking Forward

Authoring status: authored

Phase 0 established the first AOIS portfolio spine:

`Linux -> Bash -> Git -> HTTP -> Python -> API -> LLM dry-run -> persistence schema`

## What Was Gained

- Linux inspection is no longer abstract.
- Bash scripts can automate repeatable operational checks.
- Git is treated as engineering history.
- HTTP can be inspected directly with `curl`.
- Python can classify simple incident signals.
- FastAPI provides a clean local service boundary.
- LLM requests can be planned without keys, cost, or provider calls.
- Postgres-oriented persistence can be designed without starting a database.

## What Is Still Missing

- real structured AI output
- provider integration under a strict budget
- live persistence runtime
- deployment automation
- observability beyond local scripts
- Kubernetes resource controls for portfolio-owned runtime

## Phase 1 Direction

Phase 1 should begin only after the capstone is passable without rescue.

The next phase should turn the Phase 0 foundation into a more realistic AOIS service path:

1. preserve the deterministic analyzer as a baseline
2. add approval-gated structured AI output
3. keep provider calls auditable
4. keep persistence and runtime work separated from the primary AOIS project
5. use `aois-p` or `aois_p` for server-visible portfolio resources

## Carry Forward Rule

Every future upgrade must preserve this standard:

- self-paced first
- Codex as live teacher when requested
- answer keys included
- break labs included
- resource usage recorded
- no provider, database, Kubernetes, or cloud runtime without explicit approval
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [Phase 0 Capstone - Local AOIS Foundation](00-phase-capstone.md)
- Next: [Phase 1 Start Here](../../01-phase1/00-phase-start/00-start-here.md)
<!-- AOIS-NAV-END -->
