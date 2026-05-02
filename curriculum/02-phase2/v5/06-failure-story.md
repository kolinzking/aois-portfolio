# v5 Failure Story

Authoring status: authored

## Symptom

A fake provider key appears in output or logs without redaction.

## Root Cause

Input was used before local security inspection.

## Fix

Run inspection before logging or provider boundaries:

```bash
python3 examples/security_inspect.py api_key=sk-example1234567890 gateway failed
```

## Prevention

Keep real secrets out of repo files.

Use redaction before logs and provider calls.

Keep provider calls gated.

## What This Taught Me

Security must happen before data crosses important boundaries.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v5 Runbook](05-runbook.md)
- Next: [v5 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
