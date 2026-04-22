# v0.2 Notes

## Goal

Show the limit of rule-based systems.

This version is not about deep Bash.
It is about seeing why simple `if` rules stop working as systems get more complex.

## Why This Version Exists

In `v0.1`, the system showed raw information:

- CPU
- memory
- disk

But raw information is not the same as understanding.

If a system prints:

- CPU: `85%`
- memory: `90%`
- disk: `70%`

it still does not answer:

- is this dangerous
- what caused it
- what should happen next

One common first attempt is to build rigid rules.

Example:

```text
if CPU > 80 -> HIGH CPU
```

That works for a small case, but it does not scale well.

## Build

This version builds:

- `scripts/log_analyzer.sh`

## What The Script Does

The script takes one log message and checks for simple keywords.

Current rules:

- `OOMKilled` -> `Detected: Memory Issue`
- `CrashLoopBackOff` -> `Detected: Crash Issue`
- `5xx` -> `Detected: Server Error`
- no match -> `Detected: Unknown Issue`

## Full Script

```bash
#!/usr/bin/env bash

message="${1:-}"

if [[ "$message" == *"OOMKilled"* ]]; then
  echo "Detected: Memory Issue"
elif [[ "$message" == *"CrashLoopBackOff"* ]]; then
  echo "Detected: Crash Issue"
elif [[ "$message" == *"5xx"* ]]; then
  echo "Detected: Server Error"
else
  echo "Detected: Unknown Issue"
fi
```

## Full Script, Commented

```bash
#!/usr/bin/env bash

# Read the first command-line argument.
# If no argument is provided, use an empty string.
message="${1:-}"

# Check for the memory-related log keyword.
if [[ "$message" == *"OOMKilled"* ]]; then
  echo "Detected: Memory Issue"

# Check for the crash-loop keyword.
elif [[ "$message" == *"CrashLoopBackOff"* ]]; then
  echo "Detected: Crash Issue"

# Check for a simple server error pattern.
elif [[ "$message" == *"5xx"* ]]; then
  echo "Detected: Server Error"

# If nothing matched, return the fallback result.
else
  echo "Detected: Unknown Issue"
fi
```

## Commands

Build and run commands:

```bash
chmod +x scripts/log_analyzer.sh
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
./scripts/log_analyzer.sh "pod CrashLoopBackOff restarting"
./scripts/log_analyzer.sh "gateway returned 5xx"
./scripts/log_analyzer.sh "strange message with no match"
```

## Expected Behavior

Example input:

```text
pod OOMKilled exit code 137
```

Expected output:

```text
Detected: Memory Issue
```

## What You Should Notice

The script works, but only in a narrow way.

It depends on exact text patterns.

It does not:

- explain the issue
- understand variations well
- infer meaning from unfamiliar wording
- generalize beyond the rules you wrote

## Key Insight

Rule-based systems break under complexity.

As logs become more varied, the rule list grows:

- more keywords
- more exceptions
- more edge cases
- more maintenance

That is the point of this version.

You are supposed to see the limit.

## Beginner Bash Notes

What this script teaches at the Bash level:

- how to read one argument with `$1`
- how to store it in a variable
- how to use `if`, `elif`, and `else`
- how to print output with `echo`

That is enough Bash for this step.

## Troubleshooting

Use this section to record real issues only.

- Issue:
- Cause:
- Fix:

Common mistakes:

- forgetting quotes around the log message
- forgetting `chmod +x`
- expecting the script to understand wording it was not explicitly told to match

## Mastery Check

Be able to explain:

- what the script checks
- why keyword matching is limited
- why rule-based systems become hard to maintain
- why AI is needed after this point

## Takeaway

The correct conclusion from `v0.2` is:

`Rule-based systems break under complexity.`

If that insight is clear, this version succeeded.
