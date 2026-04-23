# v0.1 Introduction

Before you touch the AOIS signal collector, this is first a Linux version.

The center of `v0.1` should be:

- terminal orientation
- filesystem navigation
- permissions
- process awareness
- basic machine inspection

`sysinfo.sh` is the build artifact, but Linux is the main body of the lesson.

`v0.1` is the first time AOIS touches something real.

Nothing here is glamorous:

- no API
- no AI
- no database
- no container

That is why it matters.

Before AOIS can interpret incidents, route models, or automate remediation, it must first be able to inspect a machine and report what it sees.

This version teaches the first operational habit that the rest of the curriculum depends on:

inspect the underlying system before trusting any abstraction built on top of it.

## What You Will Build And Practice

You will practice:

- moving around the repo without getting lost
- reading permissions and process output
- understanding basic Linux machine signals

Then you will build:

You will build `scripts/sysinfo.sh`, a small shell script that summarizes:

- CPU
- memory
- disk
- timestamp

It is the first AOIS signal collector.

## Why This Version Exists

Every later phase assumes you can answer questions like:

- Is the machine under CPU pressure?
- Is memory actually tight or only cached?
- Is the filesystem filling up?
- Are we looking at a real machine problem or guessing?

`v0.1` gives you the first layer of that confidence by making Linux visible instead of implicit.

## How To Use This Pack

If you are in self-paced mode:

1. start with [CONTENTS.md](CONTENTS.md)
2. then open [notes.md](notes.md)
3. then run [lab.md](lab.md)
4. use [runbook.md](runbook.md) as the fast operational reference
5. finish with [summarynotes.md](summarynotes.md) and [looking-forward.md](looking-forward.md)

If you want Linux first, jump directly to:

- [Linux Orientation And Why It Matters](notes.md#linux-orientation-and-why-it-matters)
- [Filesystem And Navigation](notes.md#filesystem-and-navigation)
- [Permissions And Process Mindset](notes.md#permissions-and-process-mindset)

If I am teaching live, this file stays useful as the orientation layer.
