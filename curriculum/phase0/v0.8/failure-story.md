# v0.8 Failure Story

Authoring status: authored

## Symptom

A future analysis row exists, but nobody can tell which incident produced it.

## Root Cause

The analysis result was stored without a required foreign key to an incident.

The database became a pile of rows instead of a connected system memory.

## Fix

Require this relationship:

```sql
incident_id BIGINT NOT NULL REFERENCES aois_p.incidents(id) ON DELETE CASCADE
```

Keep analysis results in:

```sql
aois_p.analysis_results
```

## Prevention

Design relationships before runtime.

Validate the schema before applying it.

Use constraints to make invalid states hard to store.

## What This Taught Me

Persistence is not just saving text.

Good persistence preserves relationships, validity, and later debugging value.
