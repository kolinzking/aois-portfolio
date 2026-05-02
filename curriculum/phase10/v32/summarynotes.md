# v32 Summary Notes

Authoring status: authored

## What Was Built

v32 adds a local edge and offline inference contract:

- `frontier/aois-p/edge-offline-inference.plan.json`
- `examples/validate_edge_offline_inference_plan.py`
- `examples/simulate_edge_offline_inference.py`

The simulator decides whether AOIS-P should run centrally, run edge-online, run
offline from cache, fall back, hold, or block.

## What Was Learned

Key controls:

- deployment target
- connectivity profile
- device profile
- model format and model size budget
- quantization review
- memory, compute, power, and latency budgets
- offline cache, sync, and freshness
- residency and privacy gates
- fallback eligibility
- observability buffer
- update channel and rollback
- access policy and release gate

## Core Limitation Or Tradeoff

v32 does not start edge runtimes, load offline models, download models,
quantize models, access devices, use GPUs or NPUs, read media, call providers,
call the network, or approve live edge deployment. It models the decision
surface before any live deployment work begins.
