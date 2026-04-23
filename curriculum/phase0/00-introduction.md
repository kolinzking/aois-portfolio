# Phase 0 - Foundations That Carry The Whole System

Phase 0 is not remedial work.
It is where you build the engineering habits that make later AI, agentic, and infrastructure work real instead of theatrical.

If Phase 0 is shallow, everything later becomes vocabulary without substance.
If Phase 0 is solid, later complexity stays legible.

## What Phase 0 Is Actually Doing

Phase 0 teaches you to see AOIS as a system before AOIS becomes large.

You are learning how to think in terms of:

- inputs
- outputs
- process state
- files
- ports
- memory
- failure modes
- contracts
- repeatability

These are not separate from AI engineering.
They are the substrate of AI engineering.

## The Purpose Of This Phase

By the end of Phase 0 you should be able to:

- inspect a Linux machine and interpret what you see
- automate small tasks in bash
- use git as an engineering record, not just a backup tool
- reason clearly about HTTP requests and responses
- build a typed Python service
- expose a working FastAPI endpoint
- make a real LLM call and understand what it is doing
- store and inspect system events in Postgres

That is the minimum floor for the rest of AOIS.

## Why This Matters For Frontier AI

Serious AI systems are not just prompts and model names.

They are:

- software systems
- networked systems
- observable systems
- costed systems
- failure-prone systems
- policy-constrained systems
- increasingly agentic systems

Phase 0 gives you the language and operational reflexes to understand those later layers.

## The AOIS Thread In Phase 0

Every version in this phase must contribute to the same system story.

The Phase 0 AOIS progression is:

`machine visibility -> log interpretation -> version discipline -> network understanding -> typed backend -> API contract -> LLM call -> persistence`

That progression is deliberate.

Later agentic AOIS depends on all of it.

## Versions In This Phase

### v0.1 - Linux and machine visibility

You inspect CPU, memory, and disk and build `scripts/sysinfo.sh`.

### v0.2 - Bash and rule-based parsing

You build a simple log analyzer and see why brittle rules do not scale.

### v0.3 - Git and engineering history

You learn how to structure commits and treat the repository as a proof artifact.

### v0.4 - Networking and HTTP

You inspect requests manually and learn what really happens across the wire.

### v0.5 - Python core

You move from shell automation into typed, structured backend logic.

### v0.6 - FastAPI without AI

You build contracts and service boundaries before adding models.

### v0.7 - LLM fundamentals

You make raw model calls and learn prompts, tokens, and structured behavior.

### v0.8 - Postgres

You add persistence so AOIS can remember incidents and analysis history.

## The Teaching Contract

This phase will not ask you only to run commands.
It will ask you to think, inspect, explain, and defend.

Every version in Phase 0 must include:

- a build lab
- an ops lab
- a break lab
- an explanation lab
- a defense lab
- a mastery checkpoint

## The 4-Layer Tool Rule Starts Here

Even in Phase 0, every important tool must be explained at four levels:

1. Plain English
2. System Role
3. Minimal Technical Definition
4. Hands-on Proof

Example:

Tool: `free`

1. Plain English
It shows how memory is being used on the machine.

2. System Role
It helps AOIS inspect machine state before later automation and diagnosis layers exist.

3. Minimal Technical Definition
It is a Linux command that reports system memory and swap usage.

4. Hands-on Proof
If you stop checking memory, you lose a major signal for diagnosing slowdowns, OOMs, and capacity pressure.

## The 4-Level System Explanation Rule Also Starts Here

You must be able to explain what you are building at multiple levels from the first version.

For example, after `v0.1`:

1. Simple English
I built a script that checks how busy and full the machine is.

2. Practical explanation
It prints CPU, memory, and disk usage so I can inspect the machine quickly.

3. Technical explanation
It is a bash script that reads Linux system signals and formats them into a small report.

4. Engineer-level explanation
It samples CPU from `/proc/stat`, reads memory from `free -h`, reads root filesystem usage from `df -h /`, and produces a repeatable local health snapshot for later troubleshooting and observability work.

## How To Use The Notes

Do not read the whole lesson and then open the terminal.

Use this loop:

1. Read one section
2. Run the commands in that section
3. Compare your output to the expected behavior
4. Stop if something does not match
5. Diagnose before moving on

## What Counts As Completion

A Phase 0 version is complete only when:

1. the build works
2. the tests behave as expected
3. you can explain the tool at four layers
4. you can explain the system at four levels
5. you recorded one real failure or one realistic failure analysis
6. you can say how this version connects to later AOIS

## Why You Must Not Rush This Phase

The later frontier topics you care about depend on this exact base:

- observability needs machine and process literacy
- agents need service contracts and tool discipline
- runtime control needs logs, metrics, and debugging reflexes
- inference systems need systems thinking and performance reasoning
- governance is meaningless if the underlying system is vague

Phase 0 is where your later confidence is manufactured.

## Immediate Order

Start here:

1. `v0.1` machine visibility
2. `v0.2` rule-based limits

Do not skip them because they look small.
Their real job is not size.
Their real job is pattern formation.
