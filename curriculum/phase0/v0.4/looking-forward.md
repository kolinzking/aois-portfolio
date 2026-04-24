# v0.4 Looking Forward

Authoring status: authored

## What You Should Carry Forward

Inspect the boundary before blaming the system.

For HTTP, always ask:

- did the request connect?
- what status code returned?
- what headers came back?
- what body came back?
- how long did it take?

## What The Next Version Will Build On

`v0.5` builds on this by moving AOIS logic into Python.
Later, `v0.6` turns that Python into a real FastAPI service that you will inspect with the same HTTP habits from this version.
