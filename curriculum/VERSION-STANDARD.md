# AOIS Version Standard

This document defines the teaching and artifact standard for every AOIS version.

If a version does not satisfy this document, it is not complete.

## Version Status Labels

Use these labels consistently in lesson files and `CORPUS-STATUS.md`.

- `scaffolded`: file structure exists, but the lesson cannot teach the topic yet
- `partial`: real content exists, but one or more required labs, answer keys, artifacts, or gates are missing
- `authored`: the version can be completed self-paced from repo materials alone
- `reviewed`: the version has passed a full quality review and command validation pass
- `taught`: the version has been used in a real learning session and improved from observed failure points

Do not mark a version `authored` unless the build, ops, break, benchmark, explanation, defense, and recovery path are all present.

## Quality Gate

Every authored version must pass this gate before it is treated as complete.

| Gate | Requirement |
|---|---|
| Build | The learner creates or modifies a real artifact, or performs a deliberate direct-operations exercise when the version is pre-automation. |
| Operate | The learner inspects behavior through real commands, logs, metrics, traces, requests, database queries, or cluster tooling. |
| Break | The learner triggers or studies a real failure mode and records symptom, cause, fix, and false conclusion prevented. |
| Measure | The learner records at least one concrete benchmark or timed/scored capability check. |
| Explain | The learner answers the 4-layer tool drill and 4-level system explanation drill. |
| Defend | The learner explains why this design/tool is used here and what simpler or stronger alternatives exist. |
| Extend | The learner completes one small extension or can describe exactly what extension comes next. |

The minimum pass threshold is all seven gates.
If a gate is intentionally deferred, the lesson must say why and where that gate is satisfied later.

## Content Quality Rule

This standard is designed to produce mastery, not note-taking.

That means:

- practical-first, not theory-first
- expected behavior shown whenever ambiguity would hurt a self-learner
- deliberate failure exposure, not success-only walkthroughs
- production habits from the beginning
- explicit forward links so knowledge compounds

If a section reads like a vendor README or a Wikipedia summary, it is not done.

## Competitive Standard

Every AOIS version must be good enough to stand beside the best self-taught technical material available anywhere.

That means each version should compete with:

- the best operator handbooks
- the best practical engineering courses
- the best “learn by building” curricula
- the clearest official documentation

If AOIS is weaker than those on clarity, practice quality, expected outputs, conceptual precision, or self-learner usability, it is not done.

## Self-Contained Mastery Rule

Every version must be complete enough that a serious learner can make real progress without live Codex presence.

That means the lesson pack must be:

- self-contained
- self-paced
- self-descriptive
- self-directional
- self-correcting where possible

The learner should not need outside explanation to understand:

- what is being built
- why it matters
- what commands to run
- what outputs to expect
- what errors are likely
- how to know whether progress is real

## Basic-To-Frontier Progression Rule

AOIS is designed to take a learner from weak starting point to frontier AI infrastructure mastery.

So every version must satisfy both:

- beginner legibility
- forward-facing engineering relevance

This means:

- plain English comes before dense jargon
- fundamentals are taught before abstractions built on them
- theory exists to clarify practice, not replace it
- every concept should prepare the learner for later frontier systems work

The curriculum is not allowed to assume competence that has not yet been built.

## Source Currency Rule

Frontier and fast-moving topics must be checked against official or primary sources during authoring.

This applies especially to:

- OpenAI API behavior and model guidance
- Kubernetes behavior and production primitives
- OpenTelemetry concepts and signal semantics
- vLLM, NVIDIA GPU Operator, NVIDIA NIM, and Triton behavior
- MCP specification and tool/resource/prompt semantics
- Temporal, LangGraph, and durable agent workflow behavior
- cloud provider services, IAM, managed AI services, and security controls

Each frontier-facing version must include a short source note naming the official docs or primary references used during the most recent authoring pass.
Do not freeze fast-moving claims in the curriculum without either a dated source note or a clear statement that the material is conceptual and version-independent.

## Required Files Per Version

Each version should eventually include:

```text
curriculum/phaseX/vY/
├── CONTENTS.md
├── introduction.md
├── notes.md
├── lab.md
├── runbook.md
├── benchmark.md
├── failure-story.md
├── summarynotes.md
├── next-version-bridge.md
└── looking-forward.md
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
## Mastery Checkpoint Answer Key
## Connection Forward
## Source Notes
```

## Mandatory Labs

Every version must include:

### Build Lab

Add the new capability.

### Ops Lab

Inspect the system using real commands, logs, metrics, traces, or cluster tools.

Every ops lab should include:

- runnable commands
- expected output or expected behavior
- answer key for the main questions
- explanation of why the observed output matters

### Break Lab

Cause or inspect at least one failure mode.

Every break lab should include:

- the intended failure
- the expected symptom
- the fix
- the lesson the failure is meant to teach
- the exact false conclusion the learner might have made without this break

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

The benchmark file should be authored by default.
The learner may add notes, but should not be forced to generate the first useful benchmark interpretation from scratch.

Benchmarks must not exist as ritual.
They must answer:

- what is getting better or worse
- what tradeoff changed
- what future decision this measurement will influence

## Failure Story Standard

Every version must record:

- symptom
- root cause
- fix
- prevention
- what this taught me

Conceptual misreadings count as failures if they could lead to bad engineering decisions.

The failure-story file should also be authored by default.
It should contain at least one representative failure analysis even before the learner adds a personal one.

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
- key questions have answers available somewhere in the lesson pack
- the learner is not blocked by Codex absence or network issues

If a lesson silently relies on live chat explanation to become understandable, it fails this rule.

## Self-Paced Support Rule

Every strong version should support both:

- live guided mode
- self-paced mode

That means the lesson pack must include:

- expected outputs
- answer keys for the main questions
- authored benchmark interpretation
- authored failure-story interpretation
- concise summary notes
- a version-level contents/navigation file
- a version-level introduction file
- a bridge file connecting the current version to the next one
- a version-level looking-forward file
- enough explanation for the learner to recover after interruption

## Explanation Depth Rule

Every strong version must include all three forms of depth:

- conceptual depth
- operational depth
- judgment depth

Conceptual depth means the learner understands the model behind the commands.
Operational depth means the learner knows what to run, inspect, and change.
Judgment depth means the learner knows when the tool is right, when it is wrong, and what tradeoffs it introduces.

If one of these is missing, the lesson is incomplete.

## Mastery Checkpoint Standard

A version is complete only if the learner can:

1. reproduce it
2. explain it
3. debug it
4. defend it
5. extend it

The mastery checkpoint must test:

- reproduction
- explanation
- diagnosis
- tradeoff reasoning
- forward connection to later AOIS phases

Every mastery checkpoint must include an answer key or answer path in the same lesson pack.

The answer key should:

- appear after the learner-facing questions
- be clear enough for self-paced verification
- avoid vague "answers may vary" unless the expected reasoning is still described
- distinguish correct reasoning from weak or incomplete reasoning
- support Codex live teaching without making Codex required for basic verification

## Codex Live Teacher Standard

Every authored version should support two operating modes:

- self-paced mode, where the learner can complete the lesson from files alone
- Codex live teacher mode, where Codex actively teaches, demonstrates, reviews, debugs, quizzes, and extends the lesson

Codex live teacher mode must not weaken the written curriculum.
The files must still be complete enough for independent study.

When Codex is present, however, it should not be relegated to a passive guide.
It should teach like a live instructor:

- introduce the concept
- explain why it matters
- walk through examples
- ask the learner to run commands
- interpret outputs with the learner
- diagnose mistakes
- quiz for mastery
- push for stronger explanations

Each phase should eventually include suggested Codex prompts for:

- prerequisite check
- live lesson walkthrough
- stuck-state diagnosis
- architecture defense review
- benchmark interpretation
- mastery checkpoint quiz
- extension challenge

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

## Rebuild Standard

During the rebuild, every authored version must be written as if it may become the learner's only reliable source for that topic.

That means:

- no shallow placeholders masquerading as instruction
- no “see docs” escapes unless the exact external reference is narrowly scoped
- no theory dumping without operational proof
- no basic concept skipped just because it feels obvious to the writer
