# v17 Summary Notes

Authoring status: authored

## What Was Built

A local-only event streaming lesson for AOIS:

- `streaming/aois-p/event-streaming.plan.json`
- `examples/validate_event_streaming_plan.py`
- `examples/simulate_event_streaming.py`
- v17 curriculum notes, lab, runbook, benchmark, failure story, and bridge

No broker, producer, consumer, container, cloud resource, or persistent runtime
was started.

## What Was Learned

You learned that event streaming is not just "messages between services." A
safe stream needs a contract, topic, partition key, producer controls, consumer
offsets, lag monitoring, replay rules, dead-letter handling, retention, and
backpressure.

You also learned why self-paced infrastructure training should design and test
the safety model before adding live systems that consume memory and disk.

## Core Limitation Or Tradeoff

v17 does not prove real broker throughput, real durability, or real operational
latency. That is intentional. The tradeoff is lower realism in exchange for
zero runtime footprint on a shared server. A live broker should only be added
after resource budgets and primary-project isolation are explicit.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17 Benchmark](benchmark.md)
- Next: [v17 Looking Forward](looking-forward.md)
<!-- AOIS-NAV-END -->
