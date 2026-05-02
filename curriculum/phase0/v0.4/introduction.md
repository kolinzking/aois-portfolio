# v0.4 Introduction

Authoring status: authored

## What This Version Is About

`v0.4` is networking and HTTP inspection for AOIS.

This version teaches how to inspect a service boundary from the terminal.

## Why It Matters In AOIS

AOIS will soon expose APIs and call model providers.

Before using frameworks, you need to understand:

- URL structure
- local hosts and ports
- request and response behavior
- status codes
- headers and body
- connection failure versus HTTP error

## How To Use This Version

1. read the notes in order
2. build `scripts/http_probe.sh`
3. start the local HTTP server
4. probe it with `curl` and the script
5. stop the server and observe connection failure
6. request a missing path and observe `404`
7. do not move on until the difference is clear
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.4 Contents](CONTENTS.md)
- Next: [v0.4 - Networking And HTTP Inspection](notes.md)
<!-- AOIS-NAV-END -->
