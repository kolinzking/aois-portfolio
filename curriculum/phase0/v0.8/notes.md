# v0.8 - Postgres Foundations Without Running A Database

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: no database install, no database server, SQL design and local validation only

## What This Builds

This version builds `sql/aois_schema.sql`, a Postgres-oriented persistence schema for the AOIS portfolio project.

It also adds `examples/validate_schema.py`, a standard-library validator that checks the schema text without connecting to a database.

You will model:

- a portfolio database namespace: `aois_p`
- incidents
- deterministic analysis results
- dry-run LLM request plans
- foreign keys
- check constraints
- indexes
- provider-call gating in stored request plans

## Why This Exists

AI infrastructure needs durable state.

Terminal output is useful for learning, but operations systems need records that can be inspected later:

- what incident arrived
- when it arrived
- what analysis was produced
- which analyzer produced it
- what model request was planned
- whether an external provider call was allowed

This version teaches database design before running a database process on the shared server.

## AOIS Connection

The AOIS path is now:

`incident signal -> API/analyzer -> persistence schema -> future queryable history`

`v0.6` exposed analysis through HTTP.
`v0.7` planned model calls without using a provider.
`v0.8` gives both outputs somewhere safe and structured to live later.

Because this server also runs the primary AOIS project, any future database objects from this portfolio curriculum must use the `aois_p` namespace.

## Learning Goals

By the end of this version you should be able to:

- explain why AOIS needs durable records
- explain a table, row, column, primary key, foreign key, index, and constraint
- explain why `aois_p` is used for server-visible database objects
- explain how incidents connect to analysis results
- explain how LLM request plans connect to provider gating
- validate schema intent without starting Postgres
- explain why running a database server requires explicit resource approval

## Resource Gate

Do not install, start, or connect to Postgres in this version by default.

Expected impact:

- disk: small SQL/Python/Markdown edits only
- RAM: no persistent runtime
- network: none
- database server: none
- external API/cloud usage: none

Live database execution requires explicit approval, a target database, and a resource budget.

## Prerequisites

You should have completed:

- `v0.1` Linux inspection
- `v0.2` Bash automation
- `v0.3` Git discipline
- `v0.4` HTTP inspection
- `v0.5` Python logic
- `v0.6` API contracts
- `v0.7` LLM request planning

Required checks:

```bash
python3 -m py_compile examples/validate_schema.py
python3 examples/validate_schema.py
```

## Core Concepts

## Database

A database stores structured records so they can be queried later.

For AOIS, this means incidents and analyses are not lost after terminal output disappears.

## Schema

A schema is a namespace inside a database.

This curriculum uses:

```sql
CREATE SCHEMA IF NOT EXISTS aois_p;
```

`aois_p` means AOIS portfolio.
It is used because database objects are server-visible if they are ever applied.

## Table

A table stores one kind of record.

This version defines:

- `aois_p.incidents`
- `aois_p.analysis_results`
- `aois_p.llm_request_plans`

## Primary Key

A primary key uniquely identifies each row.

Example:

```sql
id BIGSERIAL PRIMARY KEY
```

## Foreign Key

A foreign key connects one table to another.

Example:

```sql
incident_id BIGINT NOT NULL REFERENCES aois_p.incidents(id)
```

This means an analysis result belongs to an incident.

## Constraint

A constraint rejects invalid data.

Examples:

- incident message cannot be empty
- severity must be `low`, `medium`, `high`, or `unknown`
- confidence must be between `0` and `1`
- provider calls default to not allowed

## Index

An index helps common lookups.

This version indexes:

- recent incidents by `created_at`
- incidents by `status`
- analysis results by `incident_id`
- LLM request plans by `incident_id`

## Build

Inspect the schema:

```bash
sed -n '1,220p' sql/aois_schema.sql
```

Compile the validator:

```bash
python3 -m py_compile examples/validate_schema.py
```

Run the validator:

```bash
python3 examples/validate_schema.py
```

Expected output shape:

```json
{
  "missing": [],
  "required_checks": 10,
  "schema_path": "sql/aois_schema.sql",
  "status": "pass"
}
```

Do not run `psql` or create a database unless that runtime step is explicitly approved.

## Ops Lab

Read the schema and answer:

1. Which schema namespace distinguishes this project from the primary AOIS project?
2. Which table stores raw incident messages?
3. Which table stores deterministic analysis results?
4. Which table stores planned model request metadata?
5. Which field prevents provider calls from being assumed allowed?

Answer key:

1. `aois_p`
2. `aois_p.incidents`
3. `aois_p.analysis_results`
4. `aois_p.llm_request_plans`
5. `provider_call_allowed`

## Break Lab

Do not skip this.

### Option A - Remove Provider Gate

Temporarily remove this line from a scratch copy of the schema:

```sql
provider_call_allowed BOOLEAN NOT NULL DEFAULT false
```

Run:

```bash
python3 examples/validate_schema.py /tmp/aois_schema_broken.sql
```

Expected symptom:

- validator status becomes `fail`
- missing includes `llm_provider_gate`

Lesson:

- provider gating belongs in the data model, not only in memory

### Option B - Remove Confidence Constraint

Temporarily remove the confidence check from a scratch copy.

Expected symptom:

- validator status becomes `fail`
- missing includes `analysis_confidence_check`

Lesson:

- analysis confidence should be bounded before later AI scoring is introduced

## Testing

The version passes when:

1. the schema file exists
2. the validator compiles
3. the validator returns `status=pass`
4. no Postgres server is started
5. no package is installed
6. you can explain all three tables and their relationship
7. you can explain why `aois_p` is the database namespace

## Common Mistakes

- starting a database before understanding the schema
- using the same database namespace as the primary AOIS project
- storing analysis text without linking it to an incident
- omitting constraints because "the app will validate it"
- treating indexes as optional decoration
- allowing provider calls without storing an explicit gate

## Troubleshooting

If validator compilation fails:

```bash
python3 -m py_compile examples/validate_schema.py
```

If validator status is `fail`:

- read the `missing` list
- inspect the required schema section
- fix the schema, not the validator

If you want to run the schema in Postgres:

- stop
- confirm whether a Postgres server already exists
- confirm the target database
- confirm memory and disk budget
- use `aois_p`
- get explicit approval before starting or installing anything

## Benchmark

Measure:

- can the validator compile?
- can the schema pass validation?
- can you identify each table?
- can you explain each foreign key?
- can you explain why provider calls default to blocked?
- can you explain why no DB server was started?

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can design, validate, explain, and defend the persistence schema without running a database. |
| 4/5 | Schema validation passes, but one database concept needs review. |
| 3/5 | The validator runs, but relationships or constraints are unclear. |
| 2/5 | The schema exists, but database design feels like copy/paste. |
| 1/5 | Persistence still feels like magic storage. |

Minimum pass: `4/5`.

## Architecture Defense

Why schema before running Postgres?

Because persistence design should be understood before adding a long-running database process to a shared server.

Why `aois_p`?

Because the primary AOIS project has priority.
Portfolio database objects must be unambiguous if they are ever applied on the same host or cluster.

Why store LLM request plans?

Because AI infrastructure must be auditable.
AOIS should be able to inspect what it planned to ask, what it estimated, and whether a real provider call was allowed.

## 4-Layer Tool Drill

Tool: database schema

1. Plain English
A schema describes the shape of stored records.

2. System Role
It gives AOIS durable memory for incidents, analyses, and future model request plans.

3. Minimal Technical Definition
It is SQL DDL defining namespaces, tables, columns, keys, constraints, and indexes.

4. Hands-on Proof
The validator checks that required tables, constraints, foreign keys, and provider gates exist without starting a database.

## 4-Level System Explanation Drill

1. Simple English
I learned how AOIS will remember incidents and analysis results.

2. Practical Explanation
I can read the SQL schema, identify tables, explain relationships, and validate the schema locally.

3. Technical Explanation
`v0.8` defines Postgres-oriented DDL under the `aois_p` schema for incidents, analysis results, and LLM request plans, with constraints and indexes.

4. Engineer-Level Explanation
AOIS now has a persistence boundary that separates schema design from runtime database operation, protects the primary server by avoiding a database install, and reserves an unambiguous `aois_p` namespace for future portfolio-owned database objects.

## Failure Story

Representative failure:

- Symptom: a future database contains analysis rows that cannot be tied to any incident
- Root cause: analysis records were stored without a foreign key to incidents
- Fix: require `incident_id` on `aois_p.analysis_results`
- Prevention: validate relationships before creating runtime tables
- What this taught me: persistence is not just storage; it is system memory with relationships

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v0.8` solve in AOIS?
2. Why does this lesson not start Postgres by default?
3. What is a database schema?
4. Why is the schema named `aois_p`?
5. What does `aois_p.incidents` store?
6. What does `aois_p.analysis_results` store?
7. What does `aois_p.llm_request_plans` store?
8. What is a primary key?
9. What is a foreign key?
10. What is a check constraint?
11. Why should provider-call permission be stored explicitly?
12. Explain database schema using the 4-layer tool rule.
13. Explain `v0.8` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v0.8` solve in AOIS?

It gives AOIS a persistence design so incidents, analysis results, and planned LLM calls can become durable records.

2. Why does this lesson not start Postgres by default?

Because the shared server has strict resource constraints and the primary AOIS project takes priority.
Schema design can be learned and validated without starting a database process.

3. What is a database schema?

A schema is a namespace that organizes database objects such as tables and indexes.

4. Why is the schema named `aois_p`?

It distinguishes AOIS portfolio database objects from the primary AOIS project if the schema is ever applied on the server.

5. What does `aois_p.incidents` store?

Raw incident signals, their source, status, and creation time.

6. What does `aois_p.analysis_results` store?

Structured deterministic analysis linked to an incident.

7. What does `aois_p.llm_request_plans` store?

Planned LLM request metadata such as prompts, model placeholder, output budget, estimated tokens, estimated cost, latency budget, and provider-call permission.

8. What is a primary key?

A column or set of columns that uniquely identifies each row in a table.

9. What is a foreign key?

A column that links a row in one table to a row in another table.

10. What is a check constraint?

A rule enforced by the database to reject invalid values.

11. Why should provider-call permission be stored explicitly?

Because external AI calls involve cost, keys, data exposure, latency, and approval.
The system should not infer that a provider call is allowed.

12. Explain database schema using the 4-layer tool rule.

- Plain English: it describes how records are stored.
- System Role: it gives AOIS durable memory.
- Minimal Technical Definition: it is SQL DDL for schemas, tables, columns, keys, constraints, and indexes.
- Hands-on Proof: the local validator confirms required persistence structures without running Postgres.

13. Explain `v0.8` using the 4-level system explanation rule.

- Simple English: I learned how AOIS will remember data.
- Practical explanation: I can inspect and validate the SQL schema.
- Technical explanation: `v0.8` defines `aois_p` tables for incidents, analysis results, and LLM request plans.
- Engineer-level explanation: AOIS now has a resource-safe persistence design that separates schema correctness from database runtime and protects shared-server boundaries.

## Connection Forward

`v0.8` completes the Phase 0 foundation:

`Linux -> Bash -> Git -> HTTP -> Python -> API -> LLM planning -> persistence design`

The phase capstone combines the pieces into a self-paced AOIS portfolio foundation.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.8 Introduction](introduction.md)
- Next: [v0.8 Lab](lab.md)
<!-- AOIS-NAV-END -->
