# v0.2 - Bash Scripting And First Automation

Estimated time: 4-6 focused hours

## What This Builds

You will build `scripts/sysinfo.sh`, a Bash script that turns direct Linux inspection commands into a reusable system report.

The report should include:

- timestamp
- host identity
- CPU signal
- memory signal
- disk signal for `/`

This is the first AOIS automation artifact.

## Why This Exists

`v0.1` taught direct Linux inspection.
That was necessary, but not enough.

Real systems work requires you to stop typing the same command sequence manually and start packaging repeatable behavior.

That is Bash.

## AOIS Connection

The AOIS path is now:

`machine -> shell commands -> Bash script -> reusable visibility`

This is still not “intelligence.”
It is repeatable observation through automation.

## Learning Goals

By the end of this version you should be able to:

- explain what a shell script is and why it exists
- understand shebang, execution permission, variables, functions, and command substitution
- use `set -euo pipefail` and explain why it matters
- build and run a small Bash script safely
- explain the difference between Linux commands and Bash automation

## Prerequisites

You should already be comfortable with:

- navigation
- permissions
- `hostname`
- `top`
- `free -h`
- `df -h /`

If `v0.1` still feels shaky, do not continue.

## Core Concepts

### What Bash Adds

Linux commands let you inspect the machine.
Bash lets you:

- sequence commands
- reuse them
- format output
- fail predictably

### Shebang

```bash
#!/usr/bin/env bash
```

This tells the system to run the file with Bash.

### Safety Flags

```bash
set -euo pipefail
```

- `-e`: exit on command failure
- `-u`: fail on unset variables
- `-o pipefail`: fail the pipeline if any stage fails

This is the first serious Bash discipline rule in AOIS.

### Functions

Functions let you package repeated behavior into named blocks.

Example:

```bash
timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}
```

### Command Substitution

```bash
echo "Host: $(hostname)"
```

This runs a command and inserts its output into another command.

## Build

Create or replace `scripts/sysinfo.sh` with this:

```bash
#!/usr/bin/env bash
set -euo pipefail

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

cpu_line() {
  top -bn1 | grep "Cpu(s)" || echo "CPU data unavailable"
}

memory_line() {
  free -h | awk "NR==2 {print \"Mem total=\" \$2 \" used=\" \$3 \" available=\" \$7}"
}

disk_line() {
  df -h / | awk "NR==2 {print \"Disk total=\" \$2 \" used=\" \$3 \" avail=\" \$4 \" use=\" \$5}"
}

echo "AOIS system report"
echo "Timestamp: $(timestamp)"
echo "Host: $(hostname)"
echo "CPU: $(cpu_line)"
echo "MEMORY: $(memory_line)"
echo "DISK: $(disk_line)"
```

Then run:

```bash
chmod +x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

Expected behavior:

- the script runs without permission error
- it prints timestamp, host, CPU, MEMORY, and DISK lines
- values differ by machine, structure stays similar

Expected example:

```text
AOIS system report
Timestamp: 2026-04-23T12:00:00Z
Host: codespace-abc123
CPU: %Cpu(s):  3.2 us,  1.1 sy,  0.0 ni, 95.0 id,  0.2 wa,  0.0 hi,  0.5 si,  0.0 st
MEMORY: Mem total=7.7Gi used=2.1Gi available=5.3Gi
DISK: Disk total=32G used=8.5G avail=22G use=29%
```

## Ops Lab

Compare the script with the raw commands behind it:

```bash
./scripts/sysinfo.sh
top -bn1 | grep "Cpu(s)"
free -h
df -h /
```

Questions:

1. Which part of the script comes from `free -h`?
2. Why is `available` memory more useful than just `used` memory?
3. What filesystem is `df -h /` actually reporting?
4. What did Bash add that Linux commands alone did not?

Answer key:

1. The `MEMORY:` line is derived from row 2 of `free -h`
2. Because Linux uses memory for cache, so high `used` alone can mislead you
3. The filesystem mounted at `/`, not every filesystem on the machine
4. Reuse, formatting, packaging, and repeatable execution

## Break Lab

Do not skip this.

### Option A - Permission break

```bash
chmod -x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

Expected symptom:

- `Permission denied`

Fix:

```bash
chmod +x scripts/sysinfo.sh
```

Lesson:

- a correct script still fails if the file is not executable

### Option B - Unset variable break

Add this line temporarily near the top of the script:

```bash
echo "$NOT_DEFINED"
```

Expected symptom:

- the script exits because `set -u` treats the unset variable as an error

Lesson:

- safety flags make bad assumptions fail early

### Option C - Wrong path break

```bash
./scripts/sys-info.sh
```

Expected symptom:

- `No such file or directory`

## Testing

The version passes when:

1. `scripts/sysinfo.sh` runs successfully
2. you can explain shebang, `set -euo pipefail`, functions, and command substitution
3. you can recover from the permission break
4. you can explain how Bash changed the Linux-only workflow from `v0.1`

## Common Mistakes

- forgetting `chmod +x`
- writing Bash before understanding the Linux commands it wraps
- copying `set -euo pipefail` without understanding it
- confusing command output with string literals inside scripts

## Troubleshooting

If the script will not execute:

- confirm the file exists
- confirm the path is correct
- confirm the execute bit is present

If the script output looks wrong:

- run the raw commands first
- compare their output to the function output
- inspect quoting and command substitution

## Benchmark

Measure:

- script startup feel: instant or noticeable
- whether the output can be interpreted in under 10 seconds
- whether the script removes manual repetition cleanly

Interpretation:

At `v0.2`, good means:

- the script is fast
- the output is readable
- the script saves manual retyping
- the Bash layer remains understandable

## Architecture Defense

Why use Bash here instead of Python?

Because the signals already exist on the machine and Bash is the shortest path to reusable shell automation.

Why not stay with raw Linux commands only?

Because repeating the same command sequence manually does not scale into infrastructure work.

## 4-Layer Tool Drill

Tool: `set -euo pipefail`

1. Plain English
It makes a script fail early instead of continuing through bad state.

2. System Role
It hardens the AOIS shell layer so mistakes do not silently pass.

3. Minimal Technical Definition
It is a combination of Bash safety options that stop execution on command failures, unset variables, and hidden pipeline failures.

4. Hands-on Proof
If it is removed, bad assumptions can survive longer and produce misleading output.

## 4-Level System Explanation Drill

1. Simple English
I turned Linux inspection commands into a reusable Bash script.

2. Practical Explanation
The system now produces the same local health report on demand instead of relying on manual command repetition.

3. Technical Explanation
I wrote a Bash script with functions, command substitution, and safety flags to wrap Linux inspection commands into one repeatable report.

4. Engineer-Level Explanation
AOIS now automates direct Linux visibility through a Bash entrypoint that packages `hostname`, `top`, `free`, and `df` into a consistent report while using `set -euo pipefail` to reduce silent shell failure modes.

## Failure Story

Representative failure:

- Symptom: the script existed but would not run
- Root cause: execute permission was missing
- Fix: `chmod +x scripts/sysinfo.sh`
- Prevention: inspect permissions before assuming the logic is broken
- What this taught me: shell automation still depends on operating-system file state

## Mastery Checkpoint

Do not move on until you can answer:

1. What does Bash add beyond raw Linux commands?
2. What is the purpose of the shebang?
3. Why use `set -euo pipefail`?
4. What is command substitution?
5. Why is this version Bash and not Linux fundamentals?
6. Explain `set -euo pipefail` using the 4-layer tool rule.
7. Explain `v0.2` using the 4-level system explanation rule.

## Connection Forward

`v0.2` teaches the second AOIS habit:

`automate what you can already inspect`

`v0.3` moves from shell automation into Git discipline, where the repo itself becomes engineering memory.
