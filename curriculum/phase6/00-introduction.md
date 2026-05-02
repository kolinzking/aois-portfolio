# Phase 6 Introduction

Authoring status: authored

Phase 6 is Observability, Streaming, and Reliability.

Phase 5 planned inference and GPU engineering.
Phase 6 makes AOIS behavior visible and failure-testable.

## Phase Objective

Build the ability to see what AOIS does, connect behavior across components, move events reliably, and test failure deliberately.

## Phase Versions

- `v16` unified telemetry
- `v16.5` agent and incident tracing
- `v17` event streaming
- `v17.5` SLOs for service, agent behavior, cost, and quality
- `v18` eBPF and runtime visibility
- `v19` chaos engineering
- `v19.5` AI failure engineering and governance enforcement

## Resource Rule

Observability tools can consume memory and disk.

This phase may author plans, validators, and simulations first. Live collectors, metrics backends, log stores, trace stores, streaming systems, or chaos tooling require explicit approval.

## Phase Completion

Phase 6 is authored through `v19.5`.

AOIS can now model:

- unified telemetry
- agent and incident tracing
- event streaming
- service and agent SLOs
- runtime visibility
- chaos engineering
- AI failure governance

These controls prepare the curriculum for Phase 7 tool-using agents by requiring
traceability, evidence, budgets, incident discipline, failure testing, and
policy gates before agentic action.
