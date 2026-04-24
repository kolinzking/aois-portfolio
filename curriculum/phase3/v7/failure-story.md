# v7 Failure Story

Authoring status: authored

## Symptom

A Helm chart installs workloads without resource limits.

## Root Cause

The raw manifest limits were lost during chart templating.

## Fix

Put limits in `values.yaml` and wire them into deployment templates.

## Prevention

Validate the chart before install.

Compare chart controls to the original manifests.

## What This Taught Me

Packaging must preserve safety controls.
