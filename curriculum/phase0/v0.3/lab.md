# v0.3 Lab

Authoring status: authored

## Build Lab

Create a tiny Git checkpoint file:

```bash
mkdir -p .aois-state
printf "v0.3 git discipline checkpoint\n" > .aois-state/v0.3-git-check.txt
```

Inspect it:

```bash
git status --short
git diff -- .aois-state/v0.3-git-check.txt
```

Stage only after inspection:

```bash
git add .aois-state/v0.3-git-check.txt
git diff --cached -- .aois-state/v0.3-git-check.txt
```

Commit with a meaningful message:

```bash
git commit -m "learning: record v0.3 git checkpoint"
```

Success state:

- the checkpoint file is committed
- the commit message explains intent
- unrelated files were not included

## Ops Lab

Run:

```bash
git status --short
git log --oneline -5
git diff --stat HEAD~1..HEAD
```

Expected learning:

- repo state is operational evidence
- commit history is system memory
- a commit can be inspected after it is made

## Break Lab

Create an untracked scratch file:

```bash
printf "temporary thought\n" > .aois-state/git-scratch.txt
git status --short
```

Expected symptom:

- Git reports `?? .aois-state/git-scratch.txt`

Recover:

```bash
rm -f .aois-state/git-scratch.txt
git status --short
```

Explain:

- why untracked does not mean broken
- why you should inspect before staging
- why scratch files should not be committed accidentally

## Explanation Lab

Answer:

1. What is the working tree?
2. What is the staging area?
3. What is a commit?
4. Why does AOIS need meaningful history?
5. Why is `git add -A` dangerous before inspection?

## Defense Lab

Defend:

`Git is part of the AOIS product, not just a backup tool.`

## Benchmark Lab

Score yourself from `1` to `5`:

- `5`: I can inspect, stage, commit, and explain Git history without hints.
- `4`: I can complete the workflow but one concept needs review.
- `3`: I can run the commands but need help deciding what belongs in a commit.
- `2`: I can make commits but cannot explain the workflow.
- `1`: Git still feels like magic or danger.

Minimum pass: `4`.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.3 - Git As Engineering Memory](notes.md)
- Next: [v0.3 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
