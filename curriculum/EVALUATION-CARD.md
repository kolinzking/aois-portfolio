# AOIS Evaluation Card

Authoring status: authored

Evaluation status: local corpus review passed; release approval pending commit

This card records the current review posture for the AOIS curriculum corpus.

## Current State

The lesson corpus is authored according to `curriculum/CORPUS-STATUS.md`.

Current review evidence:

- all versions in the corpus status table are marked `authored`
- Phase 10 is authored through `v34`
- dirty worktree review confirmed the untracked support files are intentional curriculum artifacts
- focused scaffold and authoring-marker scan passes for Phase 7 through Phase 10 and the new support files
- local Markdown links resolve
- referenced support-file paths resolve
- source notes are present for `v21` through `v34`
- all validators and simulators pass locally
- all example scripts compile
- repo shell scripts pass `bash -n`
- `git diff --check` passes

## Review Gates

Completed review gates:

- full scaffold and placeholder scan
- local link and continuity review
- full validator and simulator run
- source currency review
- safety-boundary review
- dirty worktree review

Before live teaching, the corpus still needs:

- dirty worktree committed
- final release approval after commit

## Evaluation Position

The curriculum is locally review-clean but not yet release-approved because the
reviewed corpus is still uncommitted.
