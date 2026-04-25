# v17 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v17 gives AOIS a safe model for durable event movement. Incident signals and
agent decisions can be represented as versioned events with trace IDs, offsets,
lag, replay, and dead-letter handling.

This unlocks the next layer of operations: deciding whether those event-driven
services and agents are meeting reliability expectations.

## Why The Next Version Exists

v17.5 introduces SLOs for services and agents. Event streaming tells you how
work moves through the system. SLOs tell you whether that movement is good
enough: how fresh events must be, how much lag is acceptable, how often agents
may fail, and when an error budget is being burned.

Carry forward the v17 discipline: no reliability claim is real unless it is
measured, bounded, and connected to an operator action.
