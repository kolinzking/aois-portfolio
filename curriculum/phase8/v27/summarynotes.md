# v27 Summary Notes

Authoring status: authored

## What Was Built

A local AOIS-P policy-aware access contract:

- role catalog
- resource catalog
- permission matrix
- deny-first policy order
- 12 access cases
- validator
- deterministic simulator

## What Was Learned

- authentication identifies the subject
- authorization decides whether the subject may act
- tenant context must be bound to identity
- roles should grant explicit resource actions, not broad dashboard access
- redaction is an access gate
- approvers still need relationship checks
- break-glass access must be narrow, redacted, and audited
- access decisions are product behavior, not only backend checks

## Core Limitation Or Tradeoff

v27 does not implement live login, SSO, token validation, cookie sessions,
database row-level security, or a real policy engine. It intentionally freezes
the access contract first so the live implementation in a future product can
be tested against known allow and deny behavior.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v27 Benchmark](benchmark.md)
- Next: [v27 Looking Forward](looking-forward.md)
<!-- AOIS-NAV-END -->
