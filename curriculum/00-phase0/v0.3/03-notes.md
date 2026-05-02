# v0.3 - Git As Engineering Memory

Estimated time: 6-8 focused hours

Authoring status: authored

## What This Builds

This version builds Git discipline for AOIS.

By the end, the repo should no longer feel like a folder of files.
It should feel like an inspectable engineering memory.

You will practice:

- checking working tree state
- reading diffs before staging
- staging intentional changes
- writing meaningful commits
- inspecting history
- explaining why Git history is part of the product

## Why This Exists

AOIS is a long-running system.
It will move from shell scripts to APIs, model routing, databases, infrastructure, observability, agents, and governance.

Without Git discipline, that growth becomes untrustworthy.

Git answers operational questions like:

- what changed?
- when did it change?
- why did it change?
- which files were part of the same decision?
- can I review the system's evolution?

In serious engineering, history is not decoration.
It is evidence.

## AOIS Connection

The AOIS path is now:

`machine -> shell commands -> Bash scripts -> Git history -> inspectable system evolution`

`v0.1` gave you direct machine visibility.
`v0.2` gave you repeatable automation.
`v0.3` makes that work durable and reviewable.

## Learning Goals

By the end of this version you should be able to:

- explain working tree, staging area, commit, and history in plain English
- use `git status --short` to identify repo state quickly
- use `git diff` before staging changes
- use `git add` intentionally instead of blindly
- use `git commit` with a meaningful message
- use `git log --oneline` to inspect recent history
- explain why commits should be small and coherent
- identify the risk of mixing unrelated changes
- explain why Git is foundational to later infrastructure and AI system work

## Prerequisites

You should have completed:

- `v0.1` Linux direct inspection
- `v0.2` Bash automation

You should already be able to run:

```bash
pwd
ls -la
git status --short
```

Expected behavior:

- `pwd` shows you are inside the AOIS repo
- `ls -la` shows `.git`
- `git status --short` shows either a clean tree or changed files

Important boundary:

- `v0.3` is local Git discipline
- GitHub and pull requests come later as collaboration and remote workflow

## Core Concepts

## Repository

A Git repository is a directory with a `.git` database inside it.

That database records snapshots, history, branches, and metadata.

Run:

```bash
ls -la .git
```

Expected behavior:

- `.git` exists
- it contains Git's internal data

You do not need to edit `.git`.
You do need to know it is what makes the folder a repository.

## Working Tree

The working tree is the files you see and edit.

If you change a Markdown file or script, the working tree changes first.

Run:

```bash
git status --short
```

Expected output shape when clean:

```text
```

Expected output shape when files changed:

```text
 M curriculum/phase0/v0.3/03-notes.md
?? scratch/example.txt
```

Read the status as a signal:

- `M` means modified
- `??` means untracked
- left column means staged state
- right column means working tree state

You do not need every status code yet.
You do need to stop treating Git status as noise.

## Diff

A diff shows what changed.

Run:

```bash
git diff
```

Expected behavior:

- Git shows changed lines that are not staged yet
- added lines usually start with `+`
- removed lines usually start with `-`

Diffs are how you review your own work before asking anyone else to trust it.

Practical rule:

Do not stage or commit changes you have not reviewed.

## Staging Area

The staging area is the set of changes selected for the next commit.

Run:

```bash
git add curriculum/phase0/v0.3/03-notes.md
git diff --cached
```

Expected behavior:

- `git diff --cached` shows staged changes
- unstaged changes, if any, remain outside the next commit

The staging area lets you say:

`these changes belong together`

That is why `git add -A` is powerful but dangerous.
It can stage unrelated work if you do not inspect first.

## Commit

A commit is a named snapshot of selected changes.

Good commit messages explain intent.

Weak:

```text
update files
```

Stronger:

```text
curriculum: author v0.3 git discipline
```

The stronger message says:

- domain: curriculum
- action: author
- subject: v0.3 git discipline

## History

Run:

```bash
git log --oneline -5
```

Expected output shape:

```text
f855755 curriculum: upgrade phase0 foundation standards
5daa92a curriculum: deepen v0.2 linux fundamentals pass
...
```

Each line is a memory handle.
It lets you inspect system evolution without guessing.

## Build

This version's build is not a new application feature.
It is a disciplined Git milestone.

Create a tiny learning marker:

```bash
mkdir -p .aois-state
printf "v0.3 git discipline checkpoint\n" > .aois-state/v0.3-git-check.txt
```

Then inspect:

```bash
git status --short
git diff -- .aois-state/v0.3-git-check.txt
```

Expected behavior:

- Git shows `.aois-state/v0.3-git-check.txt` as new or changed
- the diff shows the exact line you wrote

Then stage and review:

```bash
git add .aois-state/v0.3-git-check.txt
git diff --cached -- .aois-state/v0.3-git-check.txt
```

Expected behavior:

- the staged diff shows only the checkpoint file

Commit only after review:

```bash
git commit -m "learning: record v0.3 git checkpoint"
```

If there are other real curriculum changes in progress, do not mix them into this practice commit.
A clean Git habit is more important than rushing.

## Ops Lab

Inspect the repository as a system:

```bash
git status --short
git log --oneline -5
git diff --stat HEAD~1..HEAD
```

Questions:

1. Is the working tree clean or dirty?
2. What was the most recent commit about?
3. Which files changed in the most recent commit?
4. Was the commit message specific enough to understand intent?
5. Does the commit look like one coherent decision or mixed unrelated work?

Answer key:

1. A clean tree prints no short-status lines; a dirty tree prints changed or untracked files.
2. The most recent `git log --oneline -5` line gives the summary.
3. `git diff --stat HEAD~1..HEAD` lists changed files and size of changes.
4. A good message names the domain and the intent.
5. Coherent commits usually change files that support the same purpose.

## Break Lab

Do not skip this.

### Option A - Untracked file confusion

Create an untracked scratch file:

```bash
printf "temporary thought\n" > /tmp/aois-git-scratch.txt
cp /tmp/aois-git-scratch.txt .aois-state/git-scratch.txt
git status --short
```

Expected symptom:

```text
?? .aois-state/git-scratch.txt
```

Fix:

If the file is useful, stage it deliberately.
If it is not useful, remove only that file:

```bash
rm -f .aois-state/git-scratch.txt
git status --short
```

Lesson:

- untracked does not mean broken
- it means Git is not tracking that file yet

False conclusion this prevents:

- "Git is angry" when Git is only reporting new state

### Option B - Blind staging risk

Run:

```bash
git status --short
```

Before any `git add -A`, answer:

- do all visible changes belong in one commit?
- did I review the diff?
- are any generated, secret, scratch, or unrelated files present?

Lesson:

- staging everything is safe only after inspection

False conclusion this prevents:

- "commit everything because Git asked me to"

### Option C - Message quality break

Compare:

```text
fix
```

with:

```text
scripts: add rule-based incident classifier
```

Expected lesson:

- the second message is reviewable later
- the first message destroys useful memory

## Testing

The version passes when:

1. you can explain working tree, staging area, commit, and history
2. you can read `git status --short`
3. you can inspect unstaged and staged diffs
4. you can make a small coherent commit
5. you can explain why blind `git add -A` is risky
6. you can inspect the most recent commit and say what changed
7. you can write a commit message that explains intent

## Common Mistakes

- using Git only as a backup button
- committing unrelated work together
- staging without reading the diff
- writing messages like `fix`, `update`, or `changes`
- panicking when a file is untracked
- assuming clean history happens automatically
- using destructive commands to escape confusion

## Troubleshooting

If Git status looks confusing:

```bash
git status --short
git diff
git diff --cached
```

Then classify each file:

- intentional curriculum change
- intentional code/script change
- scratch file
- generated file
- unknown file that needs inspection

If a file is untracked:

- inspect it
- decide whether it belongs
- stage it only if it belongs

If you staged too much:

```bash
git restore --staged <path>
```

This removes the path from the staging area without deleting your working copy.

Do not use destructive reset commands unless a live teacher explicitly approves the exact recovery.

## Benchmark

Measure:

- can you identify clean vs dirty repo state in under 10 seconds?
- can you explain the most recent commit from `git log --oneline -5`?
- can you inspect what changed in the last commit?
- can you write a specific commit message without vague words?
- can you decide whether files belong together in one commit?

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can inspect, stage, commit, and explain history without hints. |
| 4/5 | You can complete the workflow, but one concept needs review. |
| 3/5 | You can follow commands, but diff/staging decisions need help. |
| 2/5 | You can commit, but cannot explain what belongs together. |
| 1/5 | Git still feels like magic or danger. |

Minimum pass: `4/5`.

## Architecture Defense

Why teach Git before HTTP, Python, and FastAPI?

Because every later system change needs durable memory.
If you cannot inspect what changed locally, deployment and production debugging become guesswork.

Why not start with GitHub pull requests?

Because local Git concepts come first.
Remote collaboration is built on local snapshots, diffs, staging, commits, and history.

Why make commits small?

Because a small coherent commit is reviewable, reversible in concept, and explainable.
A giant mixed commit hides decisions.

## 4-Layer Tool Drill

Tool: Git

1. Plain English
Git records the history of project changes.

2. System Role
It makes AOIS evolution inspectable, reviewable, and recoverable.

3. Minimal Technical Definition
Git is a distributed version control system that stores snapshots and metadata about file changes.

4. Hands-on Proof
If Git history is absent or sloppy, you cannot reliably answer what changed, why it changed, or which files belonged to the same decision.

## 4-Level System Explanation Drill

1. Simple English
I learned how to save and inspect meaningful project history.

2. Practical Explanation
I can now check repo state, review diffs, stage intentional changes, commit them, and inspect recent history.

3. Technical Explanation
This version teaches the working tree, staging area, commits, and log inspection as the local version-control layer for AOIS.

4. Engineer-Level Explanation
AOIS now has an engineering memory layer: Git records coherent system changes so later service, infrastructure, AI, and governance work can be reviewed, audited, explained, and debugged through history rather than reconstructed from memory.

## Failure Story

Representative failure:

- Symptom: unrelated files were almost committed together
- Root cause: staging happened before diff review
- Fix: inspect `git status --short`, review diffs, unstage unrelated files with `git restore --staged <path>`
- Prevention: review before staging and commit one coherent decision at a time
- What this taught me: Git discipline is not just command usage; it is engineering judgment

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does Git solve in AOIS?
2. What is the working tree?
3. What is the staging area?
4. What is a commit?
5. Why should you read `git diff` before staging?
6. Why is `git add -A` risky when you have not inspected status?
7. What makes a commit message useful?
8. Why are small coherent commits better than large mixed commits?
9. How does Git support later infrastructure debugging?
10. Explain Git using the 4-layer tool rule.
11. Explain `v0.3` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does Git solve in AOIS?

Git makes AOIS change inspectable.
It records what changed, when it changed, and why the change was grouped as one decision.
That matters because AOIS will grow across scripts, services, databases, infrastructure, models, agents, and governance.

2. What is the working tree?

The working tree is the current set of files you can see and edit in the repo.
When you modify a Markdown file, script, Python file, or config, the working tree changes before anything is committed.

3. What is the staging area?

The staging area is the set of changes selected for the next commit.
It lets you decide which changes belong together before recording them in history.

4. What is a commit?

A commit is a recorded snapshot of selected changes plus metadata such as author, time, parent commit, and message.
In AOIS, a commit should represent one coherent engineering decision.

5. Why should you read `git diff` before staging?

Because `git diff` shows the exact unstaged changes.
Reading it prevents accidental commits, catches mistakes early, and forces you to understand what you are about to preserve in history.

6. Why is `git add -A` risky when you have not inspected status?

`git add -A` stages all changes, including unrelated edits, scratch files, generated files, or accidental modifications.
It is safe only after `git status --short` and `git diff` prove everything belongs in the same commit.

7. What makes a commit message useful?

A useful commit message names the domain and intent.
For example, `curriculum: author v0.3 git discipline` is useful because it says what area changed and why.
Messages like `fix` or `updates` are weak because they do not explain the decision later.

8. Why are small coherent commits better than large mixed commits?

Small coherent commits are easier to review, explain, debug, and reason about.
Large mixed commits hide decisions and make it harder to find which change caused a later problem.

9. How does Git support later infrastructure debugging?

Infrastructure failures often come from config, deployment, or dependency changes.
Git lets you inspect exactly when manifests, scripts, service code, or policy files changed, which makes debugging evidence-based instead of memory-based.

10. Explain Git using the 4-layer tool rule.

- Plain English: Git records project history.
- System Role: Git makes AOIS evolution inspectable and reviewable.
- Minimal Technical Definition: Git is a distributed version control system that stores snapshots and metadata about file changes.
- Hands-on Proof: Without clean Git history, you cannot reliably answer what changed, why it changed, or which files belonged to one decision.

11. Explain `v0.3` using the 4-level system explanation rule.

- Simple English: I learned how to save and inspect meaningful project history.
- Practical explanation: I can check status, read diffs, stage intentional changes, commit them, and inspect recent history.
- Technical explanation: `v0.3` teaches working tree, staging area, commits, and log inspection as AOIS's local version-control layer.
- Engineer-level explanation: AOIS now has an engineering memory layer that makes later service, infrastructure, AI, and governance work auditable through coherent Git history.

## Connection Forward

`v0.3` teaches the third AOIS habit:

`record meaningful change`

`v0.4` moves from local repo history to network and HTTP inspection, where AOIS starts reasoning about service boundaries.

## Source Notes

This version uses stable local Git behavior.
No fast-moving external source is required for the core lesson.

If this version later expands into GitHub, pull requests, branch protection, signed commits, or CI policy, add source notes for the specific remote platform and policy behavior.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.3 Introduction](02-introduction.md)
- Next: [v0.3 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
