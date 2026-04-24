# v0.5 - Python Core For AOIS Logic

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: lightweight, standard-library only

## What This Builds

This version moves AOIS from shell-only automation into maintainable Python logic.

You will build:

- `app/models.py` with typed incident and result models
- `app/analysis.py` with deterministic incident analysis functions
- `app/config.py` with small environment-based settings
- `examples/analyze_incident.py` as a terminal entrypoint

No external dependencies are required in this version.

## Why This Exists

Bash is useful for operating the system.
Python is better for application logic.

AOIS needs Python before FastAPI, LLM integration, persistence, evaluation, and agents because those layers need:

- structured data
- functions
- modules
- validation
- exceptions
- testable behavior
- readable application boundaries

This version keeps the analysis deterministic on purpose.
AI comes later.

## AOIS Connection

The AOIS path is now:

`signal -> Python model -> deterministic analysis -> structured result`

This is the first version where AOIS has an application logic layer.

`v0.6` will expose this logic through FastAPI.
`v1` will eventually replace or augment deterministic analysis with structured AI output.

## Learning Goals

By the end of this version you should be able to:

- explain why Python belongs after Bash
- run Python modules from the repo
- understand functions, dataclasses, enums, and type hints
- validate simple inputs
- raise and interpret exceptions
- distinguish raw strings from structured models
- run a small CLI entrypoint
- explain why deterministic rules remain limited

## Prerequisites

You should have completed:

- `v0.1` Linux inspection
- `v0.2` Bash automation
- `v0.3` Git discipline
- `v0.4` HTTP inspection

Required checks:

```bash
python3 --version
python3 -m py_compile app/models.py app/analysis.py app/config.py examples/analyze_incident.py
```

Expected behavior:

- Python is available
- compilation succeeds with no syntax errors

## Core Concepts

## Module

A Python module is a `.py` file that can hold functions, classes, and constants.

In this version:

- `app/models.py` defines data shapes
- `app/analysis.py` defines analysis behavior
- `app/config.py` defines settings
- `examples/analyze_incident.py` gives a command-line entrypoint

## Function

A function packages behavior behind a name.

Example:

```python
def normalize_message(message: str) -> str:
    return " ".join(message.lower().strip().split())
```

The function takes a string and returns a normalized string.

## Type Hint

A type hint states what kind of value code expects.

Example:

```python
def normalize_message(message: str) -> str:
```

This says:

- `message` should be a string
- the function returns a string

Type hints do not replace runtime validation.
They make code easier to read, check, and maintain.

## Dataclass

A dataclass is a concise way to define structured data.

AOIS uses dataclasses here so an incident is not just a loose string.

Example:

```python
IncidentInput(message="gateway returned 5xx", source="manual")
```

## Enum

An enum defines a controlled vocabulary.

AOIS uses `Severity` so severity values are explicit:

- `low`
- `medium`
- `high`
- `unknown`

## Exception

An exception reports invalid state or failure.

In this version, an empty incident message raises `ValueError`.
That is better than quietly analyzing meaningless input.

## Build

Create or replace `app/models.py`, `app/analysis.py`, `app/config.py`, and `examples/analyze_incident.py` with the implementation in the repository.

Then run:

```bash
python3 -m py_compile app/models.py app/analysis.py app/config.py examples/analyze_incident.py
```

Run example analyses:

```bash
python3 examples/analyze_incident.py "gateway returned 5xx after deploy"
python3 examples/analyze_incident.py "pod OOMKilled exit code 137"
python3 examples/analyze_incident.py "strange message with no match"
```

Expected output shape:

```text
category=service-error
severity=medium
confidence=0.70
summary=...
recommended_action=...
```

Unknown messages should return:

```text
category=unknown
severity=unknown
confidence=0.20
```

## Ops Lab

Run:

```bash
python3 examples/analyze_incident.py "permission denied reading /var/log/app.log"
python3 examples/analyze_incident.py "pod CrashLoopBackOff restarting"
```

Questions:

1. Which file defines the input model?
2. Which file contains the classification rules?
3. Which field tells you how confident the deterministic rule is?
4. Why is `unknown` still a valid result?
5. What did Python add that Bash did not?

Answer key:

1. `app/models.py`
2. `app/analysis.py`
3. `confidence`
4. It honestly records that no deterministic rule matched.
5. Structured models, typed functions, reusable modules, and richer validation.

## Break Lab

Do not skip this.

### Option A - Empty message

Run:

```bash
python3 examples/analyze_incident.py ""
```

Expected symptom:

- Python raises `ValueError`
- the message says the incident message must not be empty

Lesson:

- validation blocks meaningless input

False conclusion this prevents:

- "the analyzer can interpret anything" when the input is invalid

### Option B - Unknown message

Run:

```bash
python3 examples/analyze_incident.py "the system feels odd"
```

Expected result:

- `category=unknown`
- `severity=unknown`

Lesson:

- deterministic Python rules are still not understanding

False conclusion this prevents:

- "Python made the rules intelligent"

## Testing

The version passes when:

1. Python files compile
2. known incident examples produce expected categories
3. unknown examples remain unknown
4. empty input fails clearly
5. you can explain models, functions, type hints, enums, and exceptions
6. you can explain why Python is the bridge to FastAPI

## Common Mistakes

- treating type hints as runtime validation
- swallowing invalid input instead of raising errors
- keeping all logic in one file
- returning loose strings when structured results are needed
- assuming Python rules understand meaning better than Bash rules
- adding dependencies before the standard-library version is understood

## Troubleshooting

If imports fail:

- run commands from the repo root
- confirm `app/__init__.py` exists
- use `python3 examples/analyze_incident.py "..."`

If compilation fails:

```bash
python3 -m py_compile app/models.py app/analysis.py app/config.py examples/analyze_incident.py
```

Read the file path and line number in the error.

If the analyzer returns `unknown`:

- inspect the message wording
- inspect the rules in `app/analysis.py`
- do not assume the incident is safe

## Benchmark

Measure:

- can all Python files compile?
- can you run three examples in under 30 seconds?
- can you explain one result field by field?
- can you trigger and explain the empty-message failure?
- can you say what Python improved over Bash?

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can run, explain, break, and extend the Python layer without hints. |
| 4/5 | You can complete the lab but one concept needs review. |
| 3/5 | You can run examples but struggle to explain structure. |
| 2/5 | Code runs, but models/functions/exceptions are unclear. |
| 1/5 | Python still feels like copied text. |

Minimum pass: `4/5`.

## Architecture Defense

Why use Python here instead of more Bash?

Because AOIS needs structured application logic.
Python is better for models, validation, functions, tests, APIs, and later AI integration.

Why avoid external dependencies in this version?

Because the core Python model should be understood first.
Dependencies like Pydantic and FastAPI are useful later, but they should not hide fundamentals.

Why keep deterministic rules if they are limited?

Because they create a baseline.
Later AI behavior can be compared against simple deterministic behavior.

## 4-Layer Tool Drill

Tool: Python dataclass

1. Plain English
A dataclass packages related values into a clear object.

2. System Role
It gives AOIS structured incident and result data before API and database layers arrive.

3. Minimal Technical Definition
A dataclass is a Python class generated from annotated fields, with methods like initialization created automatically.

4. Hands-on Proof
If incident data stays as loose strings, validation and structured response behavior become harder to reason about.

## 4-Level System Explanation Drill

1. Simple English
I moved AOIS logic from scripts into Python.

2. Practical Explanation
I can run a Python analyzer that turns incident messages into structured categories, severities, summaries, actions, and confidence values.

3. Technical Explanation
This version uses Python modules, dataclasses, enums, type hints, functions, and exceptions to create a deterministic application logic layer.

4. Engineer-Level Explanation
AOIS now has a maintainable Python domain layer that separates data models from analysis behavior, validates invalid input, and creates structured outputs that can later be exposed through FastAPI, persisted in Postgres, evaluated, or replaced with AI-backed reasoning.

## Failure Story

Representative failure:

- Symptom: an empty incident message crashed the CLI with `ValueError`
- Root cause: validation rejected meaningless input
- Fix: pass a non-empty message
- Prevention: validate inputs at system boundaries
- What this taught me: failing clearly is better than producing fake analysis

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v0.5` solve in AOIS?
2. Why move from Bash to Python?
3. What is a Python module?
4. What is a function?
5. What is a type hint?
6. What is a dataclass?
7. What is an enum?
8. Why does empty input raise an exception?
9. Why is `unknown` still important?
10. How does this prepare for FastAPI?
11. Explain dataclasses using the 4-layer tool rule.
12. Explain `v0.5` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v0.5` solve in AOIS?

It gives AOIS a maintainable Python logic layer.
The system can now represent incidents and analysis results as structured data instead of only shell text.

2. Why move from Bash to Python?

Bash is good for command automation.
Python is better for application logic, structured data, validation, tests, APIs, and later AI integration.

3. What is a Python module?

A module is a `.py` file that contains reusable Python code such as functions, classes, and constants.

4. What is a function?

A function is a named block of reusable behavior that accepts inputs and returns or produces outputs.

5. What is a type hint?

A type hint describes the expected type of a value.
It improves readability and tooling, but it does not automatically replace runtime validation.

6. What is a dataclass?

A dataclass is a concise way to define structured data objects from annotated fields.
AOIS uses it to represent incident inputs and analysis results.

7. What is an enum?

An enum defines a controlled set of named values.
AOIS uses `Severity` to prevent random severity strings from spreading through the code.

8. Why does empty input raise an exception?

An empty incident message cannot be meaningfully analyzed.
Raising `ValueError` makes the bad input visible instead of returning fake analysis.

9. Why is `unknown` still important?

`unknown` is honest.
It means no deterministic rule matched, so the raw signal should be preserved or escalated instead of pretending the system understands it.

10. How does this prepare for FastAPI?

FastAPI will need request models, response models, validation, and callable analysis functions.
This version creates those foundations before adding an HTTP framework.

11. Explain dataclasses using the 4-layer tool rule.

- Plain English: a dataclass groups related values.
- System Role: it gives AOIS structured data for incidents and analysis.
- Minimal Technical Definition: it is a Python class with generated initialization and field handling from annotations.
- Hands-on Proof: without structured models, AOIS returns loose strings that are harder to validate, test, expose through APIs, or persist.

12. Explain `v0.5` using the 4-level system explanation rule.

- Simple English: I learned how to write AOIS logic in Python.
- Practical explanation: I can run a Python analyzer that returns structured incident analysis.
- Technical explanation: `v0.5` uses modules, dataclasses, enums, functions, type hints, and exceptions.
- Engineer-level explanation: AOIS now has a Python domain layer that can later be exposed through FastAPI, persisted in Postgres, tested, evaluated, and upgraded with AI-backed structured reasoning.

## Connection Forward

`v0.5` teaches the fifth AOIS habit:

`structure the logic`

`v0.6` exposes this Python logic through a FastAPI service boundary.

## Source Notes

This version uses Python standard-library behavior.
No fast-moving external source is required for the core lesson.

If this version later adds Pydantic, uv, ruff, mypy, pytest, or async libraries, add source notes for those tools and their current behavior.
