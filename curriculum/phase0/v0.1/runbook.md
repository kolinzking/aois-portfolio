# v0.1 Runbook

## Purpose

Use this runbook when the basic Linux inspection commands are confusing or produce unexpected output.

## Primary Checks

1. confirm where you are with `pwd`
2. inspect the directory with `ls -la`
3. run the raw commands directly:
   - `top -bn1 | grep "Cpu(s)"`
   - `free -h`
   - `df -h /`
   - `ps aux | head -5`
4. compare what you expected with what Linux is actually showing you

## Recovery Steps

1. go back to the repo root with `cd /home/collins/aois-portfolio`
2. rerun the commands one by one instead of chaining assumptions together
3. restore permissions with `chmod` if access is blocked
4. interpret the raw command output before trying to automate anything
5. if you are confused by output, name what each visible column or token means before rerunning the command
