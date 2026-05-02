# v10.5 Introduction

Authoring status: authored

## What This Version Is About

`v10.5` compares two ways AOIS could run agent behavior:

- keep the agent loop inside AOIS
- delegate the agent loop to a managed cloud agent service later

The lesson is deliberately validation-only. You do not create an agent, configure credentials, connect a tool, or call a provider API.

The output is a managed-agent tradeoff plan and a local validator that proves the current choice remains AOIS-owned runtime.

## Why It Matters In AOIS

Model calls and agent runtime are not the same responsibility.

A model call sends input to a model and receives output. An agent runtime decides what to do next, what tools to call, what memory or retrieval to use, and how to recover from failure.

That means agent runtime is a trust boundary. If AOIS delegates it too early, the system may lose clear control over:

- tool permissions
- audit logs
- rollback behavior
- data boundaries
- vendor coupling
- cost controls

The correct frontier habit is not "use managed services everywhere." The correct habit is to know exactly which control you are giving away, what you get in return, and how you can prove the system remains safe.

## How To Use This Version

Use this version as a decision drill.

Run the validator first, then explain every field in `cloud/aws/managed-agent-tradeoff.plan.json`.

You are ready to continue only when you can defend this sentence:

AOIS can evaluate managed agents now, but should not create one until permission, data, budget, eval, credential, and rollback controls exist.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v10.5 Contents](CONTENTS.md)
- Next: [v10.5 - Managed Agent Tradeoffs Without Creating Agents](notes.md)
<!-- AOIS-NAV-END -->
