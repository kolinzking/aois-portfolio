# v0.1 Failure Story

## Symptom

The file existed, but it could not be read.

## Root Cause

The permissions removed access.

## Fix

Run:

```bash
chmod 644 /tmp/linux-demo.txt
```

## Prevention

Always inspect permissions with `ls -l` before assuming the file content is the problem.
