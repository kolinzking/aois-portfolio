# v0.5 Failure Story

Authoring status: authored

## Symptom

The CLI crashed with `ValueError` when given an empty message.

## Root Cause

`IncidentInput` validates that the incident message must not be empty.

## Fix

Pass a meaningful message:

```bash
python3 examples/analyze_incident.py "gateway returned 5xx"
```

## Prevention

Validate inputs at system boundaries and fail clearly when the input is meaningless.

## What This Taught Me

Clear validation failure is better than fake analysis.

AOIS should not pretend an empty signal can produce useful intelligence.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.5 Runbook](runbook.md)
- Next: [v0.5 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
