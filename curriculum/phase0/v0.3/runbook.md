# v0.3 Runbook

Authoring status: authored

## Purpose

Use this runbook when Git state looks confusing.

## Primary Checks

Run:

```bash
git status --short
git diff
git diff --cached
git log --oneline -5
```

Interpretation:

- `git status --short` shows changed and untracked files
- `git diff` shows unstaged changes
- `git diff --cached` shows staged changes
- `git log --oneline -5` shows recent history

## Recovery Steps

If a file is untracked:

1. inspect the file
2. decide whether it belongs in the repo
3. stage it only if it belongs
4. remove it only if it is scratch or generated

If too much is staged:

```bash
git restore --staged <path>
```

If the commit message is vague and not committed yet:

```bash
git commit -m "domain: specific intent"
```

If you are unsure:

- stop
- read `git status --short`
- read the diff
- name each file's purpose
- commit only one coherent decision

## Do Not Do This

Do not use destructive commands like:

```bash
git reset --hard
```

unless a live teacher explicitly approves the exact recovery.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.3 Lab](lab.md)
- Next: [v0.3 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
