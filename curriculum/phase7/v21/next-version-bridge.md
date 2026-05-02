# v21 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v21 gives AOIS-P a governed tool exposure boundary. A route can now ask for
tools only through a registry that records ownership, schemas, side-effect
classification, approval policy, allowed routes, audit events, and disabled
states.

This means future agent steps can be planned without relying on ad hoc tool
selection or model-visible descriptions as policy.

## Why The Next Version Exists

v22 introduces durable agent workflows.

Once tool exposure is governed, AOIS needs a way to run multi-step work without
losing state. A workflow may need to:

- plan evidence gathering
- wait for human approval
- resume after approval
- record which tools were planned or blocked
- preserve trace and cost context
- stop safely after a failure

The registry answers "which tools are allowed?" v22 answers "how does the
agent workflow remember, wait, resume, and recover?"
