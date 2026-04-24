# v10 Failure Story

Authoring status: authored

## Symptom

A cloud model call sends sensitive input and creates spend before review.

## Root Cause

The provider call was wired before security, budget, credential, and eval gates were approved.

## Fix

Restore the managed model plan and keep:

- provider call false
- credentials absent
- budget unapproved
- security inspection required
- eval baseline required

## Prevention

Validate before live integration.

Use official provider docs only when preparing real calls.

## What This Taught Me

Managed inference is still an operational boundary.
