# Phase 0 Capstone - Local AOIS Foundation

This capstone is the Phase 0 gate.

Do not treat Phase 0 as complete until the learner can pass this without live rescue.

## Goal

Prove that the learner can operate a local machine, automate basic inspection, preserve engineering history, inspect service boundaries, write typed Python, expose a clean API, make a raw model call, and persist incident data.

## Required Evidence

By the end of Phase 0, the repo should contain:

- Linux inspection notes from `v0.1`
- `scripts/sysinfo.sh`
- `scripts/log_analyzer.sh`
- meaningful Git history
- HTTP inspection notes or scripts
- typed Python AOIS logic
- a FastAPI service boundary
- a raw model-call example
- a Postgres schema and query exercises

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
6. Show how the future database schema will store it.
7. Explain why Phase 1 needs AI structured output rather than only shell rules.

## Pass Standard

The learner passes if they can:

- reproduce the local commands and scripts
- explain each artifact at four layers
- identify at least two false conclusions the early tools could cause
- describe the Phase 1 capability gap clearly
- defend the order of Phase 0 without saying "because the curriculum says so"
