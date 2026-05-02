# v20 Summary Notes

Authoring status: authored

## What Was Built

v20 built a local tool-using incident responder plan:

- read-only tool allowlist
- mutating tool denylist
- step contract
- evidence and schema rules
- decision gates
- local validator
- deterministic simulator

## What Was Learned

The key lesson is that tool use has two parts:

```text
requesting a tool
executing a tool
```

AOIS must govern the second part. The responder can plan useful investigation
steps, but the application boundary decides what can actually run.

## Core Limitation Or Tradeoff

v20 does not prove live agent behavior. That is intentional.

It proves the local decision model first: allowed read-only steps, blocked
secret paths, approval for mutation, evidence gathering, and fallback for
malformed tool output.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20 Benchmark](07-benchmark.md)
- Next: [v20 Looking Forward](09-looking-forward.md)
<!-- AOIS-NAV-END -->
