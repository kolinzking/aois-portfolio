# v0.8 Runbook

## Purpose

Use this when the AOIS memory schema needs to be inspected quickly.

## Primary Checks

```bash
sed -n '1,240p' sql/aois_schema.sql
```

If Postgres is available:

```bash
psql "$DATABASE_URL" -f sql/aois_schema.sql
```

## Recovery Steps

If the relationship is unclear:

- start with `incidents`
- then trace `analyses.incident_id`

If SQL feels too dense:

- reduce it to table purpose, key, and relationship first
