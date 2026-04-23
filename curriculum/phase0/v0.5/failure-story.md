# v0.5 Failure Story

## Symptom

Input looked fine in code review but failed at runtime when passed into the model.

## Root Cause

The request violated a real field constraint, and that constraint had not been mentally accounted for.

## Fix

Read the actual model definition and validate sample input explicitly.

## Prevention

Treat model constraints as part of the contract, not as optional decoration.
