# v19 Benchmark

Authoring status: authored

## Measurements

Record these values for the checkpoint:

- Validator status: `pass`
- Simulator status: `pass`
- Runtime services started: `0`
- Fault injections executed: `0`
- Load tests started: `0`
- Stress tools started: `0`
- Pod deletes executed: `0`
- Experiment count: `3`
- Blocked experiment count from simulator
- Repo size after checkpoint
- Virtual environment size after checkpoint
- Host memory available after checkpoint

## Interpretation

The benchmark proves that v19 teaches chaos-engineering discipline without live
fault injection or resource pressure.

The important result is not how much failure AOIS can survive today. The
important result is that AOIS can define safe experiments, block unsafe ones,
protect the primary workload, and connect learning back to incident response.
