# v11 Looking Forward

Authoring status: authored

## What You Should Carry Forward

Carry forward these rules:

1. Queue-based systems must be idempotent.
2. Retries must be bounded.
3. Failed messages need DLQ handling and replay discipline.
4. Trace IDs must cross every hop.
5. Portfolio resources must stay visibly separate as `aois-p`.
6. Cloud workflow creation requires explicit approval.

## What The Next Version Will Build On

`v12` builds on event workflow planning by adding observability and cost-control planning.

The next question is:

How does AOIS know an event workflow is healthy, affordable, and safe before live operation?
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v11 Summary Notes](summarynotes.md)
- Next: [v11 Next Version Bridge](next-version-bridge.md)
<!-- AOIS-NAV-END -->
