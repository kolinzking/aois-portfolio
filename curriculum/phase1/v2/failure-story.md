# v2 Failure Story

Authoring status: authored

## Symptom

Every incident was planned for the strongest external route.

## Root Cause

The route logic ignored severity, latency, cost, and provider-budget approval.

It treated model choice like a preference instead of an operational policy.

## Fix

Route through explicit constraints:

- severity
- latency budget
- cost budget
- provider-budget approval
- fallback

## Prevention

Test:

- no approval
- low budget
- low latency
- high severity
- fallback behavior

## What This Taught Me

Model routing is cost and reliability policy.

It should be inspectable before any provider call can happen.
