
# AOIS — AI Operations Intelligence System

A personal reference implementation exploring how to run AI/LLM systems **reliably** in
production-style environments: a containerized incident-analysis service with
provider-neutral model routing, structured-output contracts, and SRE reliability/security
patterns — packaged for Kubernetes with Helm and delivered via GitOps.

> Personal portfolio project by **Collins Igbokwe** — built to design and demonstrate
> production-grade AIOps and cloud-native SRE patterns end to end.

---

## What it does

AOIS takes an infrastructure incident message and returns a **structured analysis**
(category, severity, confidence, suggested action). The interesting part isn't the model —
it's the **engineering around** the model: the routing, validation, security, and
reliability layers an LLM service needs *before* any provider is plugged in. The core is
deterministic and provider-neutral by design, so the behaviour is testable and the
external providers integrate behind a stable contract.

## Architecture

```
                 ┌───────────────────────────────────────────────┐
   incident      │  FastAPI service  (app/)                       │
   message  ───▶ │   security      input inspection / guardrails  │
                 │   analysis      incident classification        │
                 │   ai_contract   structured-output contract     │
                 │   model_router  provider-neutral routing call  │
                 │   reliability   trace ids + eval baseline      │
                 └─────────────────────┬─────────────────────────┘
                                       ▼
              structured result:  category · severity · confidence
```

**Delivery path:** container (`Dockerfile` / `compose.yaml`) → Kubernetes
(`k8s/aois/` raw manifests) → Helm chart (`charts/aois/`, incl. NetworkPolicy,
ResourceQuota, ServiceAccount) → GitOps with Argo CD (`gitops/argocd/`).

## Tech stack

| Layer | Tools |
|-------|-------|
| Service | Python · FastAPI · Pydantic |
| Packaging | Docker · Docker Compose |
| Orchestration | Kubernetes · Helm |
| Delivery | Argo CD (GitOps) |
| Data | SQL schema |

## Repository layout

| Path | What's there |
|------|--------------|
| `app/` | FastAPI service — `analysis`, `model_router`, `ai_contract`, `security`, `reliability`, `models`, `config` |
| `examples/` | Runnable demos plus a library of pattern simulations (observability, autoscaling, agentic workflows, AI governance, chaos, cost accounting, …) |
| `charts/aois/` | Helm chart — deployment, service, namespace, network-policy, resource-quota, service-account |
| `k8s/aois/` | Raw Kubernetes manifests |
| `gitops/argocd/` | Argo CD Application for GitOps delivery |
| `sql/` | Database schema |
| `scripts/` | Utility scripts (`sysinfo`, `log_analyzer`, `http_probe`) |

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload      # POST an incident to /analyze
```

No server needed to try the analyzer:

```bash
python examples/analyze_incident.py "payment-service OOMKilled, restart loop, exit 137"
```

## Deploy to Kubernetes

```bash
helm install aois charts/aois            # Helm
# or, GitOps:
kubectl apply -f gitops/argocd/aois-application.yaml
```

## Scope & status

This is a **personal reference project**, not a managed production service. The analysis
core is deterministic and provider-neutral *by design*; external LLM providers integrate
behind the routing layer. The `examples/simulate_*` scripts model the broader patterns
(agents, event streaming, governance, chaos engineering, cost accounting) the architecture
is built to support. See [ARCHITECTURE.md](ARCHITECTURE.md) for the component breakdown.

## License

[MIT](LICENSE) © 2026 Collins Igbokwe
