# AOIS Institution Evaluation Card

This card evaluates the current AOIS institution as it exists in the repository now.

It does **not** grade imagined future delivery.
It grades the current curriculum design, structure, coverage, and mastery controls.

Status scale:

- `FRONTIER` = ahead of normal curricula and aligned with real emerging system direction
- `ELITE` = exceptionally strong, integrated, and professionally credible
- `VERY STRONG` = strong and well-placed, but not yet at the highest level of articulation or delivery proof
- `STRONG` = structurally present and useful, but still dependent on later lesson-pack execution depth
- `UNDERWEIGHTED` = present but not yet strong enough

## Layer Count

This institution currently evaluates across 13 layers.

## Evaluation Card

| Layer | Status | Reason |
|---|---|---|
| Linux / Git / Python Foundations | `ELITE` | Phase 0 is now explicitly treated as a backbone phase, not a throwaway intro, and the teaching standard forces operational depth. |
| Backend / API Systems | `ELITE` | FastAPI, contracts, typed services, request flow, async, and reliability are structurally central to AOIS. |
| Persistence / Data Lifecycle | `VERY STRONG` | Postgres, schema reasoning, pgvector foundation, and data lifecycle awareness are present, but retrieval lesson packs are not yet written. |
| AI Core / Structured LLM Engineering | `ELITE` | Structured output, routing, validation, prompt caching, and traceability are institutionally anchored. |
| Cost / Routing Economics | `ELITE` | Cost accounting, per-step attribution, budget-aware routing, and model tradeoff thinking are explicitly built into the system. |
| Caching / Retrieval / Memory | `VERY STRONG` | Redis, RAG, retrieval foundations, pgvector, and memory design are now present, but still need delivery proof in lesson packs. |
| Kubernetes / GitOps / Platform Runtime | `ELITE` | k8s is now explicitly protected as a backbone domain with pods, deployments, services, ingress, probes, requests/limits, debugging, Helm, ArgoCD, and KEDA. |
| Cloud (Hetzner + AWS) | `VERY STRONG` | The self-managed and managed-cloud split is strong and realistic, with Hetzner plus AWS enterprise patterns, but final delivery depth will determine whether it becomes elite. |
| NVIDIA / Inference Engineering | `VERY STRONG` | NIM, vLLM, GPU operator, device plugin, MIG, batching, quantization, and throughput tradeoffs are present; this is strong but not yet as deeply expressed as the very best inference curricula. |
| Observability / SRE | `ELITE` | OTel, Prometheus, Grafana, Loki, Tempo, Kafka, eBPF, chaos, SLOs, and cost telemetry are all integrated into the institution. |
| Agents / Runtime Control | `ELITE` | Tool use, memory, orchestration, evals, runtime controls, kill switch, canary behavior, and safe execution are all present as first-class layers. |
| Protocols (MCP / A2A / Tool Governance) | `FRONTIER` | These are explicitly included at the right level: not hype-only, but recognized as emerging infrastructure and governance layers. |
| Security / Identity / Governance | `ELITE` | OWASP, guardrails, red-team basics, workload identity, capability boundaries, policy controls, and governance are structurally integrated. |

## Score Summary

- `FRONTIER`: 1
- `ELITE`: 7
- `VERY STRONG`: 4
- `STRONG`: 0
- `UNDERWEIGHTED`: 0

## Comparison To The Reference Card

Reference card:

- 11 layers
- 5 elite
- 1 frontier
- 1 very strong
- 4 strong

Current AOIS institution:

- 13 layers
- 7 elite
- 1 frontier
- 4 very strong
- 0 strong

## Honest Interpretation

By design quality, this institution is currently stronger than the reference card.

Why:

- more explicit mastery controls
- stronger continuity and repo-ownership discipline
- stronger cost-engineering integration
- stronger runtime-control treatment for agents
- stronger protection against brushing past backbone concepts

But there is one important qualification:

The reference card may have more **delivered lesson depth** in some areas than the current AOIS institution, because many AOIS lesson packs are still to be authored.

So the honest statement is:

The AOIS institution is stronger as a curriculum architecture.
Its final superiority depends on whether the lesson-pack delivery keeps pace with the design standard.

## Current Weakest Risk

The greatest current risk is not missing layers anymore.
The greatest risk is execution drift:

- if later notes become too shallow
- if backbone phases are rushed
- if advanced layers are described before they are operationally earned

That is why the `VERSION-STANDARD.md` rules matter so much.

## Current Verdict

The institution is now:

- broad enough for frontier-aligned AI systems engineering
- structured enough for mastery
- protected enough against obvious curriculum drift

It is not finished.
It is now worthy of being executed.
