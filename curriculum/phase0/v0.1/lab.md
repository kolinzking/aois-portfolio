# v0.1 Lab

## Build Lab

Run and interpret the Linux commands used in the lesson.

Success state:

- you can navigate the repo
- you can inspect files and permissions
- you can inspect the machine directly with Linux commands
- you can explain what the outputs mean, not just produce them

Run:

```bash
pwd
ls -la
ps aux | head -5
echo "$HOME"
echo "$PATH"
```

Minimum interpretation bar:

- point to the current directory
- distinguish file entries from directory entries in `ls -la`
- name `USER`, `PID`, `%CPU`, `%MEM`, and `COMMAND` in `ps aux`
- explain what `HOME` and `PATH` change
- classify one failure as path-related and one as permission-related

## Ops Lab

Run:

```bash
hostname
top -bn1 | grep "Cpu(s)"
free -h
df -h /
ps aux | head -5
```

Expected learning:

- Linux inspection comes before shell automation
- you should be able to say what each command is telling you
- you should be able to separate command mechanics from command meaning
- you should be able to say which outputs are tables and which are simple values

## Break Lab

Break file readability:

```bash
touch /tmp/linux-demo.txt
chmod 000 /tmp/linux-demo.txt
cat /tmp/linux-demo.txt
```

Then recover:

```bash
chmod 644 /tmp/linux-demo.txt
cat /tmp/linux-demo.txt
```

Cleanup:

```bash
rm -f /tmp/linux-demo.txt
```

Then do a path break:

```bash
cd /tmp
cd curriculum
```

Recover with:

```bash
cd /home/collins/aois-portfolio/curriculum
pwd
```

Then do a stream break:

```bash
ls /definitely-not-a-real-path 1>/tmp/out.txt 2>/tmp/err.txt || true
cat /tmp/out.txt
cat /tmp/err.txt
```

Explain:

- why the message was not written to `out.txt`
- why the failure still produced visible information

Cleanup:

```bash
rm -f /tmp/out.txt /tmp/err.txt
```

## Explanation Lab

Answer:

1. why is Linux in AOIS before AI?
2. what is the difference between visibility and interpretation?
3. why is `available` memory important?
4. why are `stdout` and `stderr` not the same thing?
5. why can `cd curriculum` fail from one directory and succeed from another?
6. why can a command be correct in syntax but wrong in operating context?

## Defense Lab

Defend:

`teaching Linux before Bash is the right decision`

## Benchmark Lab

Score yourself from `1` to `5`:

- `5`: I can inspect, recover, explain, and classify failures without hints.
- `4`: I can complete the work but one explanation still needs refinement.
- `3`: I can run commands but still need help diagnosing.
- `2`: I can copy commands but cannot explain outputs.
- `1`: I am still blind in the terminal.

Minimum pass: `4`.
