# v0.1 - Machine Visibility And The First AOIS Signal

Estimated time: 2-3 focused hours

## What This Builds

You will build and understand `scripts/sysinfo.sh`, a small bash script that creates a local machine health snapshot.

It reports:

- CPU usage
- memory usage
- disk usage for `/`
- a timestamp

This is the first real AOIS component.

It does not use AI.
It does not use a web framework.
It does not use a database.

That is the point.

Before a system can analyze anything intelligently, it must first be able to observe something real.

## Why This Exists

This version teaches your first operational question:

What is happening on this machine right now?

That question sits underneath later questions like:

- Why is my API slow?
- Why did the container restart?
- Why did the agent fail?
- Why did latency spike?
- Why is inference unstable?

Most serious failures eventually touch one or more of these resource domains:

- CPU
- memory
- disk

If you cannot inspect these confidently, later AI infrastructure work becomes guesswork.

## AOIS Connection

Right now the system path is:

`machine -> shell command -> script -> visibility`

Later it becomes:

`signal -> ingest -> analyze -> decide -> act`

`v0.1` is the start of that chain.

## Learning Goals

By the end of this version you should be able to:

- explain what CPU, memory, and disk signals actually tell you
- read basic Linux system information commands without panic
- understand what `scripts/sysinfo.sh` is doing line by line
- run the script and interpret its output
- identify at least one misleading metric and explain why it misleads
- explain this script at four system-explanation levels
- explain each major tool at the four-layer tool level

## Prerequisites

Run these commands first.

```bash
uname -a
pwd
ls
ls scripts
```

You should confirm:

- you are on Linux
- you are inside the AOIS repo
- `scripts/sysinfo.sh` exists

If `scripts/sysinfo.sh` is missing, stop and inspect the repository before continuing.

## The System Model

At this stage, think of a machine using three core resource buckets.

### CPU

CPU is the work rate of the machine.
It tells you how busy the processor is doing tasks.

High CPU can mean:

- heavy computation
- too many active processes
- runaway loops
- hot services under load

### Memory

Memory is the machine's short-term working space.
It holds active data and running process state.

Memory pressure can mean:

- applications slow down
- the kernel reclaims aggressively
- processes get killed
- containers hit OOM conditions

### Disk

Disk is persistent storage.
It holds files, logs, packages, databases, and everything that survives process exit.

Disk pressure can mean:

- writes fail
- logs stop growing
- databases misbehave
- systems become unstable

These are the first operational signals AOIS learns to observe.

## The Commands Before The Script

Before trusting a script, inspect the underlying commands yourself.

Run:

```bash
top -bn1 | grep "Cpu(s)"
free -h
df -h /
```

You are doing two things here:

1. learning the underlying tools
2. creating a ground truth for what the script should summarize

## Tool Drill 1 - `top`

### Plain English

`top` shows what the machine is doing right now.

### System Role

It gives AOIS a direct view of live process and CPU activity before we have observability tooling.

### Minimal Technical Definition

`top` is a Linux process-monitoring utility that reports CPU, memory, load, and active processes.

### Hands-on Proof

Without a CPU inspection tool, you lose visibility into whether the machine is busy, idle, or overloaded.

## Tool Drill 2 - `free`

### Plain English

`free` shows how memory is being used.

### System Role

It lets AOIS inspect memory pressure, which is critical for diagnosing slowdowns and OOM-style failures.

### Minimal Technical Definition

`free` is a Linux command that reports memory and swap statistics.

### Hands-on Proof

Without memory visibility, you can misread a healthy system as broken or miss genuine memory pressure entirely.

## Tool Drill 3 - `df`

### Plain English

`df` shows how full a filesystem is.

### System Role

It gives AOIS visibility into storage pressure, which later matters for logs, databases, and container runtime stability.

### Minimal Technical Definition

`df` is a Linux command that reports filesystem disk space usage.

### Hands-on Proof

Without disk visibility, a system can fail writes or crash due to full storage while you are still looking in the wrong place.

## Build

Now inspect the script itself.

Run:

```bash
sed -n '1,220p' scripts/sysinfo.sh
```

Read it in sections.

### Section 1 - Safety mode

```bash
set -euo pipefail
```

This means:

- `-e`: exit on command failure
- `-u`: fail on unset variables
- `-o pipefail`: fail a pipeline if any step fails

This is the first sign of disciplined shell scripting.

### Section 2 - Formatting helpers

The script uses small functions to print headers and timestamps.

This matters because:

- output becomes predictable
- later parsing becomes easier
- humans can inspect it faster

### Section 3 - CPU logic

The CPU function does not rely on one static number.
It samples `/proc/stat` twice.

Why?

Because CPU usage is about change over time, not a single absolute counter.

The script:

1. reads cumulative CPU counters
2. waits briefly
3. reads them again
4. computes the delta
5. calculates the non-idle fraction

That is more rigorous than simply dumping one display line.

### Section 4 - Memory logic

The script parses `free -h` and prints used versus total memory.

Important:
This is useful, but incomplete.

Why incomplete?

Because Linux memory reporting can be misleading if you only look at `used`.

Later you must care about `available`.

That is your first example of a metric that can be read incorrectly.

### Section 5 - Disk logic

The script runs:

```bash
df -h /
```

This restricts the output to the root filesystem.

That is a good first step because it keeps the report focused and readable.

Later you will expand your idea of disk health to multiple mounts and service-specific storage.

## Run The Script

Make sure it is executable and then run it.

```bash
chmod +x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

Expected behavior:

- a timestamp prints first
- CPU section appears
- memory section appears
- disk section appears

The exact numbers will differ.
The structure should not.

## Ops Lab

Now inspect the system and the script output side by side.

Run:

```bash
./scripts/sysinfo.sh
free -h
df -h /
cat /proc/stat | head -n 1
```

Answer these questions:

1. Does the memory line in the script match the `Mem:` line from `free -h`?
2. What field is the script ignoring that matters operationally?
3. Why is CPU sampled twice instead of once?
4. What exact filesystem is being reported by `df -h /` on your machine?

This is where observation becomes understanding.

## Break Lab

Do not skip this.

The point is to learn what failure looks like before the system gets more complex.

Perform one of these safe break exercises:

### Option A - Permission break

```bash
chmod -x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

Observe the failure.
Then fix it:

```bash
chmod +x scripts/sysinfo.sh
```

### Option B - Wrong path break

Run:

```bash
./scripts/sys-info.sh
```

Observe the failure and explain what the shell is telling you.

### Option C - Misread the metric

Read the output of `free -h` and deliberately explain `used` as if it meant "danger".
Then correct yourself using the `available` field.

This is a conceptual failure, and it matters just as much as a command failure.

## Testing

Your current version passes if all of the following are true:

1. `./scripts/sysinfo.sh` runs successfully
2. the output includes timestamp, CPU, MEMORY, and DISK sections
3. the memory and disk values are plausible when compared to `free -h` and `df -h /`
4. you can explain why CPU is sampled twice

## Troubleshooting

Common mistakes:

- forgetting `chmod +x`
- assuming `used` memory means danger
- trusting the script without validating the raw commands
- expecting CPU output to be identical across repeated runs

When something looks wrong, compare against:

```bash
free -h
df -h /
cat /proc/stat | head -n 1
```

## Benchmark

This is an early version, so keep the benchmark simple.

Record:

- script runtime feel: instant or noticeable
- CPU sampling wait time: `0.5` seconds
- whether the output is readable at a glance

This is not about precision yet.
It is about starting the habit of measuring and judging behavior.

## Architecture Defense

Why use a shell script here instead of Python?

Because at this stage:

- the system signals already exist on the machine
- shell commands expose them directly
- setup cost is minimal
- it teaches Linux and scripting at the same time

Why not start with a web API?

Because a service that cannot inspect the machine meaningfully is an abstraction built too early.

## The 4-Layer Tool Rule For This Version

You must be able to answer this for:

- `top`
- `free`
- `df`
- `/proc/stat`
- bash script

### `/proc/stat` example

1. Plain English
It exposes raw CPU accounting data from the Linux system.

2. System Role
It provides the low-level input that the script uses to estimate CPU usage.

3. Minimal Technical Definition
It is a kernel-provided virtual file in `/proc` containing CPU and system statistics.

4. Hands-on Proof
If the script cannot read this data or an equivalent source, its CPU usage calculation stops working.

## The 4-Level AOIS Explanation Drill

You must be able to explain `v0.1` like this.

### Level 1 - Simple English

I built a script that shows how busy and full the machine is.

### Level 2 - Practical Explanation

It prints CPU, memory, and disk usage so I can inspect the machine quickly before building more system layers.

### Level 3 - Technical Explanation

It is a bash script that gathers CPU, memory, and disk signals from Linux commands and files, then formats them into a small report.

### Level 4 - Engineer-Level Explanation

It is an operational inspection script that samples CPU via `/proc/stat`, parses memory from `free -h`, reads root filesystem usage from `df -h /`, and creates a repeatable local health snapshot that later AOIS components can build on conceptually.

## Failure Story

Record one real failure from your run or use this seed template:

- Symptom:
- Root cause:
- Fix:
- Prevention:

Good examples:

- forgot execute permission
- misread memory output
- assumed CPU should be identical across two runs
- trusted the script without validating the underlying commands

## Mastery Checkpoint

Do not move forward until you can answer all of these without guessing.

1. What problem does `v0.1` solve in plain English?
2. Where does this script sit in the AOIS system story?
3. What is `free -h` technically?
4. What breaks if you stop checking disk usage?
5. Why is `available` memory often more important than `used` memory?
6. Why is CPU sampled twice?
7. Why is `df -h /` narrower than `df -h`?
8. What is the difference between observing a system and understanding a system?
9. Explain `scripts/sysinfo.sh` at all four system-explanation levels.
10. Explain one tool from this version using the four-layer rule.

## Connection Forward

This version creates the first AOIS habit:

observe before you interpret

That matters immediately in `v0.2`, where you will move from raw signals to rule-based interpretation and then discover why rules alone stop being enough.
