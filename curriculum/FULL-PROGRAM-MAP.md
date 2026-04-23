# AOIS Full Program Map

This document locks the full AOIS institution.

It defines the complete build path from `v0.1` to `v34`.
Every version exists to extend one continuous system.

The system is AOIS:

AI Operations Intelligence System

The final outcome is not "course completion."
The final outcome is operational mastery across AI systems, agentic systems, infrastructure, observability, deployment, governance, and explanation.

## System Spine

AOIS evolves through this spine:

`signal -> ingest -> store -> retrieve -> analyze -> decide -> act -> observe -> evaluate -> govern -> improve`

Different versions strengthen different parts of this spine.

## Program Threads That Never Stop

These threads must appear repeatedly across the full program:

- shell and Linux fluency
- service/process management fluency
- git and engineering history
- HTTP and service boundaries
- typed Python backend work
- persistence and data lifecycle reasoning
- AI model behavior and structured outputs
- testing and evaluation
- logs, metrics, traces, and debugging
- benchmarking and cost awareness
- caching and data lifecycle awareness
- security and trust boundaries
- architecture explanation and tradeoff defense
- agentic workflows and runtime control

## Phase 0 - Foundations That Carry Forward

Purpose:
Build the engineering substrate for everything that follows.

### v0.1 - Linux Essentials And Machine Inspection

Build:
`scripts/sysinfo.sh`

Core concepts:

- filesystem navigation
- permissions
- process awareness
- CPU
- memory
- disk
- Linux inspection
- shell safety
- process and service awareness

AOIS role:
First local health signal.

Labs:

- build a system health script
- inspect raw commands behind the script
- break permissions or paths
- explain Linux inspection and first-system signals at four levels

### v0.2 - Bash Rule-Based Log Interpretation

Build:
`scripts/log_analyzer.sh`

Core concepts:

- shell arguments
- shell branching
- arguments
- `if`/`elif`/`else`
- string matching
- brittleness of rules

AOIS role:
First interpretation layer.

Labs:

- classify simple log messages
- feed in unmatched or misleading logs
- explain why rules fail under variation
- compare raw visibility to brittle interpretation

### v0.3 - Git As Engineering Memory

Build:
A disciplined repo history for AOIS.

Core concepts:

- snapshots vs diffs
- meaningful commits
- branching
- review mindset
- repo as proof of progression

AOIS role:
Makes system evolution inspectable.

Labs:

- create version commits
- inspect history
- practice small commits
- explain why git history is part of the product

### v0.4 - Networking And HTTP

Build:
Manual API interaction drills and request tracing.

Core concepts:

- DNS
- TCP/IP
- ports
- request/response lifecycle
- headers
- methods
- `curl`

AOIS role:
Prepares for service boundaries.

Labs:

- inspect HTTP responses
- test ports and connectivity
- compare local and remote calls
- explain where HTTP sits in AOIS

### v0.5 - Python Core For Systems Work

Build:
Typed Python utilities and first AOIS backend logic.

Core concepts:

- virtual environments
- packages
- modules
- functions
- exceptions
- type hints
- Pydantic
- async basics
- configuration and env discipline

AOIS role:
Moves logic from shell-only to maintainable application code.

Labs:

- create typed Python scripts
- validate inputs
- trigger and handle exceptions
- compare shell and Python responsibilities

### v0.6 - FastAPI Without AI

Build:
A mock AOIS API.

Core concepts:

- routes
- request models
- response models
- status codes
- validation
- middleware
- service lifecycle

AOIS role:
Creates the first real service boundary.

Labs:

- run a local API
- hit endpoints with `curl`
- inspect errors and validation failures
- explain why contracts matter before AI is added

### v0.7 - LLM Fundamentals

Build:
A raw model call from AOIS.

Core concepts:

- prompts
- tokens
- cost
- latency
- prompt caching
- system vs user instructions
- structured vs unstructured outputs

AOIS role:
First model-powered reasoning step.

Labs:

- send raw prompts
- compare prompt variants
- inspect latency and token usage
- explain why free-form output is dangerous

### v0.8 - Postgres And AOIS Memory

Build:
An incident and analysis schema in Postgres.

Core concepts:

- tables
- rows
- keys
- queries
- joins
- transactions
- `EXPLAIN ANALYZE`
- pgvector foundation

AOIS role:
Persistent memory for incidents and analysis history.

Labs:

- create schema
- insert and query incidents
- inspect active queries
- explain why persistence changes the system

## Phase 1 - Intelligence Core

Purpose:
Turn AOIS into a reliable AI-backed analysis service.

### v1 - AI Analysis Endpoint

Build:
FastAPI endpoint that accepts logs and returns structured intelligence.

Core concepts:

- AI API integration
- JSON contracts
- severity modeling
- confidence scoring
- prompt design for operations
- fallback design
- provider comparison

AOIS role:
Real analysis layer.

Labs:

- send logs to AI
- inspect malformed outputs
- compare cached vs uncached system prompts
- compare rules vs model-based understanding
- explain why structured output matters

### v2 - Routing And Cost Tiers

Build:
A model routing layer.

Core concepts:

- routing policies
- fallback behavior
- cost tiers
- latency tiers
- selective model usage
- Groq fast path
- prompt caching economics
- per-request cost attribution
- Redis caching role

AOIS role:
Decision layer for model choice.

Labs:

- route different workloads to different models
- simulate model failure and fallback
- compare cost and latency
- compare Groq vs premium reasoning path
- explain why one-model-fits-all is weak design

### v3 - Reliability, Tracing, Evaluation Baseline

Build:
Validation, tracing, and eval hooks around AOIS responses.

Core concepts:

- structured validation
- tracing
- prompt iteration
- evaluation basics
- feedback loops
- Langfuse or equivalent traceability
- Instructor-style output guarantees
- retrieval readiness

AOIS role:
Makes AI behavior inspectable and testable.

Labs:

- reject malformed output
- trace a full request
- score example outputs
- explain why AI systems need observability

## Phase 2 - Containerization And Security Base

Purpose:
Make AOIS portable, repeatable, and safer.

### v4 - Docker And Local Multi-Service Runtime

Build:
Containerized AOIS service stack.

Core concepts:

- Dockerfiles
- images
- layers
- Compose
- environment injection

AOIS role:
Repeatable runtime and packaging.

Labs:

- build and run images
- compare local host vs container execution
- inspect image size and startup behavior
- explain why packaging changes engineering discipline

### v5 - Security Foundations For API And LLM Systems

Build:
Baseline security controls for AOIS.

Core concepts:

- OWASP API risks
- prompt injection
- input validation
- secret handling
- output constraints
- policy basics
- guardrails
- red-team tools

AOIS role:
Trust boundary around AI behavior and service exposure.

Labs:

- test malformed input
- test prompt injection attempts
- inspect secret handling
- run one deliberate adversarial prompt
- explain why agentic systems multiply security risk

## Phase 3 - Cluster Operations And GitOps

Purpose:
Run AOIS on real infrastructure.

### v6 - AOIS On A Real Cluster

Build:
Deploy AOIS to a low-cost Kubernetes environment.

Core concepts:

- cluster basics
- pods
- services
- ingress
- deployments
- rollout mechanics
- configmaps and secrets
- liveness and readiness probes
- requests and limits
- kubectl debugging
- scheduling basics

AOIS role:
Moves from local service to real distributed runtime.

Labs:

- deploy AOIS
- inspect pods and logs
- break and recover a deployment
- inspect service discovery and ingress flow
- debug a bad rollout with kubectl
- explain what Kubernetes is solving

### v6.5 - Identity, mTLS, And Service Trust

Build:
Workload identity and mutual trust between services.

Core concepts:

- service identity
- mTLS
- trust chains
- credential reduction

AOIS role:
Secures service-to-service communication.

Labs:

- inspect identities
- verify trust behavior
- compare static secrets to workload identity
- explain what breaks without trust boundaries

### v7 - Helm Packaging

Build:
Package AOIS as a deployable chart.

Core concepts:

- chart structure
- values
- templating
- environment-specific config

AOIS role:
Deployment packaging and reuse.

Labs:

- templatize AOIS config
- render manifests
- change deployment behavior via values
- explain why raw manifests stop scaling

### v8 - GitOps With ArgoCD

Build:
Git-driven deployment for AOIS.

Core concepts:

- desired state
- reconciliation
- sync health
- deployment discipline

AOIS role:
Makes deployment auditable and repeatable.

Labs:

- sync AOIS from git
- introduce drift and observe correction
- explain why GitOps matters operationally

### v9 - Event-Driven Scaling

Build:
Autoscaling based on workload signals.

Core concepts:

- autoscaling
- demand signals
- event-driven workloads
- scaling tradeoffs

AOIS role:
Makes resource use responsive to load.

Labs:

- generate load
- observe scaling
- inspect limits and lag
- explain the cost and stability tradeoffs of autoscaling

## Phase 4 - Enterprise Cloud

Purpose:
Understand managed cloud equivalents and enterprise patterns.

### v10 - Enterprise Model Layer

Build:
Managed-model integration.

Core concepts:

- managed AI services
- vendor integration
- security posture
- service tradeoffs
- Bedrock agent tradeoffs
- S3 and RDS role in enterprise AOIS
- CloudWatch observability path

AOIS role:
Alternative model execution path.

Labs:

- compare provider paths
- inspect policy and latency differences
- explain managed vs self-managed tradeoffs

### v11 - Event-Driven Cloud Execution

Build:
Serverless AOIS tasks.

Core concepts:

- event triggers
- function lifecycle
- cold starts
- ephemeral compute

AOIS role:
Elastic execution path for bursty work.

Labs:

- trigger functions
- observe cold starts
- compare to long-running services
- explain when serverless is or is not appropriate

### v12 - Managed Kubernetes In Cloud

Build:
AOIS on a managed Kubernetes platform.

Core concepts:

- managed control planes
- IAM integration
- IRSA-like patterns
- node lifecycle

AOIS role:
Enterprise-grade cluster operation.

Labs:

- deploy AOIS to cloud-managed cluster
- inspect identity and permissions
- compare to self-managed clusters
- explain operational differences

## Phase 5 - Inference And GPU Engineering

Purpose:
Move from model consumers to inference operators.

### v13 - GPU-Backed Inference Services

Build:
AOIS path to GPU-served inference.

Core concepts:

- GPU serving
- model hosting
- throughput
- latency
- NIM role in AOIS

AOIS role:
High-performance model execution path.

Labs:

- call GPU-backed inference
- inspect latency and throughput
- explain what changes when you leave API-only AI

### v13.5 - GPU Infrastructure Operations

Build:
GPU operator, device plugin, scheduling, observability.

Core concepts:

- GPU scheduling
- device plugins
- MIG concepts
- resource constraints
- Triton-style serving awareness

AOIS role:
Infrastructure layer for inference.

Labs:

- inspect GPU assignment
- observe scheduling behavior
- explain why GPU infra is its own discipline

### v14 - High-Throughput Inference Serving

Build:
Optimized inference server path.

Core concepts:

- batching
- concurrency
- cache behavior
- scheduling inside inference systems
- speculative decoding awareness

AOIS role:
Performance-critical model serving.

Labs:

- compare throughput modes
- inspect queueing and latency
- explain the throughput vs latency tradeoff

### v14.5 - Performance Engineering And Caching

Build:
Optimization layer for inference.

Core concepts:

- caching
- prefix reuse
- batching tradeoffs
- performance measurement
- Redis role in API/runtime caching

AOIS role:
Reduces waste and improves responsiveness.

Labs:

- benchmark optimized vs unoptimized paths
- explain what performance work is actually doing

### v15 - Fine-Tuning And Adaptation

Build:
Model adaptation path.

Core concepts:

- LoRA-style tuning
- domain adaptation
- eval before and after tuning

AOIS role:
Improved task fit for specialized work.

Labs:

- compare base vs adapted outputs
- explain why adaptation is not always the answer

### v15.5 - Quantization And Memory Economics

Build:
Reduced-footprint inference options.

Core concepts:

- quantization
- precision tradeoffs
- memory economics

AOIS role:
Makes deployment choices more realistic.

Labs:

- compare speed, memory, and output quality
- explain what is gained and lost with quantization

## Phase 6 - Observability, Streaming, Reliability

Purpose:
Make AOIS fully visible and test failure deliberately.

### v16 - Unified Telemetry

Build:
Traces, metrics, and logs for AOIS.

Core concepts:

- OpenTelemetry
- spans
- metrics
- logs correlation
- GenAI semantic conventions
- Prometheus, Loki, and Tempo roles

AOIS role:
First-class observability layer.

Labs:

- instrument requests
- trace end-to-end behavior
- explain what telemetry adds beyond logs alone

### v16.5 - Agent And Incident Tracing

Build:
Deeper traceability for multi-step behavior.

Core concepts:

- step traces
- incident traces
- correlation IDs

AOIS role:
Makes complex AI behavior inspectable.

Labs:

- trace a multi-step analysis path
- explain why single-request logs become insufficient

### v17 - Event Streaming

Build:
Streaming path for incident or telemetry events.

Core concepts:

- event streams
- producers
- consumers
- durability
- replay

AOIS role:
Asynchronous movement of signals through the system.

Labs:

- publish and consume events
- inspect lag and durability
- explain why streaming changes architecture

### v17.5 - SLOs For Services And Agents

Build:
Operational objectives for AOIS quality.

Core concepts:

- SLI
- SLO
- error budgets
- cost SLOs
- quality SLOs

AOIS role:
Makes quality measurable.

Labs:

- define targets
- measure against them
- explain why agentic systems need explicit objectives

### v18 - Deep Runtime Visibility

Build:
Kernel/runtime-level observability and security signals.

Core concepts:

- eBPF
- network visibility
- runtime events
- deep inspection

AOIS role:
Makes hidden infrastructure behavior observable.

Labs:

- inspect runtime activity
- compare app-level and kernel-level signals
- explain when deeper visibility is required

### v19 - Chaos Engineering

Build:
Controlled failure experiments.

Core concepts:

- fault injection
- recovery behavior
- resilience testing

AOIS role:
Tests whether the system survives disruption.

Labs:

- inject failure
- observe system response
- explain what resilience means operationally

### v19.5 - AI Failure Engineering And Governance

Build:
Policy and failure controls for AI behavior.

Core concepts:

- hallucination containment
- policy enforcement
- fallback design
- human review boundaries

AOIS role:
Moves from hope-based AI to controlled AI.

Labs:

- trigger failure cases
- inspect policy responses
- explain what governance changes in practice

## Phase 7 - Agentic AOIS

Purpose:
Build in the real direction of modern AI systems.

### v20 - Tool-Using Incident Responder

Build:
AOIS agent that uses tools to investigate incidents.

Core concepts:

- tool use
- step planning
- intermediate state
- incident workflows
- memory systems
- capability boundary awareness

AOIS role:
First true agentic behavior.

Labs:

- run tool-based investigations
- inspect the action sequence
- explain why this is more than chat completion

### v20.1 - Per-Incident And Per-Step Cost Accounting

Build:
Cost tracking across agent execution.

Core concepts:

- step cost
- request cost
- tool cost
- incident-level accounting
- budget explainability

AOIS role:
Makes agent execution economically visible.

Labs:

- compute cost per task
- explain why agent cost must be measured, not guessed

### v20.2 - Budget-Aware Routing

Build:
Routing decisions constrained by budget and value.

Core concepts:

- budget policies
- dynamic routing
- quality vs cost tradeoffs

AOIS role:
Economic control over autonomous behavior.

Labs:

- run the same task under different budgets
- explain how routing changes outcomes

### v21 - MCP, Tool Registry, And Tool Governance

Build:
Governed tool access layer.

Core concepts:

- MCP
- tool registry
- trust model
- allow/deny controls
- tool lifecycle
- remote MCP trust concerns

AOIS role:
Standardized and governed tool interface.

Labs:

- register tools
- control access
- inspect tool trust assumptions
- explain why unmanaged tool sprawl is dangerous

### v22 - Durable Agent Workflows

Build:
Long-running, recoverable workflows.

Core concepts:

- durability
- retries
- resumption
- workflow history

AOIS role:
Makes multi-step work reliable across time.

Labs:

- interrupt and resume workflows
- inspect recovery behavior
- explain why stateless execution is not enough

### v23 - Stateful Orchestration Loops

Build:
Graph-based or equivalent orchestration for agent decisions.

Core concepts:

- graph state
- branching
- loop control
- state transitions

AOIS role:
Decision structure for agent execution.

Labs:

- trace graph paths
- inspect loops and branch choices
- explain what orchestration adds over raw prompting

### v23.5 - Agent Evaluation Pipeline

Build:
Evaluation system for multi-step agent behavior.

Core concepts:

- unit evals
- judged outputs
- production sampling
- regression checks

AOIS role:
Makes agent quality measurable.

Labs:

- score agent behavior
- compare versions
- explain why demos are not evidence

### v23.8 - Runtime Operations And Autonomy Control

Build:
Operational control layer for agents.

Core concepts:

- canary rollout
- rollback
- kill switch
- autonomy throttling
- live controls
- runtime dashboards

AOIS role:
Production operations for agent systems.

Labs:

- reduce autonomy under bad conditions
- roll back behavior
- explain what operating an agent system actually means

### v24 - Multi-Agent Collaboration

Build:
Cooperative agent patterns.

Core concepts:

- delegation
- role separation
- handoffs
- shared state
- coordination risks
- A2A-aware design and federation concepts

AOIS role:
Distributed reasoning and work partitioning.

Labs:

- compare single-agent and multi-agent flows
- inspect coordination failures
- explain when multiple agents help or hurt

### v25 - Safe Execution Boundaries

Build:
Sandboxed execution and constrained action surfaces.

Core concepts:

- sandboxing
- capability boundaries
- action safety
- execution trust
- policy engine enforcement

AOIS role:
Turns agent action into something safer and more governable.

Labs:

- execute within boundaries
- inspect denied actions
- explain why unrestricted execution is unacceptable

## Phase 8 - Product Surface

Purpose:
Make AOIS visible and useful to humans.

### v26 - Dashboard And Real-Time Visibility

Build:
Operational UI for incidents, traces, and system state.

Core concepts:

- frontend state
- real-time updates
- visualization
- operator workflows

AOIS role:
Human control and inspection surface.

Labs:

- view incident flows
- inspect real-time updates
- explain why UI changes how a system is operated

### v27 - Auth, Tenancy, Policy-Aware Access

Build:
Identity-aware product layer.

Core concepts:

- authentication
- authorization
- tenancy
- role controls

AOIS role:
Makes AOIS usable by multiple users and teams safely.

Labs:

- test user roles
- inspect access boundaries
- explain why multi-user systems need policy-aware design

## Phase 9 - Delivery And Platform

Purpose:
Ship AOIS repeatedly and safely.

### v28 - Delivery Pipeline And Release Controls

Build:
CI/CD pipeline for AOIS.

Core concepts:

- build pipelines
- tests in delivery
- image signing
- release gates
- rollout controls
- model rollout control
- feature-flagged AI releases

AOIS role:
Turns changes into managed releases.

Labs:

- run the pipeline
- block unsafe releases
- explain what safe delivery adds to AI systems

### v29 - Experiment And Model Delivery Tracking

Build:
Track model or behavior changes over time.

Core concepts:

- experiments
- version comparison
- rollout evidence

AOIS role:
Makes AI changes traceable and defensible.

Labs:

- compare experiments
- inspect rollout decisions
- explain why model changes need delivery discipline

### v30 - Internal Platform Patterns

Build:
Reusable platform layer around AOIS.

Core concepts:

- self-service abstractions
- platform APIs
- infrastructure abstraction

AOIS role:
Turns the system into an enabling platform.

Labs:

- expose reusable platform components
- explain the difference between app engineering and platform engineering

## Phase 10 - Frontier Layer

Purpose:
Push into frontier capabilities without losing rigor.

### v31 - Multimodal AOIS

Build:
AOIS paths that reason over non-text inputs.

Core concepts:

- multimodal prompting
- cross-modal analysis
- interface changes for non-text signals

AOIS role:
Extends the types of signals AOIS can understand.

Labs:

- analyze non-text input
- inspect where the architecture changes for multimodality

### v32 - Edge And Offline Inference

Build:
AOIS deployment patterns outside centralized cloud.

Core concepts:

- edge constraints
- offline inference
- resource tradeoffs

AOIS role:
Alternative deployment model with different constraints.

Labs:

- compare central and edge paths
- explain what constraints dominate edge deployments

### v33 - Adversarial Testing And Red Teaming

Build:
A real misuse and adversarial test suite.

Core concepts:

- red teaming
- adversarial prompts
- misuse simulation
- hardening feedback loops

AOIS role:
Stress-tests trust boundaries.

Labs:

- run adversarial tests
- inspect failure patterns
- explain why AI systems require offensive testing

### v34 - Governance Verification And Computer Use

Build:
Governance-aware autonomous execution path.

Core concepts:

- auditability
- human oversight
- computer-use controls
- compliance-oriented verification

AOIS role:
The highest-trust frontier layer.

Labs:

- verify governance controls
- inspect audit trails
- explain the difference between autonomy and governed autonomy

## Program Completion Standard

You are not done when everything exists.
You are done when you can do all of these:

- explain every major tool at four layers
- explain AOIS and major subsystems at four levels
- operate the system from terminal to cluster
- diagnose failures across app, model, and infra layers
- defend architecture choices with cost, latency, risk, and reliability tradeoffs
- discuss agentic systems with runtime, safety, and governance realism

That is the completion bar for AOIS.

## Backbone Domains

These are backbone domains.
They must never be brushed past in delivery.

- Linux and process/service literacy
- HTTP and API contracts
- Python backend fundamentals
- persistence and data modeling
- model routing and output reliability
- caching and retrieval
- Kubernetes operations
- observability
- security and identity
- cost engineering
- agent runtime control
