# v33 Lab

Authoring status: authored

## Build Lab

Run:

```bash
python3 -m py_compile examples/validate_adversarial_red_teaming_plan.py examples/simulate_adversarial_red_teaming.py
python3 examples/validate_adversarial_red_teaming_plan.py
python3 examples/simulate_adversarial_red_teaming.py
```

Expected simulator summary:

```json
{
  "passed_cases": 25,
  "score": 1.0,
  "status": "pass",
  "total_cases": 25
}
```

## Ops Lab

Open `frontier/aois-p/adversarial-red-teaming.plan.json`.

Find `red_team_scope` and confirm:

- no live target
- no production system
- no exploit execution
- no harmful payload storage
- no jailbreak or prompt-injection payload generation
- no tool, network, or provider calls

Find `scenario_catalog` and confirm every entry has a scenario ID, threat
category, attack surface, OWASP mapping, ATLAS or AI threat mapping, required
controls, and sanitized example label.

## Break Lab

Change one value at a time, run the simulator, then restore it:

- set `authorization_status` to `missing`
- set `payload_safety_status` to `unsafe`
- set `target_status` to `live_external`
- set `telemetry_status` to `missing`
- set `mitigation_status` to `missing` on a failed control case
- set `regression_status` to `missing` on a failed control case

Record the decision and operator action for each change.

## Explanation Lab

Explain why:

- indirect prompt injection is different from direct prompt injection
- system prompt leakage is not solved by hiding more secrets in the prompt
- model output should be treated as untrusted data
- edge cache and fallback abuse belong in red-team coverage
- mitigation and regression are separate closure gates

## Defense Lab

Defend these choices:

- the lab does not generate real attack payloads
- red-team scope blocks before technical testing begins
- unsafe payloads block even in a security curriculum
- evidence is sanitized
- confirmed failures escalate only after mitigation and regression state is known
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v33 - Adversarial Testing And Red Teaming](03-notes.md)
- Next: [v33 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
