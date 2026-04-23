# v0.1 Benchmark

This file is pre-authored so the learner is not blocked in self-paced mode.
You may add your own observations below it.

## Basic Timing

- CPU sample wait configured in script: `0.5s`
- Script felt: effectively instant, with the visible wait dominated by the intentional CPU sampling delay
- Output readability: good for a first operational report, but still too thin for real troubleshooting

## Resource Snapshot

- CPU usage shown: one summarized percentage
- Memory shown: used and total memory only
- Disk shown: used and total root filesystem only

## Interpretation

- Is the machine under obvious pressure?
Unknown until you compare the live numbers on your machine, but the script gives a fast first check.
- Which number is most meaningful right now?
Usually memory `available` would be one of the most meaningful signals, which is exactly why its absence is an important limitation.
- Which number could be misread by a beginner?
`used` memory, because Linux caching makes high used memory look scarier than it often is.

## Improvement Ideas

- show available memory
- show disk percentage
- support multiple mounts
- add exit codes or thresholds in later versions

## Takeaway

The benchmark lesson in `v0.1` is not speed.
It is signal quality.

The script is already useful, but it is also already incomplete.
That is good.
It teaches the correct engineering reflex:

useful first version -> inspect it -> identify the missing signals -> improve later
