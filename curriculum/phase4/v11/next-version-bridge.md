# v11 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

`v11` unlocks cloud workflow reasoning without cloud execution.

AOIS can now explain:

- where events enter
- how work is buffered
- how retries behave
- where failures are preserved
- how traces cross workflow boundaries
- why idempotency is mandatory

## Why The Next Version Exists

The next version focuses on observability and cost controls.

Event-driven systems can fail silently if queues grow, retries loop, DLQs fill, or cost increases in the background.

`v12` will plan how AOIS watches event workflows before trusting them in live infrastructure.
