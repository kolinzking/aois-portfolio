# v10.5 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

`v10.5` separates agent ownership from provider inference.

AOIS can now say:

- model execution may be delegated later
- agent orchestration remains owned until controls exist
- managed-agent creation needs explicit approval

## Why The Next Version Exists

The next version moves from agent ownership to event-driven workflow planning.

Once AOIS understands who owns the agent loop, it can compare how work is triggered and coordinated:

- API request
- background job
- queue event
- serverless function
- scheduled workflow

`v11` keeps the same discipline: plan first, validate locally, do not create cloud resources without approval.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v10.5 Looking Forward](looking-forward.md)
- Next: [v11 Contents](../v11/CONTENTS.md)
<!-- AOIS-NAV-END -->
