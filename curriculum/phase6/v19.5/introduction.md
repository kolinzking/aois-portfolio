# v19.5 Introduction

Authoring status: authored

v19 taught AOIS how to test reliability assumptions safely through chaos
engineering. v19.5 narrows the focus to AI-specific failure.

Traditional services fail through errors, latency, resource pressure, bad
deploys, and unavailable dependencies. AI systems can fail while still returning
HTTP 200. They can sound confident without evidence, recommend unsafe action,
leak sensitive information, cross a policy boundary, overuse tools, or continue
when a human should take over.

This version builds a local governance plan for those failures. It does not
connect to a provider, start an agent, execute tools, or enforce policy in a
live runtime. It teaches the control model first:

- identify the AI failure class
- check evidence and confidence
- inspect policy boundaries
- allow, review, block, or fall back
- keep an audit trail
- require human approval for dangerous action

The practical outcome is simple: AOIS stops treating AI output as automatically
actionable. An AI recommendation becomes one input into a controlled operational
decision.
