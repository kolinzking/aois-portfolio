# AOIS Master Curriculum

AOIS stands for AI Operations Intelligence System.

This curriculum is built around one system and one outcome:

Build a real AI platform end to end until you can explain it, operate it, secure it, evaluate it, and evolve it like a frontier engineer.

This is not a set of disconnected lessons.
This is one continuous engineering program.

## Program Design Principles

This curriculum is designed to satisfy six non-negotiable goals:

1. Practical mastery, not passive familiarity
2. Deep conceptual understanding, not command memorization
3. Repeated use of the same tools so knowledge compounds
4. Agentic AI as a core strand, not an afterthought
5. AI infrastructure depth, not just model API usage
6. Explanation ability at multiple levels, so your mastery is visible
7. Self-paced completeness, so progress does not depend on live access to the teacher
8. Basic-to-frontier progression, so advanced infrastructure rests on real understanding

## Mastery Preservation Rule

The curriculum is allowed to grow in capability coverage.
It is not allowed to grow in a way that weakens delivery.

That means:

- no tool is added just because it is popular
- every tool must earn its place in AOIS
- every tool must satisfy the four-layer rule
- every advanced topic must appear through build, use, failure, and defense
- frontier coverage must not become theory overload

The goal is not breadth by accumulation.
The goal is depth through repeated system use.

## Institutional Promise

AOIS is not just a roadmap.
It is intended to become a complete self-study institution for AI infrastructure mastery.

That means the written material itself must eventually be strong enough to:

- teach a near-beginner from the ground up
- progress step by step without hidden jumps
- produce practical competence through repeated build-and-operate loops
- remain useful even when live Codex guidance is unavailable
- carry the learner all the way to frontier-relevant systems thinking

This promise is non-negotiable during the rebuild.

## The AOIS System Spine

Everything in the program maps to this spine:

`signals -> ingest -> store -> retrieve -> analyze -> decide -> act -> observe -> evaluate -> govern -> improve`

That spine evolves across the full course.

At the start, AOIS is a local service that analyzes logs.
At the end, AOIS is an observable, governed, agentic AI system running across real infrastructure.

## The Four-Layer Tool Rule

For every tool, framework, or subsystem, you must understand it at four levels.

1. Plain English
What problem does this solve?

2. System Role
Where does it sit in AOIS and what does it interact with?

3. Minimal Technical Definition
What is it technically?

4. Hands-on Proof
What changes when it is removed, broken, or misconfigured?

If you cannot answer all four, the tool is not mastered yet.

This rule applies to everything:

- FastAPI
- Docker
- Postgres
- Redis
- RAG
- LiteLLM
- Groq
- prompt caching
- OpenTelemetry
- Kubernetes
- LangGraph
- MCP
- Temporal
- vLLM
- NVIDIA NIM
- Redis
- pgvector
- ArgoCD
- Bedrock
- Bedrock Agents
- OPA
- SPIFFE/SPIRE
- OpenFeature
- AgentOps
- Grafana

## The Four-Level System Explanation Rule

You must also be able to explain AOIS itself at four levels.

1. Simple English
2. Practical explanation
3. Technical explanation
4. Engineer-level explanation

This becomes a required checkpoint in every version.

## Permanent Learning Loops

Every version uses the same five loops:

1. Build something real
2. Inspect and operate it from the terminal
3. Break it and diagnose it
4. Explain it in plain and technical language
5. Defend the design with tradeoffs

This is how the course creates direct learning and osmosis at the same time.

## What Repeats Across The Entire Program

These are not early topics that disappear.
They remain active throughout the course.

- shell usage
- git discipline
- HTTP inspection
- Python typing and debugging
- JSON contracts
- environment management
- logs and telemetry
- testing
- benchmarking
- cost accounting
- security checks
- architecture explanation
- failure analysis

## Phase Map

### Phase 0 - Foundations That Do Real Work

Purpose:
Build the engineering substrate that everything else depends on.

Versions:

- v0.1 Linux, processes, files, permissions, direct system inspection
- v0.2 Bash, parsing, automation, reusable scripts, rule-based log interpretation
- v0.3 Git, repo hygiene, branch logic, commit thinking, PR mindset
- v0.4 Networking, TCP/IP, DNS, ports, HTTP, `curl`, request tracing
- v0.5 Python core, venvs, packages, typing, async, errors, Pydantic
- v0.6 FastAPI without AI, contracts, routing, middleware, validation
- v0.7 LLM fundamentals, prompts, tokens, cost, latency, provider-neutral request planning
- v0.8 Postgres foundations, schema design, incident storage, relationships, constraints, server-visible namespace discipline

AOIS after Phase 0:

- local scripts
- mock API
- first real backend service
- first provider-gated AI request plans
- first persistence design

### Phase 1 - Intelligence Core

Purpose:
Turn AOIS into a reliable AI-backed service.

Versions:

- v1 AI analysis endpoint with structured output
- v2 model routing, fallbacks, cost tiers, latency-aware choice, Groq fast path, prompt caching economics
- v3 reliability layer: validation, tracing, prompt iteration, eval baseline, Langfuse or equivalent, Instructor-style guarantees

AOIS after Phase 1:

- real AI endpoint
- structured responses
- routing and fallback logic
- request tracing
- eval foundation

### Phase 2 - Containerization and Security

Purpose:
Make the system portable, safer, and harder to misuse.

Versions:

- v4 Docker, Compose, image design, local service stack
- v5 API security, LLM security, prompt injection defense, secrets discipline, policy basics, guardrails, red-team basics

AOIS after Phase 2:

- containerized local platform
- hardened API surface

### Phase 3 - Infrastructure and GitOps

Purpose:
Operate AOIS on real infrastructure with deployment discipline.

Versions:

- v6 real cluster on low-cost infrastructure
- v6.5 workload identity, mTLS, trust between services
- v7 Helm packaging
- v8 GitOps and ArgoCD
- v9 autoscaling and event-driven behavior, KEDA, streaming-driven scale decisions

AOIS after Phase 3:

- real cluster deployment
- service identity
- reproducible rollout model

### Phase 4 - Enterprise Cloud

Purpose:
Learn the managed-cloud equivalents and their tradeoffs.

Versions:

- v10 Bedrock or enterprise model layer
- v10.5 enterprise managed agent path and cloud-side agent tradeoffs
- v11 Lambda and event-driven AI workflows
- v12 EKS, IAM, IRSA, managed operations

### Phase 5 - Inference and GPU Engineering

Purpose:
Own inference infrastructure, not just AI APIs.

Versions:

- v13 NVIDIA inference services
- v13.5 GPU operator, device plugin, scheduling, observability, MIG, Triton-style serving awareness
- v14 vLLM and throughput engineering
- v14.5 caching, batching, latency-throughput tradeoffs, speculative decoding, quantization tradeoffs
- v15 fine-tuning and adaptation
- v15.5 quantization and memory economics

### Phase 6 - Observability and Reliability

Purpose:
See everything the system does and test failure deliberately.

Versions:

- v16 OpenTelemetry
- v16.5 agent and incident tracing
- v17 Kafka and streaming pipelines
- v17.5 SLOs for service and agent behavior, cost SLOs, quality SLOs
- v18 eBPF, deep runtime visibility, runtime security signals
- v19 chaos engineering
- v19.5 AI failure engineering, governance enforcement, policy boundaries

### Phase 7 - Agentic AOIS

Purpose:
Build the system in the direction AI is actually going: tool use, workflows, agents, governance, runtime control.

Versions:

- v20 tool-using AOIS responder
- v20.1 per-incident and per-step cost accounting
- v20.2 budget-aware model and tool routing
- v21 MCP, tool registry, tool governance, trust controls, remote tool trust model
- v22 durable workflows with Temporal
- v23 LangGraph or equivalent orchestration loop
- v23.5 agent eval pipeline and production scoring
- v23.8 runtime operations, canary, rollback, autonomy control, kill switch
- v24 multi-agent collaboration and delegation, A2A-aware design, agent federation concepts
- v25 safe execution sandbox and capability boundaries

AOIS after Phase 7:

- real agent runtime
- governed tool use
- workflow durability
- evaluation and runtime controls

### Phase 8 - Product Surface

Purpose:
Expose AOIS as a product that humans can understand and use.

Versions:

- v26 React dashboard, live incident and trace views
- v27 auth, tenancy, permissions, policy-aware user access

### Phase 9 - Delivery and Platform

Purpose:
Make AOIS easy to ship, roll out, and reuse.

Versions:

- v28 CI/CD, rollout logic, signatures, release safety
- v29 experiment and model delivery tracking
- v30 internal platform patterns, self-service infrastructure, platform APIs

### Phase 10 - Frontier Layer

Purpose:
Push AOIS into the frontier without losing rigor.

Versions:

- v31 multimodal inputs and analysis
- v32 edge and offline inference patterns
- v33 AI red teaming, adversarial testing, misuse simulation
- v34 governance verification, computer-use workflows, compliance controls

## Labs In Every Version

Every version must contain these labs.

### 1. Build Lab

Add the new capability.

### 2. Ops Lab

Inspect the capability from the terminal:

- process
- port
- logs
- request
- file
- config

### 3. Break Lab

Create one real failure and diagnose it.

### 4. Defense Lab

Explain why this design was chosen over alternatives.

### 5. Explanation Lab

Explain:

- the tool at four layers
- the system at four levels

### 6. Benchmark Lab

Measure one relevant thing:

- latency
- throughput
- memory
- token cost
- image size
- query time
- startup time

## Mastery Artifacts Per Version

Each version must leave behind:

- `03-notes.md`
- `04-lab.md`
- `05-runbook.md`
- `06-failure-story.md`
- `07-benchmark.md`

These documents make your understanding inspectable.

## Frontier Direction Guarantee

You asked for a curriculum that points toward where AI is going.

This one does.

It includes:

- structured AI systems, not free-form demos
- evaluation, not blind trust
- observability, not black-box usage
- policy and governance, not raw autonomy
- agentic workflows, not chatbot theatrics
- tool protocols and tool governance
- runtime control and cost control
- inference engineering and GPU literacy
- cloud and cluster deployment
- red teaming and safety

It also explicitly includes:

- Groq-style low-latency inference routing
- prompt caching and token-economics thinking
- Redis and caching as cost and latency controls
- RAG and memory system design
- workload identity and capability boundaries
- managed-cloud and self-managed deployment comparison
- GPU operations beyond just calling hosted models

That is the direction of serious AI systems.

## Final Standard

By the end of this program you should be able to do all of the following without bluffing:

- build AOIS from local service to production platform
- explain every major tool at four layers
- explain AOIS itself at four levels
- diagnose failures from request to model to infra
- justify architectural choices with tradeoffs
- discuss agentic systems with runtime, policy, and cost realism

That is the bar for the curriculum.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](READING-ORDER.md)
- Previous: [AOIS Full Program Map](FULL-PROGRAM-MAP.md)
- Next: [AOIS Learning Operating Model](LEARNING-OPERATING-MODEL.md)
<!-- AOIS-NAV-END -->
