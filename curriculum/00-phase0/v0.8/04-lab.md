# v0.8 Lab

Authoring status: authored

## Build Lab

Build and inspect:

- `sql/aois_schema.sql`
- `examples/validate_schema.py`

Compile:

```bash
python3 -m py_compile examples/validate_schema.py
```

Run:

```bash
python3 examples/validate_schema.py
```

Success state:

- validator returns `status=pass`
- `missing` is empty
- no database server is started
- no dependency is installed
- schema namespace is `aois_p`

## Ops Lab

Answer from the schema:

1. where is the raw incident message stored?
2. where is deterministic analysis stored?
3. where is dry-run LLM request planning stored?
4. which field blocks assumed provider calls?
5. which constraint prevents invalid confidence values?
6. which namespace distinguishes this project on the server?

Then run:

```bash
python3 examples/validate_schema.py
```

The validator should confirm the same design choices.

## Break Lab

Create a scratch copy outside the repo:

```bash
cp sql/aois_schema.sql /tmp/aois_schema_broken.sql
```

Edit `/tmp/aois_schema_broken.sql` and remove:

```sql
provider_call_allowed BOOLEAN NOT NULL DEFAULT false
```

Run:

```bash
python3 examples/validate_schema.py /tmp/aois_schema_broken.sql
```

Expected result:

- `status` becomes `fail`
- `missing` includes `llm_provider_gate`

Do not edit the real schema for the break lab.

## Explanation Lab

Answer without looking at the answer key first:

1. what is a schema?
2. what is a table?
3. what is a primary key?
4. what is a foreign key?
5. what is a constraint?
6. what is an index?
7. why is `aois_p` used?
8. why is this lesson not starting Postgres?

## Defense Lab

Defend:

`Schema design before database runtime is the correct order on a shared 16 GB server.`

Your defense must mention:

- resource safety
- primary AOIS priority
- namespace separation
- constraints
- future auditability
- provider-call gating

## Benchmark Lab

Record:

- validator compile result
- validator JSON result
- repo disk footprint after this version
- whether a database server was started
- whether any dependency was installed
- whether any persistent runtime remains active
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.8 - Postgres Foundations Without Running A Database](03-notes.md)
- Next: [v0.8 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
