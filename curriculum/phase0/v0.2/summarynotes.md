# v0.2 Summary Notes

## What You Built

You built `scripts/log_analyzer.sh`, a first-pass AOIS rule engine that labels log messages by exact string matches.

## What You Actually Learned

- rule systems are attractive because they are cheap, fast, and deterministic
- exact-match logic fails as soon as real language varies
- interpretation is harder than observation because the system now claims meaning
- brittle automation can look correct on the happy path and still be weak in production

## What Matters Most

The biggest lesson in `v0.2` is not shell syntax.
It is the limit of deterministic interpretation when the input language is messy.

That limit is why `v1` will matter later.

## Commands Worth Remembering

```bash
./scripts/log_analyzer.sh "pod OOMKilled exit code 137"
./scripts/log_analyzer.sh "payment service restarted repeatedly"
bash -x scripts/log_analyzer.sh "gateway returned 5xx"
```

## Core Limitation

`v0.2` can label only what it has already been taught to recognize exactly.
It cannot generalize, reason, or explain.
