# Phase 0 Capstone - Local AOIS Foundation

This capstone is the Phase 0 gate.

Do not treat Phase 0 as complete until the learner can pass this without live rescue.

## Goal

Prove that the learner can operate a local machine, automate basic inspection, preserve engineering history, inspect service boundaries, write typed Python, expose a clean API, plan an LLM request without a provider call, and design persistent incident storage.

## Required Evidence

By the end of Phase 0, the repo should contain:

- Linux inspection notes from `v0.1`
- `scripts/sysinfo.sh`
- `scripts/log_analyzer.sh`
- meaningful Git history
- HTTP inspection notes or scripts
- typed Python AOIS logic
- a FastAPI service boundary
- a provider-neutral LLM request dry-run example
- a Postgres-oriented `aois_p` schema and validator

## Capstone Scenario

You receive this incident signal:

```text
gateway returned 5xx after deploy; pod restarted; database latency increased
```

You must show how Phase 0 tools help you inspect it before any advanced AI platform exists.

## Tasks

1. Inspect the local machine with Linux commands.
2. Run the Bash scripts and explain what they can and cannot know.
3. Classify the incident with the rule-based analyzer.
4. Explain why rule-based classification is brittle.
5. Show how the future API will receive this signal.
6. Build a dry-run LLM request plan and estimate output budget.
7. Show how the future database schema will store the incident, analysis, and request plan.
8. Explain why Phase 1 needs AI structured output rather than only shell rules.

## Evidence Commands

Run only resource-safe commands unless a runtime step has been approved:

```bash
./scripts/sysinfo.sh
./scripts/log_analyzer.sh "gateway returned 5xx after deploy"
python3 examples/analyze_incident.py gateway returned 5xx after deploy
python3 examples/raw_llm_request.py gateway returned 5xx after deploy
python3 examples/validate_schema.py
```

If the FastAPI server is used for evidence, it must be short-lived, bound to `127.0.0.1`, and stopped immediately after validation.

## Self-Grading Questions

Do not treat the capstone as passed until you can answer:

1. Which Phase 0 tool inspects the machine?
2. Which Phase 0 tool classifies known log messages?
3. Which Phase 0 artifact preserves engineering history?
4. Which Phase 0 artifact exposes the analysis boundary over HTTP?
5. Which Phase 0 artifact plans a model request without calling a provider?
6. Which Phase 0 artifact designs persistence under the `aois_p` namespace?
7. Where does the deterministic analyzer fail?
8. Why is structured AI output still needed later?
9. Why is database runtime not started by default?
10. Why is `aois_p` used for server-visible portfolio objects?

## Self-Grading Answer Key

1. `v0.1` commands and `scripts/sysinfo.sh`.
2. `scripts/log_analyzer.sh` and the Python analyzer.
3. Git commits from `v0.3`.
4. The FastAPI app from `v0.6`.
5. `examples/raw_llm_request.py` from `v0.7`.
6. `sql/aois_schema.sql` from `v0.8`.
7. It only handles known patterns and cannot reason deeply about novel incidents.
8. Later AOIS needs richer reasoning with parseable fields, confidence, and auditable boundaries.
9. The shared server has strict resource limits and the primary AOIS project takes priority.
10. It separates portfolio-owned server-visible database objects from the primary AOIS project.

## Pass Standard

The learner passes if they can:

- reproduce the local commands and scripts
- explain each artifact at four layers
- identify at least two false conclusions the early tools could cause
- describe the Phase 1 capability gap clearly
- defend the order of Phase 0 without saying "because the curriculum says so"
- confirm no external provider call, database server, or persistent runtime is used without approval
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../READING-ORDER.md)
- Previous: [v0.8 Next Version Bridge](v0.8/next-version-bridge.md)
- Next: [Phase 0 Looking Forward](looking-forward.md)
<!-- AOIS-NAV-END -->
