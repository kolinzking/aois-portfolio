# v0.8 Failure Story

## Symptom

The first instinct was to put incident fields and analysis fields into one record because it looked simpler.

## Root Cause

The design treated an operational event and its interpretation as the same thing.

## Fix

Split them into related tables.

## Prevention

Model the event and the analysis as different system objects even when the initial example is small.
