# v0.2 Failure Story

## Symptom

The script existed, but it would not execute.

## Root Cause

The file lacked execute permission.

## Fix

Run:

```bash
chmod +x scripts/sysinfo.sh
```

## Prevention

Always inspect permissions with `ls -l` before assuming script logic is broken.
