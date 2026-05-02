# AOIS Learning Operating Model

This document defines how the curriculum is taught and how mastery is measured.

## Core Principle

Reading is support.
Building is the method.
Operating is the proof.
Explaining is the mastery signal.

The learner may start from near-zero.
So the curriculum must teach as if clarity is a hard engineering requirement, not a stylistic preference.

## Session Flow

Every guided session follows this order:

1. Reopen the current version notes
2. Run the prerequisite checks
3. Build one section
4. Inspect behavior from the terminal
5. Trigger or inspect at least one failure case
6. Answer the explanation drills
7. Record benchmark and failure notes
8. Commit the completed milestone

## The 4-Layer Tool Drill

For every new tool, answer these exactly.

1. Plain English
What problem does this solve?

2. System Role
Where does it sit in AOIS?

3. Minimal Technical Definition
What is it technically?

4. Hands-on Proof
What happens if it is removed or broken?

These questions appear in every version checkpoint.

## The 4-Level System Explanation Drill

For AOIS and every major subsystem, answer at these levels:

1. Simple English
2. Practical explanation
3. Technical explanation
4. Engineer-level explanation

This trains you to speak to:

- non-technical people
- operators
- engineers
- architects

## Every Version Must Produce

- code that runs
- notes that explain
- commands that verify
- one benchmark
- one failure story
- one architecture defense
- one mastery checkpoint
- one self-paced path that works without live guidance

## Every Version Must Include

### Build Lab

Implement the capability.

### Ops Lab

Inspect it with real commands.

### Break Lab

Misconfigure, remove, overload, or break something on purpose.

### Explanation Lab

Answer the 4-layer tool drill and 4-level system drill.

### Defense Lab

Answer:

- why this tool
- what alternatives existed
- why they were not chosen here

## The Three Forms of Depth

Every lesson must deliver:

### Conceptual depth

You understand the underlying model.

### Operational depth

You know what to run, inspect, and change.

### Judgment depth

You understand tradeoffs, failure modes, and limits.

If any one is missing, the lesson is too shallow.

## The Three Forms Of Independence

Every strong lesson should also reduce dependence on the live teacher.

It should create:

### Directional independence

The learner knows what to do next.

### Interpretive independence

The learner can understand what happened without waiting for explanation.

### Recovery independence

The learner can recover from confusion, interruption, or common failure without being stranded.

## Mastery Checkpoint Standard

A version is complete only if you can:

1. Reproduce it
2. Explain it
3. Debug it
4. Defend it
5. Extend it

Working once is not completion.

## Repetition By Osmosis

The course deliberately forces repeated use of:

- terminal commands
- git workflow
- Python services
- JSON APIs
- logs
- traces
- benchmarks
- runbooks
- architecture explanation

That repetition is not filler.
It is how fluency becomes normal.

## Repo Artifact Standard

Each version should eventually live under:

`curriculum/phaseX/vY/`

With these artifacts:

- `notes.md`
- `lab.md`
- `runbook.md`
- `benchmark.md`
- `failure-story.md`

This is how the repo becomes:

- a learning record
- an engineering artifact
- a portfolio
- a proof-of-mastery system

## Teaching Standard

Each teaching step must follow this sequence:

`why -> command -> output -> diagnosis -> explanation -> extension`

This prevents two common failures:

- shallow command-following without understanding
- abstract explanation without operational proof

## Frontier-With-Foundation Rule

The program exists to take the learner to the forefront of AI infrastructure.

That does not permit skipping fundamentals.
It requires stronger fundamentals.

So every frontier topic must be taught in a way that remains:

- beginner-legible at entry
- operationally grounded during practice
- frontier-relevant in the final explanation

## Future Direction Requirement

The curriculum must track where AI systems are going:

- structured outputs
- model routing
- evaluation
- observability
- policy and governance
- agentic workflows
- tool protocols
- runtime control
- cost-aware execution
- inference operations

If a lesson does not connect to that trajectory, it should not stay in the program.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](READING-ORDER.md)
- Previous: [AOIS Master Curriculum](MASTER-CURRICULUM.md)
- Next: [AOIS Study Pacing](STUDY-PACING.md)
<!-- AOIS-NAV-END -->
