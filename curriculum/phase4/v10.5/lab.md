# v10.5 Lab

Authoring status: authored

## Build Lab

Goal: validate the managed-agent tradeoff plan without creating any cloud resource.

1. Inspect the plan:

```bash
sed -n '1,240p' cloud/aws/managed-agent-tradeoff.plan.json
```

2. Compile the validator:

```bash
python3 -m py_compile examples/validate_managed_agent_plan.py
```

3. Run the validator:

```bash
python3 examples/validate_managed_agent_plan.py
```

Expected result:

```json
{
  "cloud_agent_created": false,
  "credentials_used": false,
  "status": "pass"
}
```

## Ops Lab

Answer from the plan file, not from memory:

1. What is the current agent-runtime choice?
2. Which option has lower vendor coupling?
3. Which option has provider-dependent auditability?
4. Which required item protects against unsafe tool access?
5. Which required item protects against uncontrolled spend?

Answer key:

1. `aois-owned-agent-runtime`
2. `aois-owned-agent-runtime`
3. `managed-cloud-agent-placeholder`
4. `tool_permission_review`
5. `budget_approval`

## Break Lab

Use a scratch copy only. Do not modify the committed plan.

Break 1: set `cloud_agent_created` to `true`.

Expected result: validation fails because the lesson is no-cloud-agent validation only.

Break 2: remove `tool_permission_review`.

Expected result: validation fails because managed agents must not be allowed to use tools without explicit permission review.

Break 3: set `decision.current_choice` to `managed-cloud-agent-placeholder`.

Expected result: validation fails because AOIS has not yet approved the managed-agent control set.

## Explanation Lab

Explain these aloud or in writing:

1. A model endpoint is not the same as an agent runtime.
2. Tool access makes an agent a security boundary.
3. Managed services can reduce operational burden but increase coupling.
4. Auditability must be proven, not assumed.
5. The validator is a local safety gate, not a cloud integration.

## Defense Lab

Defend the architecture decision:

AOIS should keep the agent loop owned locally until the project has provider docs review, credential storage design, budget approval, data-boundary review, tool-permission review, eval baseline, and rollback plan.

If your defense is "managed agents are easier," it is incomplete. You must also explain what control is delegated and how AOIS would verify the delegated behavior.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v10.5 - Managed Agent Tradeoffs Without Creating Agents](notes.md)
- Next: [v10.5 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
