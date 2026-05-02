# v0.8 Introduction

Authoring status: authored

## What This Version Is About

`v0.8` is Postgres foundations without running a database.

This version teaches how AOIS portfolio data should be shaped before any persistent database process is started on the shared server.

## Why It Matters In AOIS

AOIS needs durable memory.

Incidents, analysis results, and future LLM request plans should not exist only as terminal output.
They need a schema that can later support audit, debugging, historical comparison, and retrieval.

Because the primary AOIS project shares the same server, the portfolio database namespace is `aois_p`.

## How To Use This Version

1. read the schema first
2. identify the three tables
3. explain the foreign keys and constraints
4. compile the validator
5. run the validator
6. break a scratch copy and observe validation failure
7. do not start or install Postgres without explicit approval
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.8 Contents](01-contents.md)
- Next: [v0.8 - Postgres Foundations Without Running A Database](03-notes.md)
<!-- AOIS-NAV-END -->
