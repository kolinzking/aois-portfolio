# v34 Lab

Authoring status: authored

## Build Lab

Run:

```bash
python3 -m py_compile examples/validate_governance_computer_use_plan.py examples/simulate_governance_computer_use.py
python3 examples/validate_governance_computer_use_plan.py
python3 examples/simulate_governance_computer_use.py
```

Expected simulator summary:

```json
{
  "passed_cases": 21,
  "score": 1.0,
  "status": "pass",
  "total_cases": 21
}
```

## Ops Lab

Open `frontier/aois-p/governance-computer-use.plan.json`.

Find `computer_use_scope` and confirm:

- no live computer, browser, or VM
- no screenshot capture
- no mouse, keyboard, or clipboard
- no credentials
- no file transfer
- no network, provider, or tool calls
- no transaction or external action

Find `action_catalog` and compare observe-only, draft-only, synthetic, credential,
transaction, and high-impact action types.

## Break Lab

Change one value at a time, run the simulator, then restore it:

- set `environment_type` to `developer_workstation`
- set `target_status` to `live_production`
- set `credential_status` to `requested`
- set `privacy_status` to `raw` with `data_classification` set to `sensitive`
- set `stop_control_status` to `missing`
- set `red_team_status` to `unresolved`

Record the decision and operator action for each change.

## Explanation Lab

Explain why:

- observe-only and draft-only paths are not the same as action paths
- missing approval holds, but manual-required routes to an operator
- credentials block before action planning continues
- high-impact and external transaction actions are blocked
- stop control and rollback are different controls

## Defense Lab

Defend these choices:

- no live browser is started in the lesson
- screenshot evidence is modeled as redacted instead of captured
- v33 red-team clearance gates v34 release
- live targets, credentials, transactions, and high-impact actions are hard blocks
- governance verification precedes computer use
