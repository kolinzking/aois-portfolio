# v0.5 - Python Foundations For The AOIS Service Layer

Estimated time: 3-4 focused hours

## What This Builds

You build the first reusable Python substrate for AOIS:

- [requirements.txt](../../../requirements.txt)
- [.env.example](../../../.env.example)
- [app/config.py](../../../app/config.py)
- [app/models.py](../../../app/models.py)

## Why This Exists

Shell scripts are good for inspection and small automation.
They are not the right home for typed request models, reusable config loading, or an API service that will grow.

`v0.5` exists so later AOIS code has:

- structured inputs
- explicit config
- importable modules
- predictable project shape

## AOIS Connection

The system path becomes:

`env file -> config loader -> typed model -> service code`

That is the minimum backbone for `v0.6` and every Python-based phase after it.

## Learning Goals

By the end of this version you should be able to:

- explain what `requirements.txt` is doing in this repo
- explain why `.env.example` exists even before real secrets are used
- read and modify Pydantic models confidently
- explain the difference between config loading and request validation
- defend why AOIS now needs Python modules instead of only scripts

## Prerequisites

Run:

```bash
python3 --version
sed -n '1,120p' requirements.txt
sed -n '1,200p' app/config.py
sed -n '1,220p' app/models.py
```

Expected:

- Python is installed
- you see the declared dependencies
- you see environment loading
- you see typed AOIS models

## Core Concepts

### `requirements.txt`

The pinned dependency list that defines the Python environment AOIS expects.

### `.env.example`

A safe template for expected configuration keys without real secrets.

### Config loading

The code that reads environment variables and turns them into usable application settings.

### Pydantic models

Typed, validated structures for data entering or leaving AOIS.

## Build

Inspect the Python foundation files:

```bash
sed -n '1,200p' app/config.py
sed -n '1,220p' app/models.py
```

What to notice:

- config and models live in separate modules
- environment loading happens once, not everywhere
- request/response shape is explicit

## Ops Lab

Run:

```bash
python3 - <<'PY'
from app.config import get_settings
from app.models import AnalyzeRequest

print(get_settings())
print(AnalyzeRequest(log="pod OOMKilled exit code 137"))
PY
```

Expected behavior:

- settings print as a small dictionary
- the request model prints a validated object

Answer key:

- `get_settings()` handles environment lookup
- `AnalyzeRequest` handles input shape and validation

## Break Lab

Run:

```bash
python3 - <<'PY'
from app.models import AnalyzeRequest
AnalyzeRequest(log="bad")
PY
```

Expected symptom:

- Pydantic raises a validation error because the log is too short

Lesson:

- validation should fail early and loudly
- typed models are part of reliability, not just developer convenience

## Testing

Quick checks:

```bash
python3 -m py_compile app/config.py app/models.py app/analysis.py app/main.py
python3 - <<'PY'
from app.models import Severity
print([s.value for s in Severity])
PY
```

Expected:

- no syntax errors
- severities print `['P1', 'P2', 'P3', 'P4']`

## Common Mistakes

### Mixing config and business logic

Do not call `os.getenv()` everywhere in the codebase.
Centralize config reading.

### Treating types as comments

If the model is not validated, the type hint alone does not protect you.

### Putting real secrets in `.env.example`

Example files document shape, not real credentials.

## Troubleshooting

If imports fail:

```bash
pwd
find app -maxdepth 1 -type f | sort
```

If `.env` values do not appear:

- confirm the file is named `.env`
- compare it to `.env.example`
- inspect `app/config.py`

## Benchmark

Measure validation speed roughly:

```bash
python3 - <<'PY'
import time
from app.models import AnalyzeRequest

start = time.perf_counter()
for _ in range(1000):
    AnalyzeRequest(log="pod OOMKilled exit code 137")
print(round(time.perf_counter() - start, 4))
PY
```

The exact number does not matter.
The lesson is that validation has a real but small cost, and that cost buys safer service boundaries.

## Architecture Defense

Why Pydantic here:

- explicit contracts
- validation built in
- later FastAPI integration is natural

Why not plain dictionaries:

- weaker guarantees
- easier to drift
- harder to explain and defend

## 4-Layer Tool Drill

### Pydantic

1. Plain English
It checks that incoming data has the shape AOIS expects.

2. System Role
It is the contract layer for requests and responses.

3. Minimal Technical Definition
It is a Python data-validation library that turns typed classes into validated runtime objects.

4. Hands-on Proof
Without it, short or malformed logs pass through silently until they break later logic.

## 4-Level System Explanation Drill

1. Simple English
`v0.5` gives AOIS typed Python building blocks.

2. Practical Explanation
It creates config and model files so the service can load settings and validate inputs cleanly.

3. Technical Explanation
It introduces pinned dependencies, dotenv-backed config loading, and Pydantic models for request/response schemas.

4. Engineer-Level Explanation
`v0.5` establishes the Python substrate that decouples environment loading from runtime logic and formalizes service contracts before FastAPI is introduced.

## Failure Story

The representative failure is assuming a type hint alone protects input quality.
It does not.
Runtime validation is what turns a declared schema into an enforced boundary.

## Mastery Checkpoint

You are ready to leave `v0.5` when you can:

1. explain why `requirements.txt` belongs in the repo now
2. explain what `.env.example` is for
3. create and validate an `AnalyzeRequest`
4. explain why config loading and request validation are different concerns
5. defend why AOIS needed to leave pure shell at this point

## Connection Forward

`v0.6` uses these models and settings in a real FastAPI service.
