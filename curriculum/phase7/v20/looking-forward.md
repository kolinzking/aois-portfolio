# v20 Looking Forward

Authoring status: authored

## What You Should Carry Forward

Carry forward these rules:

- A tool request is not tool execution.
- Investigation starts read-only.
- Tool inputs and outputs need schemas.
- Evidence must be recorded before claims.
- Secret-bearing data blocks and redacts.
- Mutation requires human approval.
- Invalid tool output falls back.

The most important habit is to separate capability from authority.

## What The Next Version Will Build On

v20.1 will keep the same incident-step shape and add cost:

```text
step -> tokens/tool/runtime/cost -> incident total -> budget decision
```

This matters because agentic workflows can look correct while quietly becoming
too expensive or too repetitive to operate.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20 Summary Notes](summarynotes.md)
- Next: [v20 Next Version Bridge](next-version-bridge.md)
<!-- AOIS-NAV-END -->
