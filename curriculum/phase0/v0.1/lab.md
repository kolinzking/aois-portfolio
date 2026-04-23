# v0.1 Lab

## Build Lab

Run:

```bash
chmod +x scripts/sysinfo.sh
./scripts/sysinfo.sh
```

Verify that the report includes:

- timestamp
- CPU
- MEMORY
- DISK

## Ops Lab

Run:

```bash
top -bn1 | grep "Cpu(s)"
free -h
df -h /
cat /proc/stat | head -n 1
./scripts/sysinfo.sh
```

Write down:

- what each command shows
- what the script summarizes
- what the script does not yet show

## Break Lab

Do one:

```bash
chmod -x scripts/sysinfo.sh
./scripts/sysinfo.sh
chmod +x scripts/sysinfo.sh
```

Or:

```bash
./scripts/sys-info.sh
```

Explain the exact failure in plain language and technical language.

## Explanation Lab

Answer for `free`:

1. What problem does it solve?
2. Where does it sit in AOIS?
3. What is it technically?
4. What happens if you remove it from your inspection toolkit?

Then explain `v0.1` at:

1. simple English
2. practical level
3. technical level
4. engineer level

## Defense Lab

Answer:

Why start AOIS with a shell script instead of a Python service or web API?
