# v0.8 - Persistence Foundations For AOIS Incident Memory

Estimated time: 3-4 focused hours

## What This Builds

You build the first durable data model for AOIS using:

- [sql/aois_schema.sql](../../../sql/aois_schema.sql)

## Why This Exists

By the end of `v0.7`, AOIS can observe, classify, serve, and even call a real model.
It still forgets everything.

Persistence matters because later AOIS needs:

- incident history
- analysis history
- auditability
- retrieval
- evaluation datasets

## AOIS Connection

The system path becomes:

`incident arrives -> analysis happens -> record is stored`

That is the first real memory layer in AOIS.

## Learning Goals

By the end of this version you should be able to:

- explain the purpose of the `incidents` and `analyses` tables
- explain why `incident_id` is a foreign key
- explain why timestamps and indexes are present from day one
- defend why persistence belongs in Phase 0 and not only later

## Prerequisites

Run:

```bash
sed -n '1,240p' sql/aois_schema.sql
```

## Core Concepts

### Table

A structured container for related records.

### Primary key

A stable unique identifier for each row.

### Foreign key

A relational connection between tables.

### Index

A structure that makes common lookups faster.

## Build

Inspect the schema carefully:

```bash
sed -n '1,240p' sql/aois_schema.sql
```

What to notice:

- `incidents` stores the incoming operational event
- `analyses` stores the system's interpretation of that event
- one incident can have multiple analyses over time

## Ops Lab

Answer these from the schema:

1. Which table holds the raw log?
2. Which table holds the analyzer name?
3. What happens to analyses if an incident is deleted?

Answer key:

1. `incidents.raw_log`
2. `analyses.analyzer`
3. `ON DELETE CASCADE` removes dependent analyses

## Break Lab

Conceptual break:

Imagine storing the analysis summary directly in the `incidents` table with no separate `analyses` table.

What breaks?

- no history of multiple analyzers
- harder audit trail
- weaker separation between event and interpretation

That design mistake is common and worth feeling now.

## Testing

Syntax check by inspection:

- every `CREATE TABLE` closes cleanly
- indexes reference real columns
- foreign key points to a real primary key

If you have local Postgres available:

```bash
psql "$DATABASE_URL" -f sql/aois_schema.sql
```

## Common Mistakes

### Treating the event and the interpretation as the same thing

They are related but not identical.

### Forgetting timestamps

Operational systems without time fields become much harder to debug or audit.

### Adding a database too late

If persistence appears only after the system grows large, retrofitting becomes harder.

## Troubleshooting

If the schema looks abstract:

- trace one concrete example:
  - incident: `pod OOMKilled exit code 137`
  - analysis: summary, suggestion, analyzer name

If SQL feels unfamiliar:

- focus first on table purpose, relationships, and keys
- syntax will keep getting reinforced later

## Benchmark

The benchmark here is architectural:

- with persistence: AOIS can remember, audit, compare, and retrieve
- without persistence: AOIS resets to zero after each interaction

That is a qualitative performance difference in system capability.

## Architecture Defense

Why split `incidents` and `analyses`:

- keeps event and interpretation distinct
- allows multiple analyses over time
- prepares for human review or re-analysis later

Why not wait until a later phase:

- persistence is part of the system substrate, not an optional add-on

## 4-Layer Tool Drill

### Postgres schema

1. Plain English
It defines how AOIS will remember incidents and analyses.

2. System Role
It is the first durable memory layer for the system.

3. Minimal Technical Definition
It is a SQL schema defining relational tables, constraints, and indexes for operational records.

4. Hands-on Proof
Without it, AOIS can analyze a log once but cannot keep history or build retrieval on top later.

## 4-Level System Explanation Drill

1. Simple English
`v0.8` gives AOIS a memory.

2. Practical Explanation
It defines database tables for incidents and the analyses attached to them.

3. Technical Explanation
It adds a relational schema with primary keys, foreign keys, checks, timestamps, and indexes.

4. Engineer-Level Explanation
`v0.8` establishes the first durable data plane for AOIS by modeling operational events separately from their interpretations, enabling future auditability, retrieval, evaluation, and multi-analyzer workflows.

## Failure Story

The representative failure is collapsing everything into one table because it feels simpler.
That design wins briefly and then becomes painful once re-analysis, audit trails, or multiple analyzers arrive.

## Mastery Checkpoint

You are ready to leave `v0.8` when you can:

1. explain every table in the schema
2. explain the foreign key relationship
3. explain why `ON DELETE CASCADE` exists here
4. defend why persistence is part of the foundation, not optional polish
5. explain how this prepares for retrieval and memory later

## Connection Forward

Phase 1 will now connect all of Phase 0 into a real AI-backed service:

- service boundary from `v0.6`
- model call from `v0.7`
- memory substrate from `v0.8`
