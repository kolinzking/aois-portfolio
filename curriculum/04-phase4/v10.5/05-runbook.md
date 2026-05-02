# v10.5 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v10.5` managed-agent tradeoff plan to a safe validation-only state.

Safe state means:

- no cloud agent exists from this lesson
- no credentials are required
- current choice remains AOIS-owned runtime
- managed-agent use remains gated

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_managed_agent_plan.py
python3 examples/validate_managed_agent_plan.py
```

Inspect:

```bash
sed -n '1,240p' cloud/aws/managed-agent-tradeoff.plan.json
```

Required validator result:

- `cloud_agent_created` is `false`
- `credentials_used` is `false`
- `status` is `pass`

## Recovery Steps

If validation fails:

1. Read the `missing` list in the validator output.
2. Restore `cloud_agent_created` to `false`.
3. Restore `credentials_used` to `false`.
4. Restore `external_network_required_for_this_lesson` to `false`.
5. Restore `decision.current_choice` to `aois-owned-agent-runtime`.
6. Restore every required gate in `required_before_managed_agent`.
7. Rerun the validator.

If someone asks to create a real managed agent:

1. Stop the lesson path.
2. Review official provider documentation.
3. Define tool permissions before any tool integration.
4. Define credential storage and secret handling.
5. Define budget and cost guardrails.
6. Define data boundaries.
7. Define eval baseline and rollback.
8. Get explicit approval before creating any cloud resource.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v10.5 Lab](04-lab.md)
- Next: [v10.5 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
