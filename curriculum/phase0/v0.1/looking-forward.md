# v0.1 Looking Forward

`v0.1` gave AOIS the ability to observe a machine.

That means the system can now produce a signal instead of just hoping one exists.

What it still cannot do:

- interpret the signal
- classify the issue
- explain what the reading means

That is the exact gap `v0.2` is built to expose.

## What Carries Forward

From this version onward, keep these ideas:

- observation comes before interpretation
- summarized output is useful, but ground-truth commands matter more
- CPU, memory, and disk are recurring AOIS signals, not Phase 0 trivia

## Where This Reappears Later

- `v4`: container debugging still starts with resource inspection
- `v6`: k3s nodes still need Linux-level visibility
- `v16`: dashboards help, but machine symptoms still matter
- `v20+`: agents can investigate only if the underlying signals are trustworthy

## Immediate Next Move

Go to [next-version-bridge.md](next-version-bridge.md).

`v0.2` turns raw observation into the first brittle interpretation layer.
