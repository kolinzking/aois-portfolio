# v18 Introduction

Authoring status: authored

## What This Version Is About

v18 introduces incident response maturity for AOIS.

SLOs tell AOIS when reliability or trust is degrading. Incident response defines
what happens next: who leads, what severity means, how updates are written, how
mitigation is chosen, and how the system learns afterward.

This version is local-only. It defines and validates incident response policy
without starting pager, ticketing, chatops, status page, agent runtime, or
provider calls.

## Why It Matters In AOIS

AI infrastructure needs incident response for both classic service failures and
AI-specific failures. A model or agent can be available and fast while producing
unsafe recommendations. That is still an incident if trust, safety, or operator
decision quality is degraded.

Incident response prevents confusion by creating roles, severity, timeline,
communication cadence, mitigation ownership, and post-incident learning.

## How To Use This Version

Use this lesson as a self-paced response lab:

1. Read the incident response notes.
2. Inspect the `aois-p` incident response plan.
3. Run the validator.
4. Run the incident timeline simulator.
5. Explain how AOIS should respond when agent trust is degraded.

Do not connect live paging or chatops tooling for this lesson. Live incident
response integration requires on-call policy, routing approval, communication
channels, status page policy, and primary-project separation.
