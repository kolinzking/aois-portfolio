# v0.2 Failure Story

Authoring status: authored

## Symptom

The script existed, but it would not execute.

## Root Cause

The file lacked execute permission.

## Fix

Run:

```bash
chmod +x scripts/sysinfo.sh
```

## Prevention

Always inspect permissions with `ls -l` before assuming script logic is broken.

## Second Failure

## Symptom

The analyzer returned `classification=unknown` for a real-looking incident message.

## Root Cause

The wording did not match any rule.

## Fix

Preserve the raw message and inspect whether a new rule is justified.
Do not add broad rules that create false confidence.

## Prevention

Treat rules as explicit pattern matches, not understanding.

## What This Taught Me

Bash rules are useful when the signal is specific.
They become dangerous when the wording changes and the script pretends silence means safety.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.2 Runbook](runbook.md)
- Next: [v0.2 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
