# v0.6 Benchmark

## Measurements

Measure local route latency:

```bash
for i in 1 2 3; do curl -s -o /dev/null -w "%{time_total}\n" http://127.0.0.1:8000/health; done
```

## Interpretation

This is the cost of the local API boundary before any model call is introduced.
It gives you a baseline that later AI routing will exceed.
