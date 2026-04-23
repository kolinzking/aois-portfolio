# v0.2 Lab

## Build Lab

Create `scripts/sysinfo.sh` exactly as shown in `notes.md`, make it executable, and run it.

Success state:

- the script executes
- the output is readable
- the report includes timestamp, host, CPU, MEMORY, and DISK

## Ops Lab

Run:

```bash
./scripts/sysinfo.sh
top -bn1 | grep "Cpu(s)"
free -h
df -h /
```

Expected learning:

- the report is a summary of real machine commands, not magic
- you should be able to map each output line back to its source command

## Break Lab

Break the execute permission:

```bash
chmod -x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

Then recover:

```bash
chmod +x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

## Explanation Lab

Answer:

1. why is Bash in AOIS after Linux?
2. what is the difference between command execution and automation?
3. why does `set -euo pipefail` matter?

## Defense Lab

Defend:

`using Bash for the first AOIS automation artifact is the right decision`
