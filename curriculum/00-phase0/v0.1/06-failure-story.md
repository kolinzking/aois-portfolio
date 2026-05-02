# v0.1 Failure Story

Authoring status: authored

## Symptom

The file existed, but it could not be read.

## Root Cause

The permissions removed access.

## Fix

Run:

```bash
chmod 644 /tmp/linux-demo.txt
```

## Prevention

Always inspect permissions with `ls -l` before assuming the file content is the problem.

## What This Taught Me

Linux failures are often state failures:

- wrong permissions
- wrong directory
- wrong assumptions about output

The command can be correct and still fail because the operating context is wrong.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.1 Runbook](05-runbook.md)
- Next: [v0.1 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
