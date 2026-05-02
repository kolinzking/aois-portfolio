# v19 Introduction

Authoring status: authored

## What This Version Is About

v19 introduces chaos engineering for AOIS.

Chaos engineering is controlled failure experimentation. It asks whether the
system, operators, and agents behave safely when assumptions are challenged.

This version is local-only. It defines and simulates chaos experiments without
injecting faults, running load tests, creating network faults, stressing memory
or CPU, deleting pods, calling providers, or touching cloud resources.

## Why It Matters In AOIS

AOIS is building toward serious infrastructure operations. That means reliability
cannot only be reactive. Incident response handles failures after they appear.
Chaos engineering tests whether the response model works before the next real
incident.

For AI infrastructure, chaos must include agent failure modes: unsafe
recommendations, low-quality outputs, missing evidence, and risky tool
permissions.

## How To Use This Version

Use this lesson as a self-paced tabletop game-day lab:

1. Read the chaos engineering notes.
2. Inspect the `aois-p` chaos plan.
3. Run the validator.
4. Run the game-day simulator.
5. Explain why one experiment is blocked by guardrails.

Do not run live chaos for this lesson. Live chaos requires blast-radius
approval, SLO budget review, resource review, communication plan, abort
conditions, rollback plan, and explicit protection for the primary AOIS project.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19 Contents](01-contents.md)
- Next: [v19 - Chaos Engineering Without Fault Injection](03-notes.md)
<!-- AOIS-NAV-END -->
