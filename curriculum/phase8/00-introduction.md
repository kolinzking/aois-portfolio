# Phase 8 Introduction

Authoring status: authored

Phase 8 turns AOIS from a governed operating model into a human-facing product
surface.

The phase focus is not "make it pretty." The focus is operational usability:

- show incidents, traces, decisions, approvals, budgets, agent state, and execution boundaries
- keep stale state and connection loss visible
- block sensitive rendering until redaction passes
- treat accessibility as release readiness
- add identity and policy-aware access before multi-user use

## Current Progress

Phase 8 is authored through `v27` and is complete.

AOIS-P can now model:

- dashboard panels for every major Phase 7 state family
- ordered event replay for operator visibility
- active panel, badge, and operator action decisions
- stale-state warning
- empty dashboard state
- connection-loss banner
- redaction block
- accessibility block
- role-scoped product visibility
- tenant-scoped resource access
- deny-first policy decisions
- approval separation
- limited break-glass access
- access audit events

## Completed Work

Phase 8 includes:

- `v26`: dashboard and real-time visibility
- `v27`: auth, tenancy, permissions, and policy-aware access

The next phase is Phase 9, starting with `v28` delivery pipeline and release
controls.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../READING-ORDER.md)
- Previous: [Phase 8 Contents](CONTENTS.md)
- Next: [v26 Contents](v26/CONTENTS.md)
<!-- AOIS-NAV-END -->
