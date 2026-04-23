# v0.4 Benchmark

## Measurements

Probe the same endpoint three times:

```bash
for i in 1 2 3; do ./scripts/http_probe.sh https://api.github.com | grep "Total Time"; done
```

Record the three response times.

## Interpretation

The exact numbers matter less than the lesson:

- network calls are not free
- latency varies
- later AI calls will inherit the same request/response timing concerns

This is your first small benchmark of remote-call cost in AOIS.
