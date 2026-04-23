# v0.6 Failure Story

## Symptom

The API returned clean JSON, so it was tempting to assume the analysis was reliable.

## Root Cause

The service shape improved, but the analysis engine underneath was still simplistic.

## Fix

Separate transport quality from inference quality in your mind.

## Prevention

Ask two questions:

1. did the API behave correctly?
2. did the analysis logic behave intelligently?
