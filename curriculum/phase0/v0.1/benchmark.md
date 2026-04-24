# v0.1 Benchmark

## Measurements

Record:

- could you identify your current directory quickly?
- could you identify the machine name, CPU line, memory line, and root filesystem line?
- could you recover from the permission break without outside help?
- could you explain why the failing `ls` wrote to `err.txt` instead of `out.txt`?
- could you explain why a relative path failed and an absolute path succeeded?

## Score

Use this scale:

| Score | Meaning |
|---|---|
| 5 | Inspect, recover, explain, and classify failures without hints. |
| 4 | Complete the work with only minor explanation weakness. |
| 3 | Run commands, but need help diagnosing output. |
| 2 | Copy commands, but cannot explain outputs reliably. |
| 1 | Terminal behavior still feels opaque. |

Minimum pass: `4`.

## Interpretation

At `v0.1`, good means:

- the terminal is less opaque
- the machine is more inspectable
- Linux commands feel less like random incantations

If you still feel blind in the terminal after this benchmark, the version is not complete yet.

## Next Measurement

In `v0.2`, measure whether Bash automation reduces repeated typing without hiding the Linux commands you learned here.
