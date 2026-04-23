# v0.2 Lab

## Build Lab

Run:

```bash
chmod +x scripts/log_analyzer.sh
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
./scripts/log_analyzer.sh "pod CrashLoopBackOff restarting"
./scripts/log_analyzer.sh "gateway returned 5xx"
./scripts/log_analyzer.sh "strange message with no match"
```

Verify the four expected outputs.

## Ops Lab

Run:

```bash
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
./scripts/log_analyzer.sh "gateway returned 503 upstream timeout"
./scripts/log_analyzer.sh "container exited after memory exhaustion"
./scripts/log_analyzer.sh "service unavailable after repeated restart"
```

Write down:

- which messages matched
- which meaningful messages failed to match
- which label was too broad to trust as a diagnosis

## Break Lab

Run these on purpose:

```bash
./scripts/log_analyzer.sh "container terminated because it ran out of memory"
./scripts/log_analyzer.sh
./scripts/log_analyzer.sh pod OOMKilled exit code 137
```

Explain the exact failure mode in each case.

## Explanation Lab

Answer the four-layer rule for:

- Bash positional arguments
- Bash pattern matching
- shell quoting
- rule-based classifier

Then explain `v0.2` at:

1. simple English
2. practical level
3. technical level
4. engineer level

## Defense Lab

Answer:

Why is it worth building a brittle rule engine before moving to AI?
