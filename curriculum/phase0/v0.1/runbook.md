# v0.1 Runbook

## Purpose

Use this runbook when `scripts/sysinfo.sh` does not behave as expected.

## Common Checks

### 1. Confirm the file exists

```bash
ls -l scripts/sysinfo.sh
```

### 2. Confirm it is executable

```bash
chmod +x scripts/sysinfo.sh
```

### 3. Run it directly

```bash
./scripts/sysinfo.sh
```

### 4. Validate the underlying commands

```bash
free -h
df -h /
cat /proc/stat | head -n 1
```

## If The Script Fails To Execute

Likely causes:

- wrong path
- missing execute permission
- file contents changed incorrectly

## If The Output Looks Wrong

Check:

- whether `free -h` output matches the memory section
- whether `df -h /` output matches the disk section
- whether CPU changed between samples

## If Interpretation Is Confusing

Remember:

- `used` memory is not automatically danger
- `available` memory is often the more important signal
- CPU usage is derived from changing counters, not one fixed value

## Escalation Question

If the script runs but you cannot explain the output, the bug is in understanding, not execution.
Go back to the notes and answer the mastery questions before proceeding.
