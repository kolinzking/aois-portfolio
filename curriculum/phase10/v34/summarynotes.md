# v34 Summary Notes

Authoring status: authored

## What Was Built

v34 adds a local governance and computer-use contract:

- `frontier/aois-p/governance-computer-use.plan.json`
- `examples/validate_governance_computer_use_plan.py`
- `examples/simulate_governance_computer_use.py`

The simulator decides whether a proposed computer-use path is recorded,
drafted, routed to a manual operator, held, or blocked.

## What Was Learned

Key controls:

- governance policy
- action intent and classification
- local synthetic environment
- target allowlist
- human approval and manual handoff
- credential boundary
- data classification and redaction
- safety checks
- step preview
- action budget and rate limit
- stop control
- rollback
- audit trace and redacted screen evidence
- operator watch
- red-team clearance
- release and access gates

## Core Limitation Or Tradeoff

v34 does not start a computer-use runtime, browser, VM, screenshot capture,
mouse, keyboard, clipboard, file transfer, network, provider, tool, command,
shell, credential, payment, form submission, or external action. It models
governance verification before live action is considered.
