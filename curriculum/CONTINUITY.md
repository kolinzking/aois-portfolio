# AOIS Continuity Protocol

This file exists so the institution survives interruptions cleanly.

## Current Persistence State

Right now, the curriculum exists as real files in the repository.

That means the institution is already persisted on disk, not only in chat context.

Current persistence mechanisms:

- curriculum documents saved in the repo
- lesson packs saved in the repo
- git history available as the long-term record once commits are made

## What Is Not Yet Guaranteed

There is no special background autosave system that snapshots every thought independently of the filesystem.

The reliable persistence layer is:

- files on disk
- git commits

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

## Resume Protocol

If the terminal closes or the session is interrupted, resume using this order:

1. Open [INSTITUTION-INDEX.md](/home/collins/aois-portfolio/curriculum/INSTITUTION-INDEX.md:1)
2. Open this file
3. Check `git status`
4. Open the latest version directory you were working in
5. Read the `failure-story.md` and `benchmark.md` for that version
6. Continue from the last unfinished lab or mastery checkpoint

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

## Best Protection Against Loss

The best practical protection is:

1. keep everything in repo files
2. commit at each milestone
3. keep one clear resume file like this

If you want the strongest possible continuity, the next correct action is to commit the institution documents and the `v0.1` lesson pack to git.
