# AOIS Syllabus

This is the navigable syllabus for the AOIS program.

Use it to understand:

- what each phase is for
- which tools appear
- what AOIS becomes at that stage
- what mastery is expected before moving on

## Phase 0 - Foundations That Actually Carry Forward

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

Mastery target:
You can inspect the machine, reason about requests, build a typed service, make a raw LLM call, and explain each component at four layers.

## Phase 1 - Intelligence Core

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

Mastery target:
You can explain why structured AI systems beat ad hoc prompting and you can defend routing, validation, and traceability decisions.

## Phase 2 - Container and Security Base

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

Mastery target:
You can explain what becomes safer, faster, or more reproducible because of containerization and security controls.

## Phase 3 - Cluster and GitOps Operations

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

Mastery target:
You can describe how AOIS gets from code to cluster and what controls service identity, rollout, and scaling.

## Phase 4 - Enterprise Cloud

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

Mastery target:
You can compare self-managed and cloud-managed AI infrastructure realistically.

## Phase 5 - Inference and GPU Systems

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

Mastery target:
You can explain throughput, latency, memory tradeoffs, and how GPU infra affects model serving.

## Phase 6 - Observability and Reliability

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

Mastery target:
You can investigate incidents with evidence instead of guesses.

## Phase 7 - Agentic AOIS

Goal:
Build in the actual direction of modern AI systems: tools, workflows, agents, governance, runtime control.

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

Mastery target:
You can explain agent systems beyond demos: tool trust, failure modes, workflow durability, evaluation, runtime safety, and cost.

## Phase 8 - Product and Interface

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

Mastery target:
You can show the system, not just describe it.

## Phase 9 - Delivery and Platform

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

Mastery target:
You can move from one-off engineering to operational software delivery.

## Phase 10 - Frontier Layer

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

Mastery target:
You can discuss frontier AI systems with operational credibility, not hype.

## Cross-Cutting Expectations

These apply in every phase.

- You answer the 4-layer tool drill for every major tool.
- You answer the 4-level system explanation drill for AOIS and major subsystems.
- You run build, ops, break, defense, and benchmark labs.
- You commit every completed version.
- You record one real failure story per version.

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
