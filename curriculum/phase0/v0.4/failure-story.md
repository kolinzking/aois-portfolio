# v0.4 Failure Story

## Symptom

An endpoint probe failed and the first instinct was to say, "the API is broken."

## Root Cause

The failure was not an application-level response.
The hostname itself was invalid, so no real HTTP response was ever created.

## Fix

Separate these two questions:

1. did I reach a real host?
2. if yes, what HTTP response came back?

Only after that should you debug route or server behavior.

## Prevention

Always distinguish:

- DNS / host failure
- connection failure
- HTTP response failure

Those are different layers of the system.
