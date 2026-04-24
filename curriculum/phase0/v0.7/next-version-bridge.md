# v0.7 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

`v0.7` gives AOIS a safe model-call planning boundary.

The system can now describe what it would ask a model to do, how large the request might be, what output shape it expects, and why a real provider call needs approval.

## Why The Next Version Exists

`v0.8` adds Postgres foundations.

AOIS needs persistence before serious AI workflows can be evaluated over time.
Terminal output and dry-run JSON are not enough for incident history, audit trails, comparisons, or later retrieval-augmented workflows.

Carry forward:

- estimate before calling
- structure before parsing
- gate external dependencies
- keep server resources controlled
