# v0.1 Lab

## Build Lab

Run and interpret the Linux commands used in the lesson.

Success state:

- you can navigate the repo
- you can inspect files and permissions
- you can inspect the machine directly with Linux commands

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

## Explanation Lab

Answer:

1. why is Linux in AOIS before AI?
2. what is the difference between visibility and interpretation?
3. why is `available` memory important?

## Defense Lab

Defend:

`teaching Linux before Bash is the right decision`
