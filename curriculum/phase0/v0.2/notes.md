# v0.2 - Bash Scripting And First Automation

Estimated time: 6-8 focused hours

Authoring status: authored

## What This Builds

You will build two Bash scripts:

- `scripts/sysinfo.sh`, a reusable local system report
- `scripts/log_analyzer.sh`, a small rule-based log classifier

`scripts/sysinfo.sh` turns direct Linux inspection commands into reusable output.
The report includes:

- timestamp
- host identity
- CPU signal
- memory signal
- disk signal for `/`

`scripts/log_analyzer.sh` turns a raw incident message into a basic classification.
It is intentionally limited so you can feel where deterministic rules help and where they break.

## Why This Exists

`v0.1` taught direct Linux inspection.
That was necessary, but not enough.

Real systems work requires you to stop typing the same command sequence manually and start packaging repeatable behavior.

That is Bash.

This version also introduces the first interpretation boundary:

- visibility says what is present
- rules classify what the text appears to mean
- richer AI analysis later handles ambiguity, context, and tradeoffs better than fixed string rules

## AOIS Connection

The AOIS path is now:

`machine -> shell commands -> Bash scripts -> reusable visibility -> first brittle interpretation`

This is still not real AI intelligence.
It is the first useful automation layer and the first proof that rules alone are limited.

## Learning Goals

By the end of this version you should be able to:

- explain what a shell script is and why it exists
- understand shebang, execution permission, variables, functions, and command substitution
- use `set -euo pipefail` and explain why it matters
- build and run a small Bash script safely
- explain the difference between Linux commands and Bash automation
- classify a few operational messages with simple string rules
- explain why rule-based interpretation fails under wording changes
- decide when a failure is in the script, in the input, or in the assumption behind the rule

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

### Positional Arguments

Shell scripts receive arguments.

If you run:

```bash
./scripts/log_analyzer.sh "gateway returned 5xx"
```

then the script receives the message as input.

In Bash:

- `$0` is the script name
- `$1` is the first argument
- `$#` is the number of arguments
- `$*` expands all arguments into one message-like string

This matters because scripts are not only command bundles.
They can also receive operational signals.

### Branching

Bash can choose behavior with `if`, `elif`, `else`, and `fi`.

That is enough to build a primitive log classifier:

- if the message mentions `OOMKilled`, classify memory pressure
- if it mentions `CrashLoopBackOff`, classify a restart loop
- if it mentions `5xx`, classify service error
- otherwise preserve the raw message as unknown

This is useful, but brittle.
Rules match text.
They do not understand the system.

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

Create or replace `scripts/log_analyzer.sh` with this:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <log message>" >&2
  exit 2
fi

message="$*"
normalized="$(printf '%s' "$message" | tr '[:upper:]' '[:lower:]')"

if [[ "$normalized" == *"oomkilled"* || "$normalized" == *"exit code 137"* ]]; then
  echo "classification=memory-pressure severity=high action='inspect memory, limits, and recent restarts'"
elif [[ "$normalized" == *"crashloopbackoff"* || "$normalized" == *"restarting"* ]]; then
  echo "classification=restart-loop severity=high action='inspect process logs and last exit reason'"
elif [[ "$normalized" == *"5xx"* || "$normalized" == *"gateway"* ]]; then
  echo "classification=service-error severity=medium action='inspect HTTP path, upstream service, and recent deploy'"
elif [[ "$normalized" == *"permission denied"* ]]; then
  echo "classification=permission-error severity=medium action='inspect path, owner, mode, and execution context'"
else
  echo "classification=unknown severity=unknown action='preserve raw message and escalate to richer analysis'"
fi
```

Then run:

```bash
chmod +x scripts/sysinfo.sh
chmod +x scripts/log_analyzer.sh
./scripts/sysinfo.sh
./scripts/log_analyzer.sh "gateway returned 5xx after deploy"
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
./scripts/log_analyzer.sh "strange message with no match"
```

Expected behavior:

- the script runs without permission error
- it prints timestamp, host, CPU, MEMORY, and DISK lines
- values differ by machine, structure stays similar
- the analyzer classifies known phrases
- unmatched messages are preserved as `unknown`

Expected example:

```text
AOIS system report
Timestamp: 2026-04-23T12:00:00Z
Host: codespace-abc123
CPU: %Cpu(s):  3.2 us,  1.1 sy,  0.0 ni, 95.0 id,  0.2 wa,  0.0 hi,  0.5 si,  0.0 st
MEMORY: Mem total=7.7Gi used=2.1Gi available=5.3Gi
DISK: Disk total=32G used=8.5G avail=22G use=29%
```

Expected analyzer examples:

```text
classification=service-error severity=medium action='inspect HTTP path, upstream service, and recent deploy'
classification=memory-pressure severity=high action='inspect memory, limits, and recent restarts'
classification=unknown severity=unknown action='preserve raw message and escalate to richer analysis'
```

## Ops Lab

Compare the script with the raw commands behind it:

```bash
./scripts/sysinfo.sh
top -bn1 | grep "Cpu(s)"
free -h
df -h /
./scripts/log_analyzer.sh "pod CrashLoopBackOff restarting"
./scripts/log_analyzer.sh "Permission denied reading /var/log/app.log"
./scripts/log_analyzer.sh "latency went up but no error string matched"
```

Questions:

1. Which part of the script comes from `free -h`?
2. Why is `available` memory more useful than just `used` memory?
3. What filesystem is `df -h /` actually reporting?
4. What did Bash add that Linux commands alone did not?
5. Which analyzer result is strongest, and which one is weakest?
6. Why is `unknown` safer than pretending every message has a confident classification?

Answer key:

1. The `MEMORY:` line is derived from row 2 of `free -h`
2. Because Linux uses memory for cache, so high `used` alone can mislead you
3. The filesystem mounted at `/`, not every filesystem on the machine
4. Reuse, formatting, packaging, and repeatable execution
5. Strong matches like `OOMKilled` or `CrashLoopBackOff` are stronger because the wording is specific; vague latency text is weaker because the script has no context
6. `unknown` preserves honesty and prevents a false operational conclusion

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

### Option D - Rule brittleness break

Run:

```bash
./scripts/log_analyzer.sh "the service is unhealthy after the rollout"
```

Expected symptom:

- the result is `classification=unknown`

Lesson:

- the script may miss a real incident if the wording does not match its rules

False conclusion this prevents:

- "the system is healthy because the rule did not match"

## Testing

The version passes when:

1. `scripts/sysinfo.sh` runs successfully
2. `scripts/log_analyzer.sh` classifies known examples and preserves unknown examples
3. you can explain shebang, `set -euo pipefail`, functions, arguments, branching, and command substitution
4. you can recover from the permission break
5. you can explain how Bash changed the Linux-only workflow from `v0.1`
6. you can explain why string matching is useful but brittle

## Common Mistakes

- forgetting `chmod +x`
- writing Bash before understanding the Linux commands it wraps
- copying `set -euo pipefail` without understanding it
- confusing command output with string literals inside scripts
- treating string matches as real understanding
- making every unmatched message look safe instead of unknown

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
- whether known analyzer examples classify correctly
- whether unknown messages remain clearly unknown

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | Both scripts run, you can explain every Bash mechanism used, and you can identify rule brittleness without help. |
| 4/5 | Both scripts run and explanations are mostly strong, but one Bash concept needs review. |
| 3/5 | Scripts run, but you still copy patterns without confidently diagnosing failures. |
| 2/5 | One script works, but debugging depends on guesswork. |
| 1/5 | The scripts are opaque and failures feel random. |

Interpretation:

At `v0.2`, good means:

- the script is fast
- the output is readable
- the script saves manual retyping
- the Bash layer remains understandable
- the analyzer is useful only within the limits of its rules

## Architecture Defense

Why use Bash here instead of Python?

Because the signals already exist on the machine and Bash is the shortest path to reusable shell automation.
It also exposes the limits of text rules before introducing Python services and AI analysis.

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

Tool: string-matching rules

1. Plain English
They classify messages by looking for known words or phrases.

2. System Role
They create AOIS's first interpretation layer after raw machine visibility.

3. Minimal Technical Definition
They are deterministic Bash conditional checks over normalized input text.

4. Hands-on Proof
If the incident wording changes, the script can return `unknown` even when the underlying problem is real.

## 4-Level System Explanation Drill

1. Simple English
I turned Linux inspection commands and a few log patterns into reusable Bash scripts.

2. Practical Explanation
The system now produces a local health report and can classify a few common incident messages on demand.

3. Technical Explanation
I wrote Bash scripts with functions, arguments, command substitution, branching, text normalization, and safety flags.

4. Engineer-Level Explanation
AOIS now has a reusable shell automation layer that packages local machine inspection and deterministic incident classification, proving both the value of automation and the limit of brittle text rules before the system moves into Git discipline, typed Python, API contracts, and AI-backed analysis.

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
5. What is the difference between a function and a raw command?
6. How does `scripts/log_analyzer.sh` receive input?
7. Why is string matching useful?
8. Why is string matching brittle?
9. Why is `unknown` a better answer than a fake confident classification?
10. Why is this version Bash and not Linux fundamentals?
11. Explain `set -euo pipefail` using the 4-layer tool rule.
12. Explain rule-based log classification using the 4-layer tool rule.
13. Explain `v0.2` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What does Bash add beyond raw Linux commands?

Bash adds sequencing, reuse, formatting, branching, variables, functions, arguments, and repeatable execution.
It turns commands you understand into automation.

2. What is the purpose of the shebang?

The shebang tells the operating system which interpreter should run the file.
For this lesson, `#!/usr/bin/env bash` tells the system to run the script with Bash.

3. Why use `set -euo pipefail`?

It makes scripts fail earlier and more honestly.
`-e` exits on command failure, `-u` fails on unset variables, and `pipefail` prevents hidden pipeline failures from looking successful.

4. What is command substitution?

Command substitution runs a command and inserts its output into another command.
Example: `echo "Host: $(hostname)"` runs `hostname` and places the result in the printed line.

5. What is the difference between a function and a raw command?

A raw command runs one operation directly.
A function gives a name to a reusable block of shell logic, so the script can call that logic consistently.

6. How does `scripts/log_analyzer.sh` receive input?

It receives command-line arguments.
The script checks `$#` for argument count and uses `$*` to combine the message text for rule matching.

7. Why is string matching useful?

It is fast, simple, deterministic, and good for known patterns like `OOMKilled`, `CrashLoopBackOff`, `5xx`, or `permission denied`.
It gives AOIS a first interpretation layer before AI is introduced.

8. Why is string matching brittle?

It matches wording, not meaning.
If the incident is real but phrased differently, the rule may miss it.

9. Why is `unknown` a better answer than a fake confident classification?

`unknown` preserves honesty.
A fake classification can send the operator down the wrong path and hide the fact that the rule set did not understand the message.

10. Why is this version Bash and not Linux fundamentals?

`v0.1` taught raw Linux inspection.
`v0.2` assumes those commands are understood and teaches how to package them into repeatable scripts.

11. Explain `set -euo pipefail` using the 4-layer tool rule.

- Plain English: it makes bad script state fail early.
- System Role: it hardens AOIS shell automation against silent failure.
- Minimal Technical Definition: it is a set of Bash options controlling failure behavior.
- Hands-on Proof: without it, unset variables or failed commands may continue and produce misleading output.

12. Explain rule-based log classification using the 4-layer tool rule.

- Plain English: it labels messages by looking for known words.
- System Role: it is AOIS's first interpretation layer after visibility.
- Minimal Technical Definition: it is deterministic branching over normalized input text.
- Hands-on Proof: if the wording changes, a real issue can return `unknown`.

13. Explain `v0.2` using the 4-level system explanation rule.

- Simple English: I turned commands and simple incident patterns into reusable scripts.
- Practical explanation: I can run a system report and classify a few known log messages.
- Technical explanation: I used Bash functions, arguments, branching, command substitution, text normalization, and safety flags.
- Engineer-level explanation: AOIS now has a reusable shell automation layer that proves both the value of deterministic automation and the limits of brittle string rules before moving into Git, HTTP, Python, and AI-backed analysis.

## Connection Forward

`v0.2` teaches the second AOIS habit:

`automate what you can already inspect`

`v0.3` moves from shell automation into Git discipline, where the repo itself becomes engineering memory.

## Source Notes

This version uses stable Bash behavior and local command-line operation.
No fast-moving external source is required for the core lesson.

If this script is later adapted for production shell entrypoints, CI runners, or container init behavior, add source notes for that runtime because shell behavior, working directories, and available commands may differ.
