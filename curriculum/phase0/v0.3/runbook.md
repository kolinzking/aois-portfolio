# v0.3 Runbook

## Purpose

Use this runbook when repository state feels confusing during AOIS work.

## Core Checks

### 1. Check current status

```bash
git status --short
```

### 2. Check recent history

```bash
git log --oneline --decorate -8
```

### 3. Inspect unstaged change details if needed

```bash
git diff
```

## If You Feel Lost In Git

Return to the three-area model:

- working tree
- staging area
- commit history

Most confusion comes from mixing those up.

## If A Commit Message Feels Weak

Ask:

- what changed?
- why did it change?
- would another engineer understand the milestone from the message alone?

## If Too Many Files Are Changing At Once

That is usually a sign to slow down and separate work into cleaner slices.

## Escalation Question

If the repo state feels hard to explain, do not commit yet.
Understanding comes before preservation.
