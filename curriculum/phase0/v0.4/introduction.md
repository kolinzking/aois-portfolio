# v0.4 Introduction

`v0.4` is where AOIS stops being only a local shell project and starts speaking over the network.

That shift matters because nearly every later AOIS capability depends on HTTP:

- FastAPI endpoints
- model API calls
- webhooks
- health checks
- cloud service integrations

If HTTP feels like magic, the rest of the system stays fragile.

## What You Will Build

You will build `scripts/http_probe.sh`, a small network inspection script that makes a real request and reports:

- status code
- content type
- response headers
- response time
- body preview

## Why It Matters In AOIS

Later you will call:

- Claude or OpenAI APIs
- internal AOIS endpoints
- GitOps and cloud interfaces

This version gives you the language needed to inspect those flows instead of guessing.

## How To Use This Version

Start with [notes.md](notes.md), build and run the probe in [lab.md](lab.md), keep [runbook.md](runbook.md) as the quick reference, then close with [summarynotes.md](summarynotes.md) and [looking-forward.md](looking-forward.md).
