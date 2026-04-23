# v0.2 Introduction

`v0.2` is where AOIS starts claiming meaning.

In `v0.1`, the system could say:

- CPU is high
- memory is tight
- disk is filling

In `v0.2`, it tries something more dangerous:

- this is a memory issue
- this is a crash issue
- this is a server issue

That jump from observation to interpretation is the whole lesson.

## What You Will Build

You will build `scripts/log_analyzer.sh`, a rule-based classifier that maps exact log patterns to issue labels.

It is intentionally simple.
It is also intentionally brittle.

## Why This Version Exists

The wrong way to meet AI is as a magic replacement for things you never understood.

The right way is:

1. build the deterministic version first
2. feel where it breaks
3. then upgrade to a model-based system for real reasons

That is what `v0.2` is doing.

## How To Use This Pack

If you are in self-paced mode:

1. start with [notes.md](notes.md)
2. run [lab.md](lab.md)
3. keep [runbook.md](runbook.md) nearby for the shell patterns
4. close with [summarynotes.md](summarynotes.md) and [looking-forward.md](looking-forward.md)
