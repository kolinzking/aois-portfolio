# v1 Introduction

Authoring status: authored

## What This Version Is About

`v1` creates AOIS's first structured AI endpoint without calling an external AI provider.

The route behaves like an intelligence endpoint, but it returns a dry-run structured contract and keeps provider execution blocked.

## Why It Matters In AOIS

AOIS needs structured, inspectable intelligence.

If the first AI endpoint simply returns free-form text from a provider, later automation becomes fragile.
This version forces the service to define its output fields, provider gate, and deterministic fallback before real inference is introduced.

## How To Use This Version

1. read the provider gate
2. inspect `app/ai_contract.py`
3. inspect `/ai/analyze`
4. compile the Python files
5. run the endpoint briefly
6. prove `provider_call_made=false`
7. prove forced provider use returns `403`
8. stop the server
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v1 Contents](CONTENTS.md)
- Next: [v1 - Structured AI Endpoint Without Provider Calls](notes.md)
<!-- AOIS-NAV-END -->
