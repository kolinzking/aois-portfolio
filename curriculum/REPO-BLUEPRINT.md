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
│   ├── domain/
│   ├── services/
│   ├── storage/
│   └── main.py
├── scripts/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evals/
├── curriculum/
│   ├── phase0/
│   ├── phase1/
│   ├── phase2/
│   ├── phase3/
│   ├── phase4/
│   ├── phase5/
│   ├── phase6/
│   ├── phase7/
│   ├── phase8/
│   ├── phase9/
│   ├── phase10/
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
curriculum/phaseX/vY/
├── notes.md
├── lab.md
├── runbook.md
├── benchmark.md
└── failure-story.md
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
2. `curriculum/phase0/`
3. `app/`
4. `tests/`
5. `runbooks/`
6. `infra/docker/`
7. `infra/helm/`
8. `infra/terraform/`
9. `observability/`
10. `dashboards/`

## Reuse Principle

The same components should keep being touched as the curriculum grows.

Examples:

- `scripts/` starts with local inspection and later supports deployments and incident checks
- `app/` starts with API basics and later contains routing, policies, retrieval, and agents
- `tests/` starts simple and later holds eval suites and regression gates
- `runbooks/` turns failures into operational memory
- `infra/` turns delivery into a normal engineering activity instead of a final topic

That reuse is part of the learning design.
