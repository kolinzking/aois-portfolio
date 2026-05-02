# AOIS Repository Blueprint

This is the target repository shape for the full curriculum.

The directory structure should grow with the system.
Do not create empty theater.

## Target Layout

```text
aois-portfolio/
├── app/
│   ├── api/
│   ├── ai/
│   ├── agents/
│   ├── cache/
│   ├── domain/
│   ├── retrieval/
│   ├── services/
│   ├── storage/
│   └── main.py
├── scripts/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evals/
├── curriculum/
│   ├── 00-phase0/
│   ├── 01-phase1/
│   ├── 02-phase2/
│   ├── 03-phase3/
│   ├── 04-phase4/
│   ├── 05-phase5/
│   ├── 06-phase6/
│   ├── 07-phase7/
│   ├── 08-phase8/
│   ├── 09-phase9/
│   ├── 10-phase10/
│   ├── MASTER-CURRICULUM.md
│   ├── LEARNING-OPERATING-MODEL.md
│   └── REPO-BLUEPRINT.md
├── runbooks/
├── infra/
│   ├── docker/
│   ├── helm/
│   ├── terraform/
│   ├── argocd/
│   └── kubernetes/
├── observability/
│   ├── otel/
│   ├── prometheus/
│   ├── grafana/
│   └── loki/
├── dashboards/
├── docs/
├── .env.example
└── README.md
```

## Curriculum Version Pattern

Each version should use:

```text
curriculum/NN-phaseX/vY/
├── 00-start-here.md
├── 01-contents.md
├── 02-introduction.md
├── 03-notes.md
├── 04-lab.md
├── 05-runbook.md
├── 06-failure-story.md
├── 07-benchmark.md
├── 08-summary-notes.md
├── 09-looking-forward.md
└── 10-next-version-bridge.md
```

## Why This Blueprint Matters

It forces the repo to act as:

- product codebase
- lab notebook
- runbook archive
- benchmark record
- proof of progression

## Growth Order

Recommended order:

1. `scripts/`
2. `curriculum/00-phase0/`
3. `app/`
4. `tests/`
5. `runbooks/`
6. `infra/docker/`
7. `infra/kubernetes/`
8. `infra/helm/`
9. `infra/terraform/`
10. `observability/`
11. `dashboards/`

## Reuse Principle

The same components should keep being touched as the curriculum grows.

Examples:

- `scripts/` starts with local inspection and later supports deployments and incident checks
- `app/` starts with API basics and later contains routing, policies, retrieval, and agents
- `app/cache/` and `app/retrieval/` prevent caching and RAG from being afterthoughts
- `tests/` starts simple and later holds eval suites and regression gates
- `runbooks/` turns failures into operational memory
- `infra/kubernetes/` keeps k8s operational work visible as a backbone domain
- `infra/` turns delivery into a normal engineering activity instead of a final topic

That reuse is part of the learning design.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](READING-ORDER.md)
- Previous: [AOIS Source Currency](SOURCE-CURRENCY.md)
- Next: [AOIS Continuity Protocol](CONTINUITY.md)
<!-- AOIS-NAV-END -->
