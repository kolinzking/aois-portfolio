# v0.5 Benchmark

## Measurements

Validate a simple request 1000 times:

```bash
python3 - <<'PY'
import time
from app.models import AnalyzeRequest

start = time.perf_counter()
for _ in range(1000):
    AnalyzeRequest(log="pod OOMKilled exit code 137")
print(round(time.perf_counter() - start, 4))
PY
```

## Interpretation

Validation has a runtime cost, but it is small enough here that the safety and clarity benefits dominate.
