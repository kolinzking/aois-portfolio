# v0.2 Runbook

Authoring status: authored

## Purpose

Use this runbook when `scripts/sysinfo.sh` or `scripts/log_analyzer.sh` will not run or their output looks wrong.

## Primary Checks

1. confirm the file exists
2. confirm it is executable with `ls -l scripts/sysinfo.sh scripts/log_analyzer.sh`
3. run the raw commands directly:
   - `top -bn1 | grep "Cpu(s)"`
   - `free -h`
   - `df -h /`
4. run analyzer examples directly:
   - `./scripts/log_analyzer.sh "gateway returned 5xx"`
   - `./scripts/log_analyzer.sh "pod OOMKilled exit code 137"`
   - `./scripts/log_analyzer.sh "strange message with no match"`
5. compare raw output with the script output

## Recovery Steps

1. restore execute permission with `chmod +x scripts/sysinfo.sh scripts/log_analyzer.sh`
2. fix any command typo inside the script
3. rerun the raw command before rerunning the script
4. confirm the report structure before worrying about exact numeric values
5. if the analyzer says `unknown`, inspect the input wording before assuming the incident is safe

## Common Diagnosis

| Symptom | Likely cause | Fix |
|---|---|---|
| `Permission denied` | execute bit missing | run `chmod +x scripts/<name>.sh` |
| `No such file or directory` | wrong path or current directory | run `pwd` and use the correct path |
| `unbound variable` | `set -u` found an unset variable | define the variable or remove the bad reference |
| analyzer returns `unknown` | no rule matched the message | preserve the message and add/adjust a rule only if the pattern is reliable |
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.2 Lab](lab.md)
- Next: [v0.2 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
