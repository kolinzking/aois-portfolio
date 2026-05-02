# v17.5 Introduction

Authoring status: authored

## What This Version Is About

v17.5 introduces service and agent SLOs for AOIS.

An SLO is how AOIS says, "this system is reliable enough" in measurable terms.
For normal services, that means success, latency, and freshness. For AI agents,
it also means quality and safety.

This version is local-only. It defines and validates the reliability policy
without starting Prometheus, Alertmanager, Grafana, an agent runtime, or any
provider call.

## Why It Matters In AOIS

AOIS cannot reach infrastructure maturity by collecting telemetry alone.
Telemetry shows what happened. SLOs decide whether what happened is acceptable.

This matters most with AI agents. An incident agent can return a successful HTTP
response while giving a weak, unsafe, or irrelevant recommendation. If AOIS only
measures API availability, that failure stays hidden.

## How To Use This Version

Use this lesson as a self-paced reliability lab:

1. Read the SLO notes.
2. Inspect the `aois-p` reliability plan.
3. Run the validator.
4. Run the error-budget simulator.
5. Explain when AOIS should page, when it should ticket, and when it should
   freeze risky agent automation.

Do not deploy a live monitoring stack for this lesson. Live monitoring requires
service inventory, retention, storage, dashboards, alert routing, and separation
from the primary AOIS project.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17.5 Contents](CONTENTS.md)
- Next: [v17.5 - Service And Agent SLOs Without Runtime](notes.md)
<!-- AOIS-NAV-END -->
