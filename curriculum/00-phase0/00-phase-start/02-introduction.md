# Phase 0 - Foundations That Carry The Whole System

Authoring status: authored

Phase 0 is where AOIS stops being an idea and becomes an engineering program.

Nothing in this phase is filler.
Everything here becomes load-bearing later:

- Linux and shell literacy
- bash automation
- Git discipline
- HTTP inspection
- Python service foundations
- FastAPI contracts
- LLM request planning
- persistence fundamentals

## What This Phase Is For

By the end of Phase 0, the learner should be able to:

- operate confidently in a Linux terminal
- automate simple operational work with bash
- understand Git as engineering history, not just a backup button
- inspect APIs manually with `curl`
- write typed Python for AOIS
- expose a clean FastAPI API
- understand how a model request is shaped before provider integration
- design a Postgres persistence schema for incidents, analyses, and planned model calls

That is the minimum floor for serious AI infrastructure work later.

## Why This Phase Exists

The fastest way to build fake AI confidence is to jump directly into frameworks.
The fastest way to build durable AI engineering skill is to understand:

- the machine
- the shell
- the service boundary
- the data boundary
- the model boundary

Phase 0 exists so later complexity never feels magical.

## The Versions

| Version | Focus | Build |
|---|---|---|
| `v0.1` | Linux essentials | direct inspection and failure classification drills |
| `v0.2` | Bash scripting | `scripts/sysinfo.sh` and `scripts/log_analyzer.sh` |
| `v0.3` | Git and GitHub discipline | clean repo history |
| `v0.4` | Networking and HTTP | direct request inspection drills |
| `v0.5` | Python for AOIS | typed utility and model layer |
| `v0.6` | FastAPI without AI | mock AOIS endpoint |
| `v0.7` | LLM fundamentals | provider-neutral dry-run request planning |
| `v0.8` | Postgres foundations | `aois_p` schema and local validator |

## The Phase Arc

The movement of Phase 0 is deliberate:

`operate machine -> automate -> record work -> inspect network -> build typed logic -> expose API -> plan model request -> design persistence`

That sequence becomes the first complete AOIS spine.

## What Phase 1 Will Depend On

Phase 1 only works if Phase 0 is real.

To build a useful AI analysis service later, you first need:

- terminal confidence
- a known API contract
- a typed application model
- an understanding of model limits
- a data shape for incidents and responses

Phase 0 creates that floor.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [Phase 0 Contents](01-contents.md)
- Next: [v0.1 Start Here](../v0.1/00-start-here.md)
<!-- AOIS-NAV-END -->
