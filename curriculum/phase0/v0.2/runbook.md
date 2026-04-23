# v0.2 Runbook

## Purpose

Use this runbook when `scripts/log_analyzer.sh` behaves unexpectedly.

## Core Checks

### 1. Confirm the script exists

```bash
ls -l scripts/log_analyzer.sh
```

### 2. Confirm execute permission

```bash
chmod +x scripts/log_analyzer.sh
```

### 3. Run a known-good example

```bash
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
```

Expected:

```text
Detected: Memory Issue
```

### 4. Test a known non-match

```bash
./scripts/log_analyzer.sh "container terminated because it ran out of memory"
```

Expected:

```text
Detected: Unknown Issue
```

This is not a runtime failure.
It is the lesson.

## If The Script Returns `Unknown Issue`

Check:

- whether the exact keyword is present
- whether the log was quoted correctly as one argument
- whether you are expecting semantic understanding from a keyword matcher

## If The Script Behaves Strangely On Multi-Word Logs

Most likely cause:

- missing quotes around the input string

Correct usage:

```bash
./scripts/log_analyzer.sh "gateway returned 5xx"
```

## If The Output Feels Too Broad

That is expected for rules like:

- `5xx -> Server Error`

The script is giving a bucket, not a root cause.

## Escalation Question

If you want the script to handle more cases, ask yourself first:

- am I fixing one case?
- or am I beginning the rule explosion that proves this version's lesson?
