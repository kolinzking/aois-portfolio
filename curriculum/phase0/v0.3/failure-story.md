# v0.3 Failure Story

Authoring status: authored

## Symptom

Unrelated files were almost committed together.

## Root Cause

Staging happened before reviewing status and diff.

## Fix

Inspect first:

```bash
git status --short
git diff
git diff --cached
```

If a file is staged but does not belong:

```bash
git restore --staged <path>
```

## Prevention

Commit one coherent decision at a time.
Read the diff before staging or committing.

## What This Taught Me

Git mistakes are often judgment failures, not command failures.

The command can be valid and the commit can still be bad if unrelated changes are mixed together.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.3 Runbook](runbook.md)
- Next: [v0.3 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
