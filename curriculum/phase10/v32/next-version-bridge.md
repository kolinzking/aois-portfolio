# v32 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v32 gives AOIS-P an edge and offline deployment contract:

- choose central, edge-online, or offline-edge placement
- require known device profiles
- enforce model size, memory, compute, power, and latency budgets
- require cache, sync, and freshness for offline execution
- require privacy and residency controls
- require observability buffers
- require update channel and rollback
- preserve access and release policy

## Why The Next Version Exists

Placement controls are not enough if hostile inputs can trick the system into
using the wrong tool, trusting the wrong evidence, bypassing policy, hiding
resource failure, or treating stale/offline state as current.

v33 will turn the v31 multimodal contract and v32 edge/offline contract into
red-team scenarios that try to break the controls before live use.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v32 Looking Forward](looking-forward.md)
- Next: [v33 Start Here](../v33/00-start-here.md)
<!-- AOIS-NAV-END -->
