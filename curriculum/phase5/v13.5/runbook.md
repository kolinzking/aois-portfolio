# v13.5 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v13.5` GPU infrastructure plan to safe no-apply state.

Safe state means:

- no `kubectl apply`
- no GPU operator installed
- no device plugin installed
- no GPU runtime started
- no GPU required for the lesson
- no live GPU infrastructure approval

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_gpu_infrastructure_plan.py
python3 examples/validate_gpu_infrastructure_plan.py
```

Required result:

- `status=pass`
- `kubectl_apply_ran=false`
- `gpu_operator_installed=false`
- `device_plugin_installed=false`
- `gpu_runtime_started=false`
- namespace is `aois-p`

## Recovery Steps

If validation fails:

1. Read the `missing` list.
2. Restore namespace to `aois-p`.
3. Restore apply/operator/plugin/runtime flags to `false`.
4. Restore requested GPU count to `0`.
5. Restore scheduling controls.
6. Restore MIG review controls.
7. Restore observability controls.
8. Restore live checks.
9. Rerun validation.

If live GPU infrastructure work is requested:

1. Stop.
2. Review official operator/device-plugin documentation.
3. Define driver and CUDA plan.
4. Define node pool budget.
5. Define scheduling policy.
6. Define MIG strategy.
7. Define GPU observability.
8. Define rollback.
9. Verify primary AOIS separation.
10. Get explicit approval before applying anything.
