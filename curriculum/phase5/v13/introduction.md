# v13 Introduction

Authoring status: authored

## What This Version Is About

`v13` starts Phase 5: inference and GPU engineering.

It defines a GPU-backed inference service contract without running a GPU.

The lesson introduces the operational shift from "call an AI API" to "own the inference path."

## Why It Matters In AOIS

AOIS cannot reach frontier AI infrastructure maturity by only consuming external APIs.

Owning inference means AOIS must understand runtime, model artifacts, memory, latency, throughput, observability, cost, and failure behavior.

This version keeps the learning safe on the current server by using only a plan, validator, and simulator.

## How To Use This Version

Run the validator and simulator locally.

Focus on the contract:

- what the request must contain
- what the response must prove
- what performance must be measured
- what must be approved before live GPU work

Do not install drivers, download models, build images, or start GPU services during this lesson.
