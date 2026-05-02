# v0.4 Failure Story

Authoring status: authored

## Symptom

The probe failed before returning a useful HTTP status code.

## Root Cause

No server was listening on `127.0.0.1:8765`.

## Fix

Start the local server:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Then rerun:

```bash
./scripts/http_probe.sh http://127.0.0.1:8765/
```

## Prevention

Confirm that a service is listening before assuming an HTTP endpoint is returning an error.

## What This Taught Me

Connection failure and HTTP error status are different.

A `404` means the server responded.
A connection failure means the request did not reach a listening HTTP service.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.4 Runbook](05-runbook.md)
- Next: [v0.4 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
