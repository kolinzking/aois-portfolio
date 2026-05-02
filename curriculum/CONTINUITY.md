# AOIS Continuity Protocol

This file exists so the institution survives interruptions cleanly.

## Current Persistence State

Right now, the curriculum exists as real files in the repository.

That means the institution is already persisted on disk, not only in chat context.

Current persistence mechanisms:

- curriculum documents saved in the repo
- lesson packs saved in the repo
- git history available as the long-term record once commits are made
- VS Code autosave in `.vscode/settings.json`
- repo-owned checkpoint snapshots in `.aois-state/`
- versioned git hook in `.githooks/post-commit`

## What Is Not Yet Guaranteed

There is no special background autosave system that snapshots every thought independently of the filesystem.

The reliable persistence layer is:

- files on disk
- git commits
- repo checkpoint snapshots

So the strongest protection is disciplined checkpoint commits.

## Required Continuity Measures

To avoid losing progress, we use these rules:

1. All curriculum design must live in repo files, not only in chat.
2. Every meaningful institutional milestone should be committed.
3. Every teaching milestone should leave explicit artifacts:
   - notes
   - lab
   - runbook
   - benchmark
   - failure story
4. Every session should end with a visible current-status note.
5. The repo should maintain a resumable checkpoint on disk even between commits.

## Resume Protocol

If the terminal closes or the session is interrupted, resume using this order:

1. Open [INSTITUTION-INDEX.md](INSTITUTION-INDEX.md)
2. Open this file
3. Check `git status`
4. Run `scripts/aois_resume.sh`
5. Open the latest version directory you were working in
6. Read `06-failure-story.md` and `07-benchmark.md` for that version
7. Continue from the last unfinished lab or mastery checkpoint

## Session-End Checklist

At the end of any session, we should know:

- which version was active
- what was completed
- what failed
- what the next exact step is

## Current Resume Point

Institution locked through:

- master curriculum
- syllabus
- full program map
- learning operating model
- version standard
- repo blueprint

Teaching progress:

- Phase 0 introduction rewritten
- `v0.1` lesson pack rewritten

Current next step:

- teach `v0.1`
- author `v0.2` lesson pack next

## Installed Continuity Toolchain

The institution now uses a three-layer continuity setup:

1. Editor autosave
Local VS Code settings save file edits automatically after a short delay.

2. Repo checkpoint script
`scripts/aois_checkpoint.sh` writes the latest working state into `.aois-state/latest-checkpoint.md`.

Example:

```bash
scripts/aois_checkpoint.sh \
  --lesson "00-phase0/v0.1" \
  --next "Complete the v0.1 mastery checkpoint" \
  --note "Finished the ops lab, break lab next."
```

3. Automatic post-commit checkpoint
The repo hook `.githooks/post-commit` refreshes the checkpoint automatically after each commit.

## Best Protection Against Loss

The best practical protection is:

1. keep everything in repo files
2. commit at each milestone
3. keep one clear resume file like this
4. keep an on-disk checkpoint snapshot through the installed toolchain

If you want the strongest possible continuity, the next correct action is to commit the institution documents and the `v0.1` lesson pack to git.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](READING-ORDER.md)
- Previous: [AOIS Repository Blueprint](REPO-BLUEPRINT.md)
- Next: [AOIS Curriculum Corpus Status](CORPUS-STATUS.md)
<!-- AOIS-NAV-END -->
