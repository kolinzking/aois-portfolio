# v26 Introduction

Authoring status: authored

## What This Version Is About

v26 starts Phase 8 by turning AOIS-P's governed operational state into a
dashboard visibility contract.

The lesson does not build a live React app. It defines the operator panels,
event model, dashboard state decisions, stale-state warnings, redaction gates,
accessibility gates, and connection-loss handling that a product surface must
support before implementation.

## Why It Matters In AOIS

Phase 7 made AOIS-P govern agentic work. Operators still need to see what is
happening.

A system can have good backend controls and still be unsafe to operate if the
UI hides approvals, stale traces, budget risk, agent handoffs, or execution
boundary decisions. v26 makes those states first-class dashboard concepts.

## How To Use This Version

Read `notes.md`, inspect the plan, run the validator, and run the simulator.
Then use the break lab to change one dashboard-control field at a time.

Do not start a frontend, API server, WebSocket stream, SSE stream, browser, or
provider in this version. v26 proves the visibility contract locally.
