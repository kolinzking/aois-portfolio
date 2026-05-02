# v0.2 Lab

Authoring status: authored

## Build Lab

Create `scripts/sysinfo.sh` and `scripts/log_analyzer.sh` exactly as shown in `notes.md`, make them executable, and run them.

Success state:

- both scripts execute
- the system report output is readable
- the report includes timestamp, host, CPU, MEMORY, and DISK
- the log analyzer classifies known incident phrases
- unmatched messages are preserved as `unknown`

## Ops Lab

Run:

```bash
./scripts/sysinfo.sh
./scripts/log_analyzer.sh "gateway returned 5xx after deploy"
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
./scripts/log_analyzer.sh "strange message with no match"
top -bn1 | grep "Cpu(s)"
free -h
df -h /
```

Expected learning:

- the report is a summary of real machine commands, not magic
- you should be able to map each output line back to its source command
- the analyzer is a summary of string rules, not real understanding
- you should be able to say why each test message did or did not match

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

Break rule coverage:

```bash
./scripts/log_analyzer.sh "the service is unhealthy after rollout"
```

Expected result:

- `classification=unknown`

This is not proof that the message is safe.
It is proof that the rule set did not understand the wording.

## Explanation Lab

Answer:

1. why is Bash in AOIS after Linux?
2. what is the difference between command execution and automation?
3. why does `set -euo pipefail` matter?
4. why is string matching useful but brittle?
5. why is `unknown` safer than fake confidence?

## Defense Lab

Defend:

`using Bash for the first AOIS automation artifact is the right decision`

## Benchmark Lab

Score yourself from `1` to `5`:

- `5`: both scripts run, and I can explain safety flags, functions, arguments, branching, and rule brittleness.
- `4`: both scripts run, and only one explanation needs review.
- `3`: both scripts run, but I still need help diagnosing script failures.
- `2`: one script works, but the Bash behavior is mostly copied.
- `1`: script execution still feels random.

Minimum pass: `4`.
