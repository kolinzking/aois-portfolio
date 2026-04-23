# v0.1 Summary Notes

## What You Built

You built `scripts/sysinfo.sh`, a first-pass machine inspection script for AOIS.

## What You Actually Learned

- AOIS starts with observation before interpretation
- CPU, memory, and disk are foundational machine signals
- shell scripting can expose useful operational signals quickly
- summarized output is useful, but it can still hide important detail
- `used` memory is often a misleading signal on Linux

## What Matters Most

The most important lesson in `v0.1` is not the script itself.
It is the engineering habit:

inspect the underlying command before trusting the summarized report

## Commands Worth Remembering

```bash
free -h
df -h /
cat /proc/stat | head -n 1
./scripts/sysinfo.sh
```

## Core Limitation

`v0.1` gives visibility, not interpretation.
It tells you what the machine looks like.
It does not yet tell you what that state means.
