# v0.3 - Git As Engineering Memory And Portfolio Proof

Estimated time: 2-3 focused hours

## What This Builds

You will use Git deliberately inside AOIS instead of treating it as a background utility.

This version does not build a runtime feature like `sysinfo.sh` or `log_analyzer.sh`.
It builds something equally important:

an inspectable engineering history.

You will learn how AOIS progress becomes visible in:

- commits
- status checks
- staged changes
- commit messages
- repository history

That matters because AOIS is not only a system.
It is also a proof artifact.

## Why This Exists

If you build real work but leave no clean history behind, you lose three things:

- continuity
- reviewability
- evidence

For AOIS, Git is not optional bookkeeping.
It is part of the learning system.

Without disciplined version control:

- you cannot show what changed and why
- you cannot recover cleanly from mistakes
- you cannot defend the sequence of your engineering decisions
- your portfolio becomes much weaker

This version exists to make Git part of the AOIS operating model from the beginning.

## AOIS Connection

In `v0.1`, AOIS observed.
In `v0.2`, AOIS interpreted with rules.
In `v0.3`, AOIS gains a durable development memory.

The system path now includes:

`working tree -> staged change -> commit -> reviewable system history`

That path matters later when AOIS becomes:

- larger
- multi-service
- infrastructure-backed
- agentic
- more failure-prone

As the system grows, clean history becomes more valuable, not less.

## Learning Goals

By the end of this version you should be able to:

- explain the difference between working tree, staging area, and commit history
- use `git status`, `git add`, `git commit`, and `git log` with confidence
- explain why a commit is a snapshot, not just a text diff in your head
- identify what makes a commit useful for future review
- explain why Git history is part of your AOIS portfolio proof
- explain Git at the four-layer tool level
- explain `v0.3` at the four system-explanation levels

## Prerequisites

Run these commands first.

```bash
pwd
git status --short
git log --oneline -5
```

You should confirm:

- you are in the AOIS repository
- Git is working normally
- the repository already has commits

If Git is not initialized or the repo is not available, stop and diagnose that first.

## The Git Model

At minimum, you must understand three areas.

### 1. Working Tree

This is what is currently on disk.
These are the files you are actively editing.

### 2. Staging Area

This is the set of changes you are preparing for the next commit.

### 3. Commit History

This is the durable record of saved snapshots.

That means a commit is not:

- a vague checkpoint in your mind
- a random "save point"
- just a message

A commit is a concrete snapshot of tracked content.

If your mental model of Git is weak here, everything later becomes confusing.

## Tool Drill 1 - `git status`

Run:

```bash
git status --short
```

### Plain English

It tells you what changed and what Git currently thinks about those changes.

### System Role

It is the main AOIS checkpoint command for understanding the state of your work before committing.

### Minimal Technical Definition

It reports the repository status, including tracked modifications, staged changes, and untracked files.

### Hands-on Proof

If you stop checking status, you will eventually commit the wrong files, miss important changes, or lose clarity about what state the repo is in.

## Tool Drill 2 - `git add`

Run this on a file you understand, not blindly.

### Plain English

It selects changes for the next commit.

### System Role

It lets AOIS version progress in deliberate slices instead of dumping unrelated changes together.

### Minimal Technical Definition

It updates the staging area with content from the working tree.

### Hands-on Proof

Without staging discipline, your commit history becomes noisy, mixed, and much harder to review or explain later.

## Tool Drill 3 - `git commit`

### Plain English

It saves a named snapshot of the staged work.

### System Role

It turns AOIS progress into durable, reviewable history.

### Minimal Technical Definition

It writes the staged snapshot into the repository history with metadata and a commit message.

### Hands-on Proof

If you never commit cleanly, the repo stops functioning as curriculum evidence and becomes just a folder with files.

## Build

Inspect the repository state first.

Run:

```bash
git status --short
git log --oneline -8
```

Study what you see.

Questions:

1. Which files are modified?
2. Which changes are already safely in history?
3. What story do the recent commit messages tell?

This is already part of the lesson.
The repo is not separate from the curriculum.
The repo is one of the teaching surfaces.

## Commit Quality

A useful commit should be:

- small enough to understand
- real enough to matter
- narrow enough to review
- named clearly enough to find later

Bad commit habits:

- mixing unrelated changes
- vague messages like `update stuff`
- giant commits that hide many concepts at once
- committing without understanding what is staged

Good commit habits:

- one version or milestone at a time
- one coherent reason for the change
- message that states what was added or changed
- quick review before commit

## Ops Lab

Run these commands:

```bash
git status --short
git diff -- curriculum/phase0/v0.2/notes.md || true
git log --oneline --decorate -8
```

Now answer:

1. What is the difference between `git status` and `git log`?
2. What is the difference between uncommitted work and committed history?
3. Why is the commit log part of your AOIS portfolio?
4. If someone interviews you using only your repo, what should they be able to infer from the history?

## Break Lab

This version should include controlled Git mistakes.

### Case 1 - Status blindness

Imagine you edit several files and commit without checking `git status`.

What can go wrong?

Write down at least three risks.

Then run:

```bash
git status --short
```

The lesson is simple:
status ignorance creates commit confusion.

### Case 2 - Mixed commit thinking

Suppose you changed:

- a curriculum note
- a shell script
- a README explanation

Should those always be one commit?

No.

Explain why.

### Case 3 - Message failure

Which message is better?

- `fix`
- `curriculum: author v0.2 lesson pack`

Explain why the second is stronger.

This is not about style points.
It is about recoverability and reviewability.

## Testing

This version passes if all of these are true:

1. you can explain the three Git areas clearly
2. you can interpret `git status --short`
3. you can explain what the recent AOIS commits represent
4. you understand why a clean history is part of the curriculum itself
5. you can distinguish a useful commit from a noisy one

## Common Mistakes

### Mistake 1 - Thinking Git is only backup

Symptom:
You treat Git like cloud storage for code.

Correction:
Git is versioned engineering memory.
In AOIS, it is part of the learning and proof system.

### Mistake 2 - Thinking commits are diffs in isolation

Symptom:
You talk about commits only as lines added or removed.

Correction:
A commit is a snapshot of the staged repository state.
That is the mental model you need.

### Mistake 3 - Committing without reading status

Symptom:
You are surprised by what ended up in a commit.

Correction:
Always inspect status before and after staging.

### Mistake 4 - Writing low-information commit messages

Symptom:
Your history becomes unreadable later.

Correction:
Name the milestone clearly and specifically.

## Troubleshooting

### Problem: `git status` shows files you did not expect

Diagnosis:
You may have edited more files than you realized, or scaffolded files may still exist nearby.

Fix:
Read the output carefully.
Do not stage blindly.

### Problem: commit history feels noisy

Diagnosis:
The repository may already include commits from setup, scaffolding, and curriculum corrections.

Fix:
That is normal.
The lesson is to keep future commits clean, not to pretend history starts from zero.

### Problem: you cannot explain what a commit actually is

Diagnosis:
Your mental model is still too vague.

Fix:
Return to the three-area model:

- working tree
- staging area
- commit history

## Benchmark

This benchmark is qualitative.

Record:

- number of recent commits you can explain confidently
- whether the recent commit messages are readable at a glance
- whether the history tells a coherent curriculum story

The benchmark here is history clarity, not speed.

## Architecture Defense

Why teach Git this early?

Because every later AOIS phase depends on disciplined iteration.

If Git is weak:

- infrastructure work becomes harder to review
- debugging becomes harder to trace historically
- the portfolio becomes less credible

Why is Git inside AOIS and not outside it?

Because the curriculum is not only about building code.
It is about building a system with evidence.
Git is the evidence layer.

## 4-Layer Tool Drill For This Version

You must be able to answer the four-layer rule for:

- `git status`
- `git add`
- `git commit`
- `git log`
- commit history itself

### `git log` example

1. Plain English
It shows the saved history of the repository.

2. System Role
It lets AOIS progress be inspected as a sequence of engineering decisions.

3. Minimal Technical Definition
It displays commit objects from repository history, including commit messages and metadata.

4. Hands-on Proof
If the log is unreadable or incoherent, the portfolio loses explanatory power even if the code itself exists.

## 4-Level AOIS Explanation Drill

You must be able to explain `v0.3` like this.

### Level 1 - Simple English

I learned how to save AOIS progress in a clean, reviewable way.

### Level 2 - Practical Explanation

This version teaches me how to inspect changes, stage the right files, and create useful commits so the repository becomes a clear record of progress.

### Level 3 - Technical Explanation

It introduces the Git working tree, staging area, and commit history, and uses the AOIS repo itself as the object of version control practice.

### Level 4 - Engineer-Level Explanation

It turns the AOIS repository into versioned engineering memory by enforcing disciplined use of `git status`, `git add`, `git commit`, and `git log`, so each milestone becomes a reviewable historical snapshot rather than an unstructured pile of edits.

## Failure Story

Record one real failure from your run or use one of these:

- committed without reading status and included the wrong file
- confused working tree changes with staged changes
- assumed a vague commit message was good enough
- underestimated how much a clean Git history matters for the portfolio

Use the usual structure:

- Symptom:
- Root cause:
- Fix:
- Prevention:

## Mastery Checkpoint

Do not move on until you can answer all of these without guessing.

1. What are the three main Git areas you need to understand?
2. What does `git status --short` tell you that `git log` does not?
3. Why is a commit a snapshot rather than just a diff in your head?
4. Why is Git part of AOIS itself rather than just a side tool?
5. What makes a commit message strong?
6. What goes wrong when unrelated changes are committed together?
7. Why does clean history matter for interviews and portfolio proof?
8. Explain Git at the four-layer level for one command in this version.
9. Explain `v0.3` at all four system-explanation levels.
10. How does this version make later infrastructure and agent work safer?

## Connection Forward

`v0.3` gives AOIS disciplined engineering memory.

That matters immediately in `v0.4`, where networking and HTTP work start to create more moving parts, more commands, and more opportunities for confusion.

As AOIS grows, clean Git history stops being nice to have.
It becomes operationally important.
