# v0.2 - Rule-Based Interpretation And Why It Stops Scaling

Estimated time: 2-3 focused hours

## What This Builds

You will build and analyze `scripts/log_analyzer.sh`, a small bash script that inspects one log message and labels it using exact keyword rules.

Current behavior:

- `OOMKilled` -> `Detected: Memory Issue`
- `CrashLoopBackOff` -> `Detected: Crash Issue`
- `5xx` -> `Detected: Server Error`
- no match -> `Detected: Unknown Issue`

This is the first AOIS interpretation layer.

In `v0.1`, AOIS learned to observe.
In `v0.2`, AOIS starts to interpret.

That change matters.

The system is no longer just showing a signal.
It is trying to assign meaning.

## Why This Exists

A machine health snapshot is useful, but it is still raw information.

For example:

- CPU high
- memory high
- disk high

Those are signals.
They are not yet conclusions.

As soon as a system begins to say things like:

- this is a memory issue
- this is a crash issue
- this is a server error

it has moved from visibility into interpretation.

The first instinct many engineers have is to use explicit rules.
That instinct is correct at first.

Rules are:

- simple
- fast
- easy to inspect
- deterministic

But they have a hard limit.

This version exists so you feel that limit directly instead of only hearing about it later.

## AOIS Connection

The AOIS path is now:

`log text -> string matching -> labeled issue`

That is progress.
But it is still brittle progress.

Later AOIS will become:

`log text -> model reasoning -> structured intelligence -> retrieval -> action`

`v0.2` is the bridge between:

- raw signals in `v0.1`
- AI analysis in `v1`

This version is important because it gives you a fair comparison point.
You need to understand what rules can do before you can understand why AI is stronger.

## Learning Goals

By the end of this version you should be able to:

- explain what `scripts/log_analyzer.sh` does line by line
- explain why exact keyword rules are useful but limited
- run the script on matching and non-matching inputs
- identify false confidence in rule-based systems
- explain the script at four system-explanation levels
- explain the main tools in this version using the four-layer rule
- articulate why `v1` is not just "fancier output" but a different capability class

## Prerequisites

Run these commands first.

```bash
pwd
ls scripts
sed -n '1,120p' scripts/log_analyzer.sh
```

You should confirm:

- you are in the AOIS repository
- `scripts/log_analyzer.sh` exists
- the script matches the current lesson

If it does not, stop and inspect the repo state before continuing.

## The System Model

A rule-based interpreter is a system that says:

if this pattern appears,
then assign this meaning.

That sounds trivial.
It is also foundational.

Many real systems start this way.

Examples:

- if HTTP status starts with `5` -> server-side error
- if log contains `OOMKilled` -> memory pressure likely involved
- if pod state is `CrashLoopBackOff` -> restart failure pattern exists

The strength of a rule system is determinism.
The weakness of a rule system is brittleness.

A deterministic rule system works only as long as the world keeps speaking the exact language the rules expect.

Production systems do not behave that politely.

## The Script

Current script:

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

This script reads one input string and checks whether it contains one of three known patterns.

That is all.

Do not underestimate it.
This is the first time AOIS claims to know what a log means.

## Tool Drill 1 - Bash Argument Input

The line:

```bash
message="${1:-}"
```

reads the first command-line argument.

### Plain English

It grabs the message you want the script to inspect.

### System Role

It is the input boundary for this first AOIS interpretation layer.

### Minimal Technical Definition

It assigns the first positional shell argument to a variable and falls back to an empty string if no argument is provided.

### Hands-on Proof

If this input line disappears, the script has nothing to analyze and all rule matching becomes meaningless.

## Tool Drill 2 - Bash Pattern Matching

The line:

```bash
[[ "$message" == *"OOMKilled"* ]]
```

checks whether a string contains a substring.

### Plain English

It asks: does this message contain this exact keyword?

### System Role

It is the decision mechanism for the rule engine.

### Minimal Technical Definition

It is a Bash conditional expression using glob-style wildcard pattern matching against a shell variable.

### Hands-on Proof

If the log says the same thing in different words, the rule fails even if the meaning is similar.

That is the central weakness of this version.

## Build

Make the script executable and run the baseline cases.

```bash
chmod +x scripts/log_analyzer.sh
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
./scripts/log_analyzer.sh "pod CrashLoopBackOff restarting"
./scripts/log_analyzer.sh "gateway returned 5xx"
./scripts/log_analyzer.sh "strange message with no match"
```

Expected outputs:

```text
Detected: Memory Issue
Detected: Crash Issue
Detected: Server Error
Detected: Unknown Issue
```

If that does not happen, stop and debug before reading further.

## What The Rules Actually Mean

### Rule 1 - `OOMKilled`

This is commonly associated with memory exhaustion.

The rule is useful because:

- it is specific
- it often indicates a known operational pattern

But even here, the script is not actually reasoning.
It is only recognizing a familiar token.

### Rule 2 - `CrashLoopBackOff`

This is associated with repeated restart failure in Kubernetes.

The rule is useful because:

- it maps a known orchestration state to a high-level interpretation

But again, the script does not know why the crash loop happened.
It only recognizes the label.

### Rule 3 - `5xx`

This is associated with server-side HTTP errors.

Useful, yes.
But limited.

A `503`, `500`, and `504` are not the same problem.
The rule collapses different failure classes into one bucket.

That is another important limit:

rule systems often compress meaning too aggressively.

## Ops Lab

Run these commands.

```bash
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
./scripts/log_analyzer.sh "gateway returned 503 upstream timeout"
./scripts/log_analyzer.sh "container exited after memory exhaustion"
./scripts/log_analyzer.sh "service unavailable after repeated restart"
```

Now answer:

1. Which of these did the script classify correctly?
2. Which messages express a similar idea but fail the rule?
3. Which message is too broad to trust as a full diagnosis?
4. What does the script know?
5. What does the script only appear to know?

This distinction matters.

## Break Lab

This version must be broken conceptually, not just mechanically.

Perform these tests.

### Case 1 - Variation break

```bash
./scripts/log_analyzer.sh "container terminated because it ran out of memory"
```

Expected output:

```text
Detected: Unknown Issue
```

That is the break.
The meaning is close to `OOMKilled`, but the wording changed.

### Case 2 - Over-broad match

```bash
./scripts/log_analyzer.sh "dashboard shows a 5xx spike after deploy"
```

Expected output:

```text
Detected: Server Error
```

But what exactly failed?
The script still does not know.

### Case 3 - Empty input

```bash
./scripts/log_analyzer.sh
```

Expected output:

```text
Detected: Unknown Issue
```

The script handles missing input safely, but not intelligently.

### Case 4 - Quoting failure

Run this intentionally wrong:

```bash
./scripts/log_analyzer.sh pod OOMKilled exit code 137
```

You may still get `Detected: Unknown Issue` because only the first word becomes `$1`.

That teaches a different lesson:

bad shell invocation can corrupt otherwise correct logic.

## Testing

Your current version passes if all of these are true:

1. the script runs successfully on the known inputs
2. the exact known keywords map to the intended labels
3. wording changes cause visible failure
4. you can explain why that failure is not a bug in Bash but a limit of the rule system
5. you can explain why this version is still worth building even though it is limited

## Common Mistakes

### Mistake 1 - Thinking keyword match equals understanding

Symptom:
You say the system "understands the log" because it returned a label.

Correction:
No.
It recognizes a known token and maps it to a preset label.
That is not the same as understanding novel language.

### Mistake 2 - Forgetting quotes around the input

Symptom:
The script behaves strangely on multi-word logs.

Correction:
Quote the whole log message so it arrives as one argument.

### Mistake 3 - Thinking deterministic means scalable

Symptom:
You assume the system is strong because it is predictable.

Correction:
Predictability is good.
But when the rule list grows, maintenance and coverage become serious problems.

### Mistake 4 - Treating `5xx` as one complete diagnosis

Symptom:
You accept `Server Error` as sufficient explanation.

Correction:
It is a coarse label, not a root cause.

## Troubleshooting

### Problem: `Permission denied`

Fix:

```bash
chmod +x scripts/log_analyzer.sh
```

### Problem: script outputs `Unknown Issue` for an apparently meaningful message

Diagnosis:
The wording likely did not match the exact patterns in the rules.

Fix:
Either:

- change the input to match the rule
- or add a new rule

But note the real lesson:
adding more rules is exactly what starts becoming unmanageable.

### Problem: output is wrong because the shell split the message

Diagnosis:
You likely forgot quotes around the input string.

Fix:

```bash
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
```

## Benchmark

Keep this benchmark simple.

Record:

- how fast the script feels: instant or delayed
- how many explicit patterns it currently supports: `3`
- how many test inputs fail when the wording changes: count them from your break lab

The benchmark insight here is not performance.
It is coverage.

Coverage is already becoming the real bottleneck.

## Architecture Defense

Why use Bash and rules here instead of jumping straight to AI?

Because you need to understand:

- what deterministic systems are good at
- where they fail
- why AI is not just a luxury layer but a different class of interpreter

Why is this still valuable if it is brittle?

Because a good engineer should be able to say:

- this is where rules work
- this is where rules stop working
- this is why the next design step is justified

That is much stronger than blindly replacing everything with a model.

## 4-Layer Tool Drill For This Version

You must be able to answer the four-layer rule for:

- Bash positional arguments
- Bash conditional matching
- shell quoting
- rule-based classifier

### Rule-based classifier example

1. Plain English
It looks for known patterns and assigns preset labels.

2. System Role
It is AOIS's first attempt at turning log text into an issue category.

3. Minimal Technical Definition
It is a deterministic interpreter that maps exact string patterns to fixed outputs.

4. Hands-on Proof
If the wording changes or the pattern list is incomplete, the classifier either misses the issue or collapses different issues into one crude label.

## 4-Level AOIS Explanation Drill

You must be able to explain `v0.2` like this.

### Level 1 - Simple English

I built a script that reads a log message and labels it using simple rules.

### Level 2 - Practical Explanation

It checks whether a log contains a few known keywords like `OOMKilled` or `5xx` and returns a basic issue label.

### Level 3 - Technical Explanation

It is a Bash script that reads one string argument and uses shell pattern matching inside `if` and `elif` branches to classify known log patterns.

### Level 4 - Engineer-Level Explanation

It is a deterministic, keyword-based interpreter that maps exact substrings in a log message to fixed output labels, which makes it fast and inspectable but brittle under wording variation, ambiguity, and scale.

## Failure Story

Record one real failure from your run or use one of these:

- forgot to quote the message and corrupted the input
- assumed `Unknown Issue` meant the system was broken when the real issue was rule coverage
- accepted `Server Error` as a diagnosis instead of a broad label
- confused pattern recognition with real understanding

Use the usual structure:

- Symptom:
- Root cause:
- Fix:
- Prevention:

## Mastery Checkpoint

Do not move on until you can answer all of these without guessing.

1. What new capability does `v0.2` add beyond `v0.1`?
2. Why is a rule-based classifier deterministic?
3. Why does deterministic not automatically mean scalable?
4. Why does `container terminated because it ran out of memory` fail this script?
5. Why is `5xx -> Server Error` useful but incomplete?
6. What role do shell quotes play in this version?
7. What is the difference between pattern recognition and understanding?
8. Explain `scripts/log_analyzer.sh` at all four system-explanation levels.
9. Explain one tool from this version using the four-layer rule.
10. Why does this version justify the move to AI in `v1`?

## Connection Forward

`v0.2` teaches the exact pain that `v1` will address.

The pain is not that rules are bad.
The pain is that rules break when language becomes varied, ambiguous, and operationally richer.

That is why AI enters AOIS later.

Not as decoration.
Not as hype.
As the next interpreter class.
