# v0.1 - Linux Essentials

Estimated time: 5-7 focused hours

Quality Target: Elite

Quality Stamp: Authored / Foundation-Grade

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
- distinguish `stdout` from `stderr`
- explain what a pipe is doing between two Linux commands
- explain why Linux is foundational to later AI infrastructure work
- identify at least one misleading system metric and correct the misreading
- explain why a command failed because of path, permission, or context

## Prerequisites

Run:

```bash
uname -a
pwd
ls
echo "$SHELL"
```

Expected behavior:

- `uname -a` confirms you are on Linux
- `pwd` shows you are in the repo
- `ls` shows the repo contents
- `echo "$SHELL"` shows the active shell path

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

This version is intentionally direct.

You are learning to inspect a real machine without hiding behind:

- helper scripts
- dashboards
- container tooling
- Kubernetes abstractions

Those layers come later.
If Linux inspection is weak, every later layer becomes cargo culting.

## The Shell Prompt Is Telling You Something

When you open a terminal, you are usually looking at a shell prompt.
It may look different on different machines, but it normally encodes at least some of:

- who you are
- what machine you are on
- where you currently are

Example shape:

```text
collins@host:~/aois-portfolio$
```

What you should read from that:

- `collins` is the current user
- `host` is the machine name
- `~/aois-portfolio` is the current working directory
- `$` usually means you are not root

The prompt is not decoration.
It is live state.
Ignoring it is one of the fastest ways to get lost.

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

Typical `pwd` output shape:

```text
/home/collins/aois-portfolio
```

Typical `ls` output shape from repo root:

```text
curriculum
scripts
README.md
```

Expected output shape for `ls -la`:

```text
total ...
drwxr-xr-x ...
drwxr-xr-x ...
-rw-r--r-- ... README.md
drwxr-xr-x ... curriculum
```

Interpret the first column:

- `drwxr-xr-x`
- first character: directory or file type
- next three: owner permissions
- next three: group permissions
- last three: other permissions

What the first permission character means:

- `d` = directory
- `-` = regular file

What the next 9 characters mean:

- owner permissions
- group permissions
- other permissions

For example:

- `rwx` = can read, write, execute
- `r-x` = can read and execute, but not write
- `rw-` = can read and write, but not execute
- `---` = no permission

Directory meaning is slightly different from file meaning:

- `r` on a directory means you can list entries
- `x` on a directory means you can enter or traverse it
- `w` on a directory means you can modify entries inside it if other conditions also allow it

That is why a directory can exist, be visible in some contexts, and still resist access.

Why this matters:

- later you will debug from unfamiliar directories constantly
- you must stop treating terminal location as invisible state

Absolute versus relative path:

- absolute path starts at `/` and works from anywhere
- relative path depends on where you are now

Examples:

- absolute: `/home/collins/aois-portfolio/curriculum`
- relative from repo root: `curriculum`

Quick self-check:

- if you are in `/home/collins/aois-portfolio`, `cd curriculum` works
- if you are in `/tmp`, `cd curriculum` fails
- from `/tmp`, `cd /home/collins/aois-portfolio/curriculum` still works

That is the practical difference between relative and absolute paths.

Recognition drill:

Look at each path and classify it:

- `/etc` -> absolute
- `curriculum` -> relative
- `../scripts` -> relative
- `./curriculum` -> relative

If you cannot classify the path instantly, path handling is still weak.

## Processes Permissions And Environment

Run:

```bash
ls -l
ls -l curriculum
ps aux | head -5
echo "$HOME"
echo "$PATH"
```

Expected observations:

- `ls -l` shows whether files are readable or executable
- `ls -l curriculum` proves directories also have permission bits
- `ps aux` reminds you that services are just processes
- `HOME` and `PATH` show that shell behavior depends on environment variables

Expected output shape for `ps aux | head -5`:

```text
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
...
```

The columns you must recognize now:

- `USER`: who owns the process
- `PID`: the process id
- `%CPU`: CPU usage
- `%MEM`: memory usage
- `COMMAND`: what is running

Two more columns worth noticing:

- `VSZ`: virtual memory size
- `RSS`: resident memory actually held in RAM

You do not need deep mastery of `VSZ` and `RSS` yet.
You do need to stop treating `ps aux` as unreadable noise.

One more thing to notice:

- the line at the very top is a header
- every line below it is one process snapshot

That means `ps aux` is not a story.
It is a table.
Read it like one.

Important conceptual note:

- files have permissions
- processes are the living form of services
- environment variables change command behavior

Permission model:

- owner
- group
- others

Common meanings:

- `r` = read
- `w` = write
- `x` = execute

If a file exists but the permission bits block access, Linux will refuse the action even when the path is correct.

Typical `ls -l` output shape:

```text
-rw-r--r-- 1 collins collins ... README.md
drwxr-xr-x 3 collins collins ... curriculum
```

What this proves:

- files and directories both have owners
- files and directories both have permissions
- the first character changes with the file type
- the permission groups always follow the same owner/group/other pattern

That distinction matters:

- path correctness answers "did I point at the right thing?"
- permissions answer "am I allowed to use it?"

Those are different failure classes.

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
echo $?
```

Expected behavior:

- `hello` is written to `/tmp/hello.txt`
- `out.txt` stays empty for the failing `ls`
- `err.txt` contains the error message
- the final `echo $?` prints the exit code of the most recent command, not the earlier failing `ls`

Typical `err.txt` content:

```text
ls: cannot access '/definitely-not-a-real-path': No such file or directory
```

This is your first proof that:

- normal output and error output are different things
- they may both appear on screen, but they are not the same stream

This matters because later logs, pipelines, and scripts all depend on understanding where output actually goes.

Important caution:

once you run another command, `$?` changes.
So if you want the exit code of a failing command, inspect it immediately after that command.

## Pipes And Filtering

Run:

```bash
ps aux | head -5
ps aux | grep bash
env | grep HOME
pwd | cat
```

Expected behavior:

- the pipe sends one command's output into another
- `grep` filters text instead of forcing you to read all output manually
- `pwd | cat` proves that even a simple line of text can move through a pipe

Plain-English mental model:

- one command produces text
- the pipe passes that text forward
- the next command transforms or filters it

If you run:

```bash
env | grep HOME
```

the left command prints many lines.
The right command keeps only the lines that match `HOME`.

If you run:

```bash
pwd | cat
```

the left command prints one line.
The pipe passes that line to `cat`.
`cat` prints it back out.
Nothing magical happened.
The text just flowed from one process to another.

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

Important caution:

high CPU is a signal, not a verdict.
It tells you where to inspect next, not what the final diagnosis is.

### Memory

Memory is active working space.
High `used` memory is not automatically a crisis.
Linux may use memory aggressively for caching, so `available` often matters more than `used`.

Important caution:

if you only stare at `used`, you can call a healthy Linux system unhealthy.

### Disk

Disk is persistent storage.
Disk pressure can mean:

- writes fail
- logs stop growing
- databases misbehave

Important caution:

`df -h /` is useful, but narrow.
It shows the filesystem mounted at `/`, not every mount on the machine.

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

Expected output shape:

```text
<hostname>
%Cpu(s): ...
               total        used        free      shared  buff/cache   available
Filesystem      Size  Used Avail Use% Mounted on
```

You do not need your numbers to match mine.
You do need your output shape to match the command family:

- one host line
- one CPU summary line
- one memory table
- one filesystem table

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
pwd
```

Questions:

1. Which command identifies the machine name?
2. Why is `available` memory more useful than just `used` memory?
3. What filesystem is `df -h /` actually reporting?
4. What does `ps aux` prove about services?
5. If `pwd` says `/tmp`, why might `cd curriculum` fail even though the directory exists somewhere else?
6. Which outputs in this lab are tables rather than single-value answers?

Answer key:

1. `hostname`
2. Because Linux uses memory for cache, so high `used` alone can mislead you
3. The filesystem mounted at `/`, not every filesystem on the machine
4. Services are running processes with PIDs and resource usage
5. Because relative paths depend on the current directory, and `/tmp/curriculum` may not exist
6. `ps aux`, `free -h`, and `df -h /` are tabular outputs

## Break Lab

Do not skip this.

### Option A - Permission break

```bash
touch /tmp/linux-demo.txt
chmod 000 /tmp/linux-demo.txt
cat /tmp/linux-demo.txt
ls -l /tmp/linux-demo.txt
```

Expected symptom:

- `Permission denied`
- `ls -l` shows blocked permission bits

Fix:

```bash
chmod 644 /tmp/linux-demo.txt
ls -l /tmp/linux-demo.txt
```

Lesson:

- a file can exist and still be unreadable because of permissions

False conclusion this prevents:

- “the file is broken” when the real problem is permission state

### Option B - Path break

```bash
cd /tmp
pwd
cd scripts
```

Expected symptom:

- `No such file or directory`
- `pwd` proves you are in `/tmp`, not in the repo root

Lesson:

- shell execution depends on exact path correctness

False conclusion this prevents:

- "Linux lost my directory" when the real problem is your current location

### Option C - Metric break

Look at `free -h` and deliberately misread `used` memory as automatic danger.
Then correct yourself using `available`.

Lesson:

- some failures are conceptual, not mechanical

False conclusion this prevents:

- "the machine is in danger" when the metric is being interpreted badly

## Testing

The version passes when:

1. you can navigate directories without getting lost
2. you can inspect permissions, processes, and environment at a basic level
3. you can run and interpret `hostname`, `top`, `free -h`, and `df -h /`
4. you can recover from the permission break
5. you can explain the difference between `stdout` and `stderr`
6. you can explain why a relative path can fail while an absolute path succeeds
7. you can read the major columns in `ps aux` without panic
8. you can explain what changed after `chmod 000` and `chmod 644`

## Common Mistakes

- thinking Linux means “writing shell scripts immediately”
- confusing files, paths, and permissions
- treating high `used` memory as automatic danger
- not realizing `df -h /` is only one filesystem view
- seeing `ps aux` as unreadable text instead of structured columns
- forgetting that error output and normal output are different streams
- checking `$?` too late and blaming the wrong command

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

If a command fails:

- verify the path
- verify permissions
- verify whether the message was written to `stderr`
- only then invent a higher-level explanation

If you are still confused:

- say what directory you are in
- say what exact command you ran
- say what exact output appeared
- say whether the failure was path, permission, process, or interpretation

That habit is the beginning of operational debugging.

## Benchmark

Measure:

- how quickly you can identify your current directory, hostname, CPU line, memory line, and root filesystem line
- whether you can recover from a permissions mistake without outside help
- whether you can explain why `cd curriculum` is location-dependent
- whether the terminal feels less opaque at the end of the lesson than at the start
- whether you can classify a failure as path, permission, or interpretation without guessing

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can run the checks, interpret them, recover from the breaks, and explain the false conclusions without help. |
| 4/5 | You can run and recover, but one explanation is still vague. |
| 3/5 | You can follow the commands, but diagnosis still depends on hints. |
| 2/5 | You can produce output, but cannot reliably explain what it means. |
| 1/5 | You are still copying commands blindly. |

Interpretation:

At `v0.1`, the goal is not automation.
The goal is direct machine legibility.

If you still treat the machine as a black box, this lesson is unfinished.

Minimum pass:

- score at least `4/5`
- classify one path failure correctly
- classify one permission failure correctly
- explain why `used` memory alone can mislead you
- explain why `stderr` and `stdout` separation matters later for scripts and logs

## Architecture Defense

Why not start with a script?

Because Linux commands must be understandable before shell automation starts composing them.

Why not jump to Docker or Kubernetes?

Because those systems still sit on Linux machines, Linux filesystems, Linux processes, and Linux resource pressure.
Skipping Linux does not remove the dependency.
It only hides it until something breaks.

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
8. What is the difference between a relative path and an absolute path?
9. What is the difference between `stdout` and `stderr`?
10. Why can a command be correct but still fail because of operating context?
11. What does `x` mean on a file, and what does `x` mean on a directory?
12. Why is `ps aux` better read as a table than as a paragraph?

## Connection Forward

`v0.1` teaches the first AOIS habit:

`observe before you interpret`

`v0.2` will keep these Linux commands, but start teaching Bash so you can automate and compose them into real scripts.

## Source Notes

This version uses stable Linux command behavior and local terminal observation.
No fast-moving external source is required for the core lesson.

If this version is later adapted to containers, remote VMs, or Kubernetes nodes, add source notes for that runtime because process, filesystem, and permission visibility can change under isolation.
