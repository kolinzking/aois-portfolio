# v0.6 Introduction

Authoring status: authored

## What This Version Is About

`v0.6` is FastAPI without AI.

This version exposes the Python analyzer from `v0.5` through a local HTTP API.

## Why It Matters In AOIS

AOIS needs a stable API contract before model calls are added.

This version teaches:

- routes
- request models
- response models
- validation
- local server operation
- HTTP inspection with `curl`
- runtime resource discipline on a shared server

## How To Use This Version

1. read the resource gate first
2. inspect `app/main.py`
3. install dependencies only after approval
4. run the server bound to `127.0.0.1`
5. test with `curl`
6. trigger validation failure
7. stop the server immediately after the lab
