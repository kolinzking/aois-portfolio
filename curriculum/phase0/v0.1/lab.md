# v0.1 Lab

## Build Lab

Run:

```bash
chmod +x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

Verify that the report includes:

- timestamp
- CPU
- MEMORY
- DISK

Expected structure:

```text
Timestamp: YYYY-MM-DD HH:MM:SS UTC

==== CPU ====
Usage: N.N%

==== MEMORY ====
Used: X / Y

==== DISK ====
Used: X / Y
```

Answer key:

- The exact numbers will differ.
- The ordering and section names should not.
- If one section is missing, the script or file execution is wrong.

## Ops Lab

Run:

```bash
top -bn1 | grep "Cpu(s)"
free -h
df -h /
cat /proc/stat | head -n 1
./scripts/sysinfo.sh
```

Write down:

- what each command shows
- what the script summarizes
- what the script does not yet show

Expected observations:

- `top -bn1 | grep "Cpu(s)"` shows a live CPU summary line
- `free -h` shows memory totals, used, free, cache, and available
- `df -h /` shows usage for the root filesystem
- `cat /proc/stat | head -n 1` shows raw cumulative CPU counters
- `./scripts/sysinfo.sh` summarizes CPU, memory, and root disk into one report

Answer key:

- `top` shows a live snapshot; the script computes CPU from `/proc/stat`
- `free -h` shows more detail than the script currently prints
- the script does not yet show `available` memory
- the script does not yet show disk percentage
- the script does not yet show multiple mounts

## Break Lab

Do one:

```bash
chmod -x scripts/sysinfo.sh
./scripts/sysinfo.sh
chmod +x scripts/sysinfo.sh
```

Or:

```bash
./scripts/sys-info.sh
```

Explain the exact failure in plain language and technical language.

Expected failure examples:

- `chmod -x` path:
  - plain language: the file exists, but the shell is not allowed to execute it
  - technical language: execute permission is missing on the script file
- wrong-path case:
  - plain language: you asked the shell to run a file that does not exist
  - technical language: the path `./scripts/sys-info.sh` does not resolve to a real file

## Explanation Lab

Answer for `free`:

1. What problem does it solve?
2. Where does it sit in AOIS?
3. What is it technically?
4. What happens if you remove it from your inspection toolkit?

Then explain `v0.1` at:

1. simple English
2. practical level
3. technical level
4. engineer level

Answer key for `free`:

1. What problem does it solve?
It shows how memory is being used so you can judge whether the machine may be under memory pressure.

2. Where does it sit in AOIS?
It sits in the earliest inspection layer, before later automation and observability stacks exist.

3. What is it technically?
It is a Linux command that reports memory and swap usage.

4. What happens if you remove it from your inspection toolkit?
You lose a primary visibility source for diagnosing slowdowns, OOM conditions, and misleading memory interpretations.

Answer key for `v0.1`:

1. Simple English
I built a script that shows how busy and full the machine is.

2. Practical level
It prints CPU, memory, and disk usage so I can inspect the machine quickly before building more system layers.

3. Technical level
It is a bash script that gathers system signals from Linux commands and files and formats them into a readable report.

4. Engineer level
It is an operational inspection script that samples CPU via `/proc/stat`, parses memory from `free -h`, reads root filesystem usage from `df -h /`, and creates a repeatable local health snapshot for later AOIS troubleshooting and observability work.

## Defense Lab

Answer:

Why start AOIS with a shell script instead of a Python service or web API?

Answer key:

Because the system signals already exist locally, shell commands expose them directly, the setup cost is low, and this version is supposed to build Linux and scripting fluency before introducing service-layer abstractions.
