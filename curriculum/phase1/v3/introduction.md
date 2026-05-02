# v3 Introduction

Authoring status: authored

## What This Version Is About

`v3` is the local reliability baseline for AOIS intelligence.

It adds trace IDs, local evaluation cases, scoring, and a FastAPI eval endpoint without calling any provider.

## Why It Matters In AOIS

AI work becomes fragile when there is no baseline.

Before real model integration, AOIS needs a repeatable way to answer: did the known cases still pass?

## How To Use This Version

1. inspect `app/reliability.py`
2. compile the files
3. run the local eval script
4. inspect trace ID and score
5. run the API endpoint briefly
6. stop the server
7. explain why reliability comes before provider scale
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v3 Contents](CONTENTS.md)
- Next: [v3 - Reliability Baseline Without Provider Calls](notes.md)
<!-- AOIS-NAV-END -->
