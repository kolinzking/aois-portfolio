# v0.1 Notes

## Goal

Build the first useful system script in AOIS and establish the repo habit of documenting versions as they happen.

This version is not just about writing a script. It is the first SRE lens for AOIS:

What is happening inside this machine?

That perspective becomes the foundation of observability, debugging, and later automation.

## System Model

A basic system here means:

- CPU for processing
- memory for temporary working space
- disk for persistent storage

Production failures often reduce to one of these areas. Later AOIS will map signals like `OOMKilled`, high latency, or full storage back to them.

## Scope

Current implementation target:

- `scripts/sysinfo.sh`

The script must show:

- CPU usage
- memory usage
- disk usage

## Why This Version Exists

This version establishes the first execution loop:

1. create a useful script
2. run it locally
3. inspect the result
4. refine based on real behavior

Current visibility path:

`machine -> sysinfo.sh -> visibility`

Future AOIS path:

`logs -> AOIS -> diagnosis -> action`

## Commands

Record the commands you actually run for this version here as work is validated.

Manual exploration commands:

```bash
top -bn1 | grep "Cpu(s)"
free -h
df -h
```

Build and run commands:

```bash
chmod +x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

## Full Script, Commented

Below is the full `scripts/sysinfo.sh` content rewritten with comments so the purpose of each part is explicit.

```bash
#!/usr/bin/env bash

# Exit immediately on errors, treat unset variables as errors,
# and fail a pipeline if any command in it fails.
set -euo pipefail

# Print a section heading like: ==== CPU ====
print_header() {
  printf '==== %s ====\n' "$1"
}

# Print the current timestamp so the report is tied to a real moment.
print_timestamp() {
  printf 'Timestamp: %s\n\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
}

# Measure CPU usage by reading /proc/stat twice and comparing the samples.
get_cpu_usage() {
  # Declare local variables used for parsing and calculation.
  local line user nice system idle iowait irq softirq steal total idle_total usage

  # Read the first CPU sample from /proc/stat.
  # The first line starts with "cpu" followed by cumulative time counters.
  read -r _ user nice system idle iowait irq softirq steal _ < /proc/stat

  # Total CPU time is the sum of all tracked CPU states.
  total=$((user + nice + system + idle + iowait + irq + softirq + steal))

  # Idle time includes both idle and iowait time.
  idle_total=$((idle + iowait))

  # Wait briefly so a second sample can show change over time.
  sleep 0.5

  # Read the second CPU sample.
  read -r _ user nice system idle iowait irq softirq steal _ < /proc/stat

  # Calculate the next totals from the second sample.
  local total_next=$((user + nice + system + idle + iowait + irq + softirq + steal))
  local idle_next=$((idle + iowait))

  # Work with the difference between samples, not the raw totals.
  local total_diff=$((total_next - total))
  local idle_diff=$((idle_next - idle_total))

  # Avoid division by zero in the unlikely case that no CPU time changed.
  if (( total_diff == 0 )); then
    usage="0.0"
  else
    # CPU usage is the non-idle fraction of the total elapsed CPU time.
    usage=$(awk -v total="$total_diff" -v idle="$idle_diff" 'BEGIN { printf "%.1f", ((total - idle) / total) * 100 }')
  fi

  # Print the final CPU usage value.
  printf 'Usage: %s%%\n' "$usage"
}

# Read memory usage from free -h and print the used and total values.
get_memory_usage() {
  awk '
    /^Mem:/ {
      printf "Used: %s / %s\n", $3, $2
    }
  ' < <(free -h)
}

# Read disk usage for the root filesystem only.
get_disk_usage() {
  df -h / | awk 'NR==2 { printf "Used: %s / %s\n", $3, $2 }'
}

# Start the report with a timestamp.
print_timestamp

# Print CPU section.
print_header "CPU"
get_cpu_usage
printf '\n'

# Print memory section.
print_header "MEMORY"
get_memory_usage
printf '\n'

# Print disk section.
print_header "DISK"
get_disk_usage
```

## Expected Behavior

The script should report:

- CPU usage
- memory usage
- disk usage

It should also print a timestamp at the top so each report is tied to a moment in time.

Example:

```text
Report generated at: 2026-04-22 12:30
```

## Interpretation

When reading the output, be able to identify:

- which value is used
- which value is available
- what would count as danger

Examples:

- memory almost full means elevated risk
- disk at 100% means failure is close or already happening

## Troubleshooting

Use this section to capture real issues only.

- Issue:
- Cause:
- Fix:

Common mistakes to watch for:

- messy or unclear output formatting
- incorrect memory parsing
- forgetting `chmod +x`
- trusting output without checking the underlying command behavior

## Mastery Check

Be able to explain, in plain language:

- what the script does
- how it gathers system information
- why running it yourself matters
- what `free -h` shows
- the difference between used and available memory
- why disk is shown per mount
- how to detect a critical system state

Answered mastery questions:

What does `free -h` show?

- total memory
- used memory
- free memory
- available memory, which is the most important signal

What is the difference between used and available memory?

- `used` includes cache and can look high even when the system is healthy
- `available` is the memory that is still safely usable and is the better metric to monitor

Why is disk shown per mount?

Because each mount is independent.

Examples:

- `/` full can crash the system
- `/data` full can break the application
- `/var` full can stop logs from being written

Each mount must be monitored separately.

How would you detect a critical system state?

Combine signals:

- CPU consistently above `80-90%`
- memory with very low available capacity, not just high used memory
- any disk mount above `90-95%`

## Question Answers

### 1. What command is used for CPU?

Command:

```bash
top -bn1 | grep "Cpu(s)"
```

What it does:

- `top` shows live system activity
- `-b` runs in batch mode
- `-n1` captures one snapshot
- `grep "Cpu(s)"` extracts the CPU line

Current script note:

The `scripts/sysinfo.sh` implementation does not use `top` for CPU usage. It reads from `/proc/stat` twice and calculates usage from the difference between the two samples.

What you see:

```text
Cpu(s): 5.3% us, 1.2% sy, 0.0% ni, 92.0% id
```

Meaning:

- `us` is user process time
- `sy` is system or kernel process time
- `id` is idle time

So:

`CPU usage = 100% - idle`

### 2. How is memory calculated?

Command:

```bash
free -h
```

Example output:

```text
              total   used   free   shared   buff/cache   available
Mem:          8.0G   2.1G   1.0G     200M        4.9G        5.3G
```

Important distinction:

- `used` is memory currently used, including cache
- `available` is memory that can still be used safely

Linux uses memory for caching to be efficient.

So:

- `used` does not automatically mean there is a problem
- `available` is the more important signal

### 3. Why is disk shown per mount?

Command:

```bash
df -h
```

Example:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   20G   30G  40% /
/dev/sdb1       100G   90G   10G  90% /data
```

Why per mount?

Because Linux does not have one single disk view. It has multiple mounted filesystems such as:

- root at `/`
- data volumes at `/data`
- logs at `/var`

Each mount can fail independently, so disk usage is reported per mount.

## Commit Target

When this version is complete, the intended commit is:

```bash
git add .
git commit -m "v0.1: sysinfo script built and understood"
git push
```

## Addendum: Simpler v0.1 Path

This addendum does not replace the curriculum above.

It exists to make the assignment easier to understand and easier to practice writing on your own.

If the main script feels too advanced, use this section as a beginner support note.

## Addendum: What You Actually Need To Learn First

For a `v0.1`, the most important skills are:

- how to run a shell script
- how to print text with `echo`
- how to run `date`
- how to run `top`, `free -h`, and `df -h /`
- how to group those commands into one script file

You do not need to memorize `/proc/stat` or write CPU math from scratch before you understand the basic idea.

## Addendum: Simple Practice Script

This is a simpler version of the system script that is easier to read and rewrite yourself.

```bash
#!/usr/bin/env bash

echo "System Report"
date
echo

echo "CPU"
top -bn1 | grep "Cpu(s)"
echo

echo "Memory"
free -h
echo

echo "Disk"
df -h /
```

## Addendum: Simple Script, Commented

```bash
#!/usr/bin/env bash

# Print a title so the output is easy to recognize.
echo "System Report"

# Print the current date and time.
date

# Print a blank line to separate sections.
echo

# Show the CPU section heading.
echo "CPU"

# Run top once in batch mode and keep only the CPU line.
top -bn1 | grep "Cpu(s)"

# Print a blank line before the next section.
echo

# Show the memory section heading.
echo "Memory"

# Show memory usage in human-readable format.
free -h

# Print a blank line before the next section.
echo

# Show the disk section heading.
echo "Disk"

# Show disk usage for the root filesystem.
df -h /
```

## Addendum: Beginner Bash Notes

### What `#!/usr/bin/env bash` means

This is the shebang.

It tells the system to run the script with `bash`.

### What `echo` does

`echo` prints text to the terminal.

Example:

```bash
echo "CPU"
```

### What `date` does

`date` prints the current date and time.

### What `top -bn1 | grep "Cpu(s)"` does

- `top -bn1` runs `top` once
- `grep "Cpu(s)"` keeps only the CPU line

You do not need to understand every CPU field yet.
At this stage, it is enough to know that this command shows CPU activity.

### What `free -h` does

It shows memory usage in a human-readable format like `MiB` or `GiB`.

### What `df -h /` does

It shows disk usage for the root filesystem `/` in a human-readable format.

## Addendum: Plain-Language Version

If you need to explain the simple script in your own words, you can say:

1. The script prints a title.
2. It prints the current date and time.
3. It shows CPU information.
4. It shows memory information.
5. It shows disk information.

That is enough for a real beginner explanation.

## Addendum: Honest v0.1 Standard

For a beginner `v0.1`, being able to do the following is already a solid result:

- make the script executable
- run it successfully
- explain what each command is doing
- explain what CPU, memory, and disk mean at a basic level
- edit the text output to make it cleaner

That is a better learning target than pretending to fully understand advanced Bash internals on day one.

Completion marker:

`v0.1 done`

## Rebuild It Yourself

You should be able to rebuild `scripts/sysinfo.sh` without AI if you understand three things:

- which command gives each system signal
- which part of the output actually matters
- how to format shell output clearly

Use this process:

1. Start with a shell script skeleton.

```bash
#!/usr/bin/env bash
set -euo pipefail
```

The first line tells the system to run the file with `bash`.
`set -euo pipefail` makes the script stricter so mistakes fail early instead of silently.

2. Add a small helper for section headers.

```bash
print_header() {
  printf '==== %s ====\n' "$1"
}
```

This gives structure to the output and makes each section easy to scan.

3. Add a timestamp function.

```bash
print_timestamp() {
  printf 'Report generated at: %s\n\n' "$(date '+%Y-%m-%d %H:%M')"
}
```

You do not need to memorize the date format. You only need to know that `date` can print the current time in a custom format.

4. Build CPU output first.

For the learning version, use:

```bash
top -bn1 | grep "Cpu(s)"
```

Why this works:

- `top` shows live system activity
- `-b` makes it printable in scripts
- `-n1` captures one snapshot
- `grep` extracts only the CPU line

Put that into a function:

```bash
get_cpu_usage() {
  top -bn1 | grep "Cpu(s)"
}
```

What matters in the output:

- `us` means user work
- `sy` means system or kernel work
- `id` means idle

The main idea is simple: high idle means low CPU pressure.

5. Build memory output next.

Run:

```bash
free -h
```

Find the `Mem:` row. That row contains the memory summary.
For a simple script, extract `used` and `total`:

```bash
get_memory_usage() {
  awk '/^Mem:/ { printf "Used: %s / %s\n", $3, $2 }' < <(free -h)
}
```

You do not need to be an `awk` expert.
Just understand:

- `/^Mem:/` means "use the line that starts with `Mem:`"
- `$3` is the third column, which is `used`
- `$2` is the second column, which is `total`

Important interpretation:

- high `used` is not automatically bad
- low `available` is the real danger signal

6. Build disk output last.

Run:

```bash
df -h
```

That shows disk usage per mount.
If you only want the root filesystem, use:

```bash
df -h /
```

Then extract the second row:

```bash
get_disk_usage() {
  df -h / | awk 'NR==2 { printf "Used: %s / %s\n", $3, $2 }'
}
```

You are reading:

- `$3` as used space
- `$2` as total space

The key concept is that Linux reports disk per mount because `/`, `/data`, and `/var` can each fill independently.

7. Call everything in order.

```bash
print_timestamp

print_header "CPU"
get_cpu_usage
printf '\n'

print_header "MEMORY"
get_memory_usage
printf '\n'

print_header "DISK"
get_disk_usage
```

This is the final assembly step. By this point, you are no longer guessing. You already know what each command returns, and you are just arranging the output.

8. Make it executable and run it.

```bash
chmod +x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

If it fails, debug one piece at a time:

- run `top -bn1 | grep "Cpu(s)"` alone
- run `free -h` alone
- run `df -h /` alone
- then test each function separately inside the script

How to work without AI:

- read the command output before writing the script
- decide which single line or columns you need
- write one function at a time
- run the script after each small change
- fix formatting only after the data is correct

The goal is not memorization. The goal is knowing how to inspect command output, choose the useful fields, and turn them into readable shell output.

## Next Step

After `v0.1` is stable, move to `v0.2`, where simple system visibility starts to break down and AI-assisted diagnosis becomes necessary.
