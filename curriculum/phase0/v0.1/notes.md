# v0.1 - Linux Essentials

Estimated time: 3-5 focused hours

## What This Builds

This version builds Linux operating confidence.

By the end of it, you should be able to:

- move around the filesystem without getting lost
- inspect files and permissions
- inspect running processes
- read key environment variables
- inspect basic machine state using native Linux commands

## Why This Exists

This version teaches the first operational question:

`what is happening on this machine right now?`

That question sits under later questions like:

- why is the API slow?
- why did the container restart?
- why did the node go unhealthy?
- why did the agent fail at runtime?

If Linux is weak, everything later becomes guessing.

## AOIS Connection

At this stage the AOIS path is:

`machine -> shell command -> visibility`

Later it becomes:

`signal -> ingest -> analyze -> decide -> act`

`v0.1` starts the chain by teaching direct machine inspection.

## Learning Goals

By the end of this version you should be able to:

- navigate the repo without feeling lost
- explain what CPU, memory, and disk signals mean at beginner and technical levels
- inspect file permissions and execution state
- explain why Linux is foundational to later AI infrastructure work
- identify at least one misleading system metric and correct the misreading

## Prerequisites

Run:

```bash
uname -a
pwd
ls
```

Expected behavior:

- `uname -a` confirms you are on Linux
- `pwd` shows you are in the repo
- `ls` shows the repo contents

Important boundary:

- `v0.1` is Linux
- `v0.2` is Bash

## Core Concepts

## Linux Orientation

Linux is not a side topic in AOIS.
It is the operating ground for:

- containers
- cloud VMs
- Kubernetes nodes
- shell automation
- agent tool execution

For `v0.1`, Linux means four things:

- know where you are
- know what files are around you
- know what process is running
- know what the machine is doing

## Filesystem And Navigation

Run:

```bash
pwd
ls
ls -la
cd curriculum
pwd
ls -la
cd ..
```

Expected behavior:

- `pwd` prints your current directory
- `ls` shows visible files
- `ls -la` shows hidden files, permissions, owners, and timestamps
- `cd curriculum` enters the curriculum directory
- `cd ..` returns you to the repo root

Why this matters:

- later you will debug from unfamiliar directories constantly
- you must stop treating terminal location as invisible state

## Processes Permissions And Environment

Run:

```bash
ls -l
ps aux | head -5
echo "$HOME"
echo "$PATH"
```

Expected observations:

- `ls -l` shows whether files are readable or executable
- `ps aux` reminds you that services are just processes
- `HOME` and `PATH` show that shell behavior depends on environment variables

Important conceptual note:

- files have permissions
- processes are the living form of services
- environment variables change command behavior

## Standard Streams And Redirection

Every Linux process starts with three standard streams:

- `stdin`: input
- `stdout`: normal output
- `stderr`: error output

Run:

```bash
echo "hello" > /tmp/hello.txt
cat /tmp/hello.txt
ls /definitely-not-a-real-path 1>/tmp/out.txt 2>/tmp/err.txt || true
cat /tmp/out.txt
cat /tmp/err.txt
```

Expected behavior:

- `hello` is written to `/tmp/hello.txt`
- `out.txt` stays empty for the failing `ls`
- `err.txt` contains the error message

This matters because later logs, pipelines, and scripts all depend on understanding where output actually goes.

## Pipes And Filtering

Run:

```bash
ps aux | head -5
ps aux | grep bash
env | grep HOME
```

Expected behavior:

- the pipe sends one command's output into another
- `grep` filters text instead of forcing you to read all output manually

This is still Linux command usage.
You are not scripting yet.

## The First Three System Signals

### CPU

CPU is work rate.
High CPU can mean:

- heavy useful work
- a hot service
- a runaway loop
- contention

### Memory

Memory is active working space.
High `used` memory is not automatically a crisis.
Linux may use memory aggressively for caching, so `available` often matters more than `used`.

### Disk

Disk is persistent storage.
Disk pressure can mean:

- writes fail
- logs stop growing
- databases misbehave

## Build

There is no Bash script build in `v0.1`.

Run the direct Linux inspection commands instead:

```bash
hostname
top -bn1 | grep "Cpu(s)"
free -h
df -h /
```

Expected learning:

- `hostname` identifies the machine
- `top` exposes a live CPU signal
- `free -h` exposes memory usage
- `df -h /` exposes root filesystem pressure

This is the pure Linux version of the lesson:
read the machine directly before you automate anything.

## Ops Lab

Run:

```bash
hostname
top -bn1 | grep "Cpu(s)"
free -h
df -h /
ps aux | head -5
```

Questions:

1. Which command identifies the machine name?
2. Why is `available` memory more useful than just `used` memory?
3. What filesystem is `df -h /` actually reporting?
4. What does `ps aux` prove about services?

Answer key:

1. `hostname`
2. Because Linux uses memory for cache, so high `used` alone can mislead you
3. The filesystem mounted at `/`, not every filesystem on the machine
4. Services are running processes with PIDs and resource usage

## Break Lab

Do not skip this.

### Option A - Permission break

```bash
touch /tmp/linux-demo.txt
chmod 000 /tmp/linux-demo.txt
cat /tmp/linux-demo.txt
```

Expected symptom:

- `Permission denied`

Fix:

```bash
chmod 644 /tmp/linux-demo.txt
```

Lesson:

- a file can exist and still be unreadable because of permissions

False conclusion this prevents:

- “the file is broken” when the real problem is permission state

### Option B - Path break

```bash
cd /tmp
cd scripts
```

Expected symptom:

- `No such file or directory`

Lesson:

- shell execution depends on exact path correctness

### Option C - Metric break

Look at `free -h` and deliberately misread `used` memory as automatic danger.
Then correct yourself using `available`.

Lesson:

- some failures are conceptual, not mechanical

## Testing

The version passes when:

1. you can navigate directories without getting lost
2. you can inspect permissions, processes, and environment at a basic level
3. you can run and interpret `hostname`, `top`, `free -h`, and `df -h /`
4. you can recover from the permission break

## Common Mistakes

- thinking Linux means “writing shell scripts immediately”
- confusing files, paths, and permissions
- treating high `used` memory as automatic danger
- not realizing `df -h /` is only one filesystem view

## Troubleshooting

When something looks wrong, compare against:

```bash
top -bn1 | grep "Cpu(s)"
free -h
df -h /
pwd
ls -la
```

If the output looks surprising:

- check the raw commands first
- then inspect your assumptions about what the output means

## Benchmark

Measure:

- how quickly you can identify your current directory, hostname, CPU line, memory line, and root filesystem line
- whether you can recover from a permissions mistake without outside help
- whether the terminal feels less opaque at the end of the lesson than at the start

Interpretation:

At `v0.1`, the goal is not automation.
The goal is direct machine legibility.

## Architecture Defense

Why not start with a script?

Because Linux commands must be understandable before shell automation starts composing them.

## 4-Layer Tool Drill

Tool: `ps`

1. Plain English
It shows running processes on the machine.

2. System Role
It gives AOIS direct visibility into what is actually running.

3. Minimal Technical Definition
It is a Linux command that reports currently running processes and their resource information.

4. Hands-on Proof
If you stop checking processes, you lose direct visibility into what services and commands are actually alive.

## 4-Level System Explanation Drill

1. Simple English
I learned how to inspect the machine directly from Linux.

2. Practical Explanation
I can now check files, permissions, processes, environment, CPU, memory, and disk from the terminal.

3. Technical Explanation
It is a Linux fundamentals lesson that teaches direct inspection with native commands before automation.

4. Engineer-Level Explanation
It creates the first AOIS operating layer by teaching direct machine inspection through `pwd`, `ls`, `ps`, `hostname`, `top`, `free`, and `df`, so later automation and service work rest on real operating skill instead of blind command copying.

## Failure Story

Representative failure:

- Symptom: a file existed but could not be read
- Root cause: permissions removed access
- Fix: restore readable permissions with `chmod`
- Prevention: inspect permissions before blaming the file content
- What this taught me: Linux state can block access even when the file is present

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v0.1` solve in plain English?
2. Why is Linux foundational to later AOIS phases?
3. What is the difference between a file existing and a file being executable?
4. Why is `available` memory often more useful than `used` memory?
5. Why is this version about Linux first and not Bash yet?
6. Explain `ps` using the 4-layer tool rule.
7. Explain `v0.1` using the 4-level system explanation rule.

## Connection Forward

`v0.1` teaches the first AOIS habit:

`observe before you interpret`

`v0.2` will keep these Linux commands, but start teaching Bash so you can automate and compose them into real scripts.
