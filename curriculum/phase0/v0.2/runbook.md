# v0.2 Runbook

## Purpose

Use this runbook when `scripts/sysinfo.sh` will not run or its output looks wrong.

## Primary Checks

1. confirm the file exists
2. confirm it is executable with `ls -l scripts/sysinfo.sh`
3. run the raw commands directly:
   - `top -bn1 | grep "Cpu(s)"`
   - `free -h`
   - `df -h /`
4. compare raw output with the script output

## Recovery Steps

1. restore execute permission with `chmod +x scripts/sysinfo.sh`
2. fix any command typo inside the script
3. rerun the raw command before rerunning the script
4. confirm the report structure before worrying about exact numeric values
