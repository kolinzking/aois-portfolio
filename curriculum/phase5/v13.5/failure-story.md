# v13.5 Failure Story

Authoring status: authored

## Symptom

A GPU inference pod stays pending and the team cannot tell whether the problem is node capacity, resource advertisement, taints, or workload configuration.

## Root Cause

The team assumed GPU infrastructure existed because the application manifest requested GPU resources.

They skipped device plugin planning, node labeling, taints/tolerations, and scheduling observability.

## Fix

Return to the infrastructure plan.

Verify resource advertisement, node placement rules, scheduling events, and pod-to-GPU mapping before applying GPU workloads.

## Prevention

Validate the `v13.5` plan before any GPU operator, device plugin, or workload apply.

Lesson learned: GPU failures often start in scheduling, not model code.
