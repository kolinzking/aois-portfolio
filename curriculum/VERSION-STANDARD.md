# AOIS Version Standard

This document defines the teaching and artifact standard for every AOIS version.

If a version does not satisfy this document, it is not complete.

## Content Quality Rule

This standard is designed to produce mastery, not note-taking.

That means:

- practical-first, not theory-first
- expected behavior shown whenever ambiguity would hurt a self-learner
- deliberate failure exposure, not success-only walkthroughs
- production habits from the beginning
- explicit forward links so knowledge compounds

If a section reads like a vendor README or a Wikipedia summary, it is not done.

## Required Files Per Version

Each version should eventually include:

```text
curriculum/phaseX/vY/
├── notes.md
├── lab.md
├── runbook.md
├── benchmark.md
└── failure-story.md
```

## Required Sections In `notes.md`

```text
# vX - Title
Estimated time: X-Y hours

## What This Builds
## Why This Exists
## AOIS Connection
## Learning Goals
## Prerequisites
## Core Concepts
## Build
## Ops Lab
## Break Lab
## Testing
## Common Mistakes
## Troubleshooting
## Benchmark
## Architecture Defense
## 4-Layer Tool Drill
## 4-Level System Explanation Drill
## Failure Story
## Mastery Checkpoint
## Connection Forward
```

## Mandatory Labs

Every version must include:

### Build Lab

Add the new capability.

### Ops Lab

Inspect the system using real commands, logs, metrics, traces, or cluster tools.

### Break Lab

Cause or inspect at least one failure mode.

### Explanation Lab

Answer:

- the 4-layer tool rule
- the 4-level system explanation rule

Also answer:

- why this tool is in AOIS at all
- what simpler alternative existed
- why that alternative eventually stops being enough

### Defense Lab

Explain:

- why this tool
- what alternatives existed
- why they were not chosen here

### Benchmark Lab

Measure at least one relevant thing.

Examples:

- latency
- token usage
- memory use
- image size
- startup time
- throughput
- queue lag
- GPU utilization

## The 4-Layer Tool Rule

For every major tool or subsystem, answer:

1. Plain English
What problem does this solve?

2. System Role
Where does it sit in AOIS?

3. Minimal Technical Definition
What is it technically?

4. Hands-on Proof
What changes when it is removed, broken, or misconfigured?

## The 4-Level System Explanation Rule

For AOIS and major subsystems, explain at these levels:

1. Simple English
2. Practical explanation
3. Technical explanation
4. Engineer-level explanation

## Benchmark Standard

Benchmarks do not need to be elaborate.
They do need to be real.

Each version should record:

- what was measured
- how it was measured
- what the result means
- what tradeoff was observed

## Failure Story Standard

Every version must record:

- symptom
- root cause
- fix
- prevention
- what this taught me

Conceptual misreadings count as failures if they could lead to bad engineering decisions.

## Delivery Rules

Every strong version should:

- show the problem before the abstraction
- force at least one realistic error or failure mode
- keep explanations in plain English before technical language
- connect the current build to later AOIS layers
- keep tool count low enough that the learner can still reason clearly

Frontier coverage is required.
Frontier sprawl is forbidden.

## Self-Learner Rule

The learner must be able to complete the version from the repo materials alone.

That means:

- prerequisites are explicit
- commands are runnable
- likely errors are named
- the success state is visible
- the mastery checkpoint is concrete

## Mastery Checkpoint Standard

A version is complete only if the learner can:

1. reproduce it
2. explain it
3. debug it
4. defend it
5. extend it

## Cross-Version Continuity Questions

Every version should answer these at the end:

- What new capability was added to AOIS?
- What earlier versions does this depend on?
- What later versions will depend on this?
- What new failure mode entered the system because of this version?
- What new visibility or control did this version create?

## Teaching Sequence Rule

The proper sequence is:

`why -> build -> inspect -> break -> measure -> explain -> defend -> record`

If a version skips most of that sequence, it may inform but it will not produce mastery.
