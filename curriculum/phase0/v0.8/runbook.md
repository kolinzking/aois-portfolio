# v0.8 Runbook

Authoring status: authored

## Purpose

Use this runbook when the schema validator fails or when database practice risks touching shared-server runtime.

## Primary Checks

Compile the validator:

```bash
python3 -m py_compile examples/validate_schema.py
```

Run the validator:

```bash
python3 examples/validate_schema.py
```

Inspect schema namespace:

```bash
grep -n "CREATE SCHEMA" sql/aois_schema.sql
```

Inspect provider gate:

```bash
grep -n "provider_call_allowed" sql/aois_schema.sql
```

## Recovery Steps

If the validator reports missing schema:

- confirm `CREATE SCHEMA IF NOT EXISTS aois_p;` exists
- do not rename it to plain `aois`

If a required table is missing:

- restore `aois_p.incidents`
- restore `aois_p.analysis_results`
- restore `aois_p.llm_request_plans`

If a constraint is missing:

- restore the check constraint
- rerun the validator
- explain what invalid data the constraint blocks

If you are about to run Postgres:

- stop
- confirm the target host and database
- confirm the memory/disk budget
- confirm it will not interfere with primary AOIS
- get explicit approval

If you need live database practice later:

- prefer an already-approved isolated database target
- keep objects under `aois_p`
- record disk and memory impact in `RESOURCE-USAGE.md`
