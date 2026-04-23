# v0.8 Lab

## Build Lab

Inspect:

```bash
sed -n '1,240p' sql/aois_schema.sql
```

## Ops Lab

Answer from the file:

1. where is severity stored?
2. where is analyzer stored?
3. which columns are indexed?

Answer key:

1. `incidents.severity`
2. `analyses.analyzer`
3. `incidents.created_at`, `incidents.severity`, `analyses.incident_id`

## Break Lab

Think through the one-table design mistake.

Expected lesson:

- simpler initial design can make later growth worse

## Explanation Lab

Question:
Why does `analyses` reference `incidents` instead of duplicating the raw log?

Answer:
Because the incident is the operational event and the analysis is an attached interpretation.

## Defense Lab

Why is SQL in Phase 0?

Because persistence is a foundational system concern, not only a later optimization.
