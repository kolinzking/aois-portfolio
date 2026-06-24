# Architecture

AOIS is structured so the **operational engineering** around an LLM is explicit and
testable, independent of any specific model provider.

## Request flow

1. **Security inspection** (`app/security.py`) — inspect the incoming incident text before
   anything else acts on it (input guardrails).
2. **Analysis** (`app/analysis.py`) — classify the incident into a category and severity.
   Deterministic by default so behaviour is reproducible and unit-testable.
3. **Structured-output contract** (`app/ai_contract.py`) — enforce a typed response shape
   (`app/models.py`, Pydantic), so callers always receive a valid, predictable object.
4. **Model routing** (`app/model_router.py`) — choose a route under operational constraints
   (severity, latency budget, cost ceiling, provider approval). Provider-neutral: the
   decision is made independently of which provider is wired in.
5. **Reliability** (`app/reliability.py`) — issue a trace id per request and run an
   evaluation baseline so quality can be measured rather than assumed.

The HTTP surface lives in `app/main.py` (FastAPI), with configuration in `app/config.py`.

## Delivery

| Stage | Where |
|-------|-------|
| Container image | `Dockerfile`, `compose.yaml` |
| Raw Kubernetes manifests | `k8s/aois/` |
| Helm chart (NetworkPolicy, ResourceQuota, ServiceAccount) | `charts/aois/` |
| GitOps delivery (Argo CD Application) | `gitops/argocd/` |
| Database schema | `sql/` |

## Pattern library

`examples/` holds runnable demos (`analyze_incident.py`, `run_eval_baseline.py`,
`security_inspect.py`, `raw_llm_request.py`) and a set of `simulate_*` scripts that model
the broader patterns the architecture is designed to support — observability and SLOs,
autoscaling, agentic and multi-agent workflows, durable orchestration, event streaming,
AI-failure governance, chaos game-days, and per-step cost accounting.

## Design choices

- **Deterministic core, providers at the edge** — keeps the system testable and makes
  provider integration a contained change behind the routing layer.
- **Constraint-driven routing** — routing is a function of severity, latency budget, cost
  ceiling, and explicit provider approval, not a hard-coded model choice.
- **Security and reliability are first-class** — input inspection and trace/eval baselines
  are part of the request path, not afterthoughts.
