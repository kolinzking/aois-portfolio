# AOIS Syllabus

This is the operational syllabus for the AOIS program.

Use it to understand:

- what each phase is for
- which tools and concepts are central in that phase
- what AOIS becomes by the end of that phase
- what you must be able to defend before moving on

Navigation:

- [Global Table Of Contents](TABLE-OF-CONTENTS.md)
- [Full Program Map](FULL-PROGRAM-MAP.md)
- [Corpus Status](CORPUS-STATUS.md)

## How To Read This Syllabus

Each phase is described through five lenses:

- `Goal`: the main purpose of the phase
- `Core tools and concepts`: the minimum concepts that actually carry the phase
- `AOIS deliverables`: what exists in the repo and system by the end
- `Mastery target`: what you should be able to do
- `Interview defense`: what you should be able to explain under pressure

This is not the detailed lesson map.
It is the high-level control surface for the whole program.

## Phase Sequence

The phases are not interchangeable.
They deliberately move AOIS through this order:

`foundation -> intelligence -> portability -> cluster runtime -> enterprise cloud -> inference ownership -> observability -> agent runtime -> product surface -> delivery platform -> frontier expansion`

That order exists so later complexity sits on real operating skill rather than theory.

## Phase 0 - Foundations That Actually Carry Forward

Navigation:

- [Phase 0 Contents](phase0/CONTENTS.md)

Goal:
Build the engineering substrate for the entire system.

Core tools and concepts:

- Linux
- systemd
- Linux performance inspection
- bash
- git
- HTTP
- Python
- FastAPI
- LLM fundamentals
- Postgres
- data modeling

AOIS deliverables:

- machine inspection scripts
- log parsing scripts
- versioned repository workflow
- HTTP interaction exercises
- first typed backend service
- first raw LLM call
- first schema and persistence layer

AOIS after this phase:

- a repo you can operate from the terminal
- a first service boundary
- a first raw AI call
- a first persistence layer

Mastery target:
You can inspect the machine, reason about requests, build a typed service, make a raw LLM call, and explain each component at four layers.

Interview defense:
You can explain why Linux, bash, HTTP, typed Python, FastAPI, LLM fundamentals, and Postgres all had to appear before “real AI engineering” started.

Do not move on until:

- you can operate the repo comfortably from the terminal
- you can explain every Phase 0 component at four layers
- you can show where brittle rules stop and where AI becomes necessary

## Phase 1 - Intelligence Core

Navigation:

- [Phase 1 Contents](phase1/CONTENTS.md)

Goal:
Turn AOIS into a reliable AI analysis service.

Core tools and concepts:

- model APIs
- structured output
- routing
- prompt caching
- cost-aware routing
- validation
- tracing
- evaluation baseline
- Redis as runtime cache
- retrieval foundations

AOIS deliverables:

- AI analysis endpoint
- model routing layer
- reliability and tracing layer
- first cost-aware caching and retrieval behavior

AOIS after this phase:

- a real AI-backed analysis service
- routing and fallback behavior
- traceable and measurable model use

Mastery target:
You can explain why structured AI systems beat ad hoc prompting and you can defend routing, validation, and traceability decisions.

Interview defense:
You can justify why one request goes to a premium reasoning model, another to a cheaper fast path, and how you measure whether that decision was correct.

Do not move on until:

- AOIS returns structured analysis reliably
- routing, fallback, and tracing behavior are visible and explainable
- you can defend model-choice decisions with latency, cost, and quality reasoning

## Phase 2 - Container And Security Base

Navigation:

- [Phase 2 Contents](phase2/CONTENTS.md)

Goal:
Make AOIS portable and safer.

Core tools and concepts:

- Docker
- Compose
- secrets management
- API security
- LLM security
- prompt injection defense
- runtime hardening
- red-team basics

AOIS deliverables:

- containerized service stack
- hardened request path
- security baseline

AOIS after this phase:

- a portable local platform
- a better-defined security posture

Mastery target:
You can explain what becomes safer, faster, or more reproducible because of containerization and security controls.

Interview defense:
You can defend why the same AOIS service should behave similarly across environments and what concrete attack paths you reduced before going to cluster or cloud.

Do not move on until:

- the local AOIS stack is portable through containers
- the obvious API and LLM attack paths have first-pass mitigations
- you can explain which security controls are baseline versus future hardening

## Phase 3 - Cluster And GitOps Operations

Navigation:

- [Phase 3 Contents](phase3/CONTENTS.md)

Goal:
Operate AOIS on real infrastructure.

Core tools and concepts:

- Kubernetes
- pods
- deployments
- services
- ingress
- configmaps
- secrets
- probes
- requests and limits
- scheduling basics
- kubectl debugging
- Helm
- ArgoCD
- KEDA
- workload identity
- mTLS

AOIS deliverables:

- running cluster
- packaged service
- GitOps deployment flow
- autoscaling behavior
- first true distributed AOIS runtime

AOIS after this phase:

- a real deployed cluster service
- declarative rollout and rollback
- service identity and scaling controls

Mastery target:
You can describe how AOIS gets from code to cluster and what controls service identity, rollout, and scaling.

Interview defense:
You can explain why Kubernetes exists in this system, how a request reaches the service, and how you debug the app when the problem is no longer on one machine.

Do not move on until:

- AOIS is actually running on a cluster
- you can trace the path from code to deployment to live service
- you can debug the service with cluster-native tools instead of single-machine habits

## Phase 4 - Enterprise Cloud

Navigation:

- [Phase 4 Contents](phase4/CONTENTS.md)

Goal:
Learn managed-cloud AI infrastructure patterns.

Core tools and concepts:

- Bedrock
- Bedrock Agents
- Lambda
- S3
- RDS
- CloudWatch
- EKS
- IAM
- IRSA

AOIS deliverables:

- managed model integration
- event-driven workloads
- cloud-managed cluster deployment

AOIS after this phase:

- a cloud-mapped AOIS architecture
- managed identities and data-plane services
- a realistic self-managed versus managed-cloud comparison

Mastery target:
You can compare self-managed and cloud-managed AI infrastructure realistically.

Interview defense:
You can explain when Hetzner or self-managed infra is enough, when AWS becomes worth it, and what you gain or lose by moving AOIS into managed cloud services.

Do not move on until:

- you can map AOIS clearly onto managed cloud primitives
- you can compare self-managed versus managed-cloud tradeoffs without hand-waving
- identity, storage, runtime, and observability choices all have explicit reasons

## Phase 5 - Inference And GPU Systems

Navigation:

- [Phase 5 Contents](phase5/CONTENTS.md)

Goal:
Move from API consumption to inference engineering.

Core tools and concepts:

- NVIDIA stack
- GPU scheduling
- GPU operator
- device plugin
- MIG awareness
- vLLM
- NIM
- batching
- caching
- fine-tuning
- quantization

AOIS deliverables:

- self-hosted inference path
- GPU-aware operations
- performance optimization evidence

AOIS after this phase:

- an owned inference path, not just external API dependence
- measurable GPU-serving tradeoffs

Mastery target:
You can explain throughput, latency, memory tradeoffs, and how GPU infra affects model serving.

Interview defense:
You can defend when to keep using managed APIs, when to self-host, and what operational costs appear the moment you introduce GPUs into AOIS.

Do not move on until:

- AOIS has at least one real self-hosted inference path
- GPU-serving tradeoffs are measured, not guessed
- you can explain the operational cost of owning inference infrastructure

## Phase 6 - Observability And Reliability

Navigation:

- [Phase 6 Contents](phase6/CONTENTS.md)

Goal:
Make AOIS legible under load and failure.

Core tools and concepts:

- OpenTelemetry
- Prometheus
- Grafana
- Loki
- Tempo
- Kafka
- eBPF
- chaos engineering
- policy enforcement
- SLOs
- cost telemetry

AOIS deliverables:

- telemetry pipeline
- dashboards
- traces
- event streams
- resilience tests

AOIS after this phase:

- a measurable system under real load and failure
- incident evidence instead of guesswork

Mastery target:
You can investigate incidents with evidence instead of guesses.

Interview defense:
You can explain what happened, how you know, what the blast radius was, and whether the system met its SLOs, budgets, and reliability expectations.

Do not move on until:

- AOIS emits telemetry that supports real incident investigation
- you can answer operational questions with traces, logs, metrics, or event evidence
- reliability and cost expectations are visible as measurable targets

## Phase 7 - Agentic AOIS

Navigation:

- [Phase 7 Contents](phase7/CONTENTS.md)

Goal:
Build AOIS in the real direction of modern AI systems: tools, workflows, agents, governance, and runtime control.

Core tools and concepts:

- tool use
- MCP
- A2A-aware design
- Temporal
- LangGraph
- multi-agent patterns
- policy boundaries
- eval pipelines
- autonomy control
- sandboxed execution
- agent memory
- runtime cost control

AOIS deliverables:

- tool-using agent
- governed tool registry
- durable workflows
- agent evaluation system
- runtime controls
- incident-cost-aware agent runtime

AOIS after this phase:

- a governed tool-using agent runtime
- durable workflows and autonomy limits
- measurable agent behavior under cost and safety constraints

Mastery target:
You can explain agent systems beyond demos: tool trust, failure modes, workflow durability, evaluation, runtime safety, and cost.

Interview defense:
You can defend why the system is an agent instead of a chatbot, what it is allowed to do, how you stop it, and how you prove it behaved acceptably.

Do not move on until:

- the agent can use tools within explicit boundaries
- autonomy, durability, and evaluation are visible in the runtime
- you can explain how governance and cost control limit agent behavior

## Phase 8 - Product And Interface

Navigation:

- [Phase 8 Contents](phase8/CONTENTS.md)

Goal:
Make AOIS useful to humans in real time.

Core tools and concepts:

- React
- WebSockets
- auth
- RBAC
- policy-aware UI

AOIS deliverables:

- dashboard
- live views
- user-aware access control

AOIS after this phase:

- a visible operational product
- a real user surface for the system

Mastery target:
You can show the system, not just describe it.

Interview defense:
You can explain how human users interact with AOIS safely, what they see in real time, and how policy-aware access changes behavior across tenants or roles.

Do not move on until:

- AOIS has a usable human-facing interface
- real-time visibility is available without breaking policy boundaries
- you can explain how access control changes what different users can do and see

## Phase 9 - Delivery And Platform

Navigation:

- [Phase 9 Contents](phase9/CONTENTS.md)

Goal:
Make AOIS easy to ship and repeat.

Core tools and concepts:

- CI/CD
- release policy
- model rollout control
- rollout controls
- signatures
- experiment tracking
- platform engineering

AOIS deliverables:

- delivery pipeline
- repeatable releases
- internal platform foundations

AOIS after this phase:

- a system that can be shipped repeatedly
- a platform that reduces one-off operational work

Mastery target:
You can move from one-off engineering to operational software delivery.

Interview defense:
You can explain how AOIS changes safely over time, how new models or behaviors are rolled out, and how you keep delivery reproducible instead of fragile.

Do not move on until:

- AOIS can be delivered repeatedly through a defined pipeline
- rollout and rollback behavior are explicit
- platform work is reducing operational friction rather than adding abstraction noise

## Phase 10 - Frontier Layer

Navigation:

- [Phase 10 Contents](phase10/CONTENTS.md)

Goal:
Push AOIS into frontier territory without losing rigor.

Core tools and concepts:

- multimodal systems
- edge inference
- red teaming
- governance verification
- computer-use workflows

AOIS deliverables:

- multimodal AOIS path
- offline or edge path
- red-team suite
- governance and compliance proof

AOIS after this phase:

- a frontier-facing system that still has operational discipline
- stronger governance and adversarial proof

Mastery target:
You can discuss frontier AI systems with operational credibility, not hype.

Interview defense:
You can explain why each frontier feature exists, what new risk it creates, and how you preserved control, observability, and governance instead of chasing novelty.

Do not move on until:

- each frontier feature has an operational reason to exist
- new risk introduced by frontier capability is explicitly named and mitigated
- the system is still explainable and governable after the frontier additions

## Cross-Cutting Expectations

These apply in every phase.

- You answer the 4-layer tool drill for every major tool.
- You answer the 4-level system explanation drill for AOIS and major subsystems.
- You run build, ops, break, defense, and benchmark labs.
- You commit every completed version.
- You record one real failure story per version.
- You should always be able to say what AOIS became in the last phase and why the next phase is necessary.

## Program Outcome

When the course is done, the repo should prove that you can:

- build AI systems
- operate them
- observe them
- secure them
- govern them
- evaluate them
- deploy them
- explain them clearly at multiple levels

That is the standard this syllabus is designed to enforce.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](READING-ORDER.md)
- Previous: [AOIS Institution Index](INSTITUTION-INDEX.md)
- Next: [AOIS Full Program Map](FULL-PROGRAM-MAP.md)
<!-- AOIS-NAV-END -->
