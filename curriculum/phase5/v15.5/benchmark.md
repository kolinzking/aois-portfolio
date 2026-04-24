# v15.5 Benchmark

Authoring status: authored

## Measurements

Record:

- validator status
- simulator status
- memory by precision
- speed index by precision
- quality score by precision
- memory reduction versus FP16
- quality delta versus FP16
- repo disk footprint
- memory snapshot

## Interpretation

A passing benchmark proves the local tradeoff simulation is consistent.

It does not prove a real quantized artifact is safe.

Production quantization requires real model artifacts, calibration data, task eval, and approval.
