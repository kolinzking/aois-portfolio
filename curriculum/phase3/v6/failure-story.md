# v6 Failure Story

Authoring status: authored

## Symptom

A portfolio pod consumes more memory than expected on the shared server.

## Root Cause

The workload was applied without quota, default limits, or container memory limits.

## Fix

Add and validate:

- `ResourceQuota`
- `LimitRange`
- deployment `resources`
- one replica

## Prevention

Validate manifests before applying.

Keep portfolio workloads in `aois-p`.

Record resource usage after any approved apply.

## What This Taught Me

Kubernetes safety starts before live cluster mutation.
