# AOIS Portfolio

AOIS stands for AI Operations & Intelligence System.

This repository serves two purposes:

1. The working engineering system as it evolves across phases and versions.
2. The public portfolio artifact that shows traceable, reviewable progress.

## Operating Model

The project runs with three roles:

- ChatGPT: architect, teacher, debugger, curriculum guide
- Codex: builder, file editor, command runner, implementation assistant
- User: orchestrator, learner, final decision-maker

The workflow is intentionally strict:

1. Define the version goal and understand what is being built.
2. Implement the smallest useful slice in the repo.
3. Run the result locally and inspect the output.
4. Debug, refine, and explain what happened.
5. Commit small milestones with clear messages.

## Current Phase

The repository is currently in Phase 0.

Phase 0 focuses on:

- Linux and bash fundamentals
- Git and disciplined iteration
- Early scripts and local tooling
- Clear documentation of what was built and why

This phase should stay simple. Avoid premature platform complexity until the curriculum reaches it.

## Structure

The repo starts minimal and expands only when the work justifies it:

- `scripts/`: shell utilities and early system scripts
- `app/`: early Python modules and the first FastAPI service
- `examples/`: focused one-off artifacts such as the first raw model call
- `sql/`: the first AOIS persistence schema
- `curriculum/`: phase-by-phase notes, version records, and continuity docs

Additional top-level directories such as `app/`, `tests/`, `tools/`, `workflows/`, `graph/`, `policy/`, and deployment layers will be added when the curriculum genuinely reaches them.

## Continuity Rule

Continuity is preserved through:

- stable directory structure
- small commits
- version-scoped notes in `curriculum/`
- Git history as the primary source of truth

Persistent agent memory files such as `AGENTS.md` are intentionally deferred until a later phase unless explicitly needed.
