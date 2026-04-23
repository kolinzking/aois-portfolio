# v0.1 Failure Story

This file is pre-authored so self-paced learners are not blocked.
You may append your own failure after reading this one.

## Symptom

The script ran, but a beginner might read the memory line and conclude the machine is already close to failure because `used` memory looks high.

## Root Cause

The script reports `used / total` memory only.
That is operationally incomplete on Linux because `used` includes cached memory and does not directly tell you how much memory is safely available.

## Fix

Validate the script output against `free -h` and pay special attention to the `available` column.
Then explicitly note that the script is useful but incomplete.

## Prevention

Never trust a summarized metric until you compare it to the underlying system command at least once.
Later versions should improve the report to include stronger memory signals.

## What This Taught Me

Execution success is not the same as interpretation success.
A script can run perfectly and still support bad operational conclusions if I read the wrong signal too confidently.

## Why This Counts

Interpretation failures count.
Misreading memory or disk data is an engineering failure, not a minor detail.

## Optional Personal Failure

Add your own failure below this section if a different one happened during your run.
