# v0.5 Lab

## Build Lab

Inspect the actual files:

```bash
sed -n '1,200p' app/config.py
sed -n '1,220p' app/models.py
cat .env.example
```

## Ops Lab

Run:

```bash
python3 - <<'PY'
from app.config import get_settings
print(get_settings())
PY
```

Expected:

- a small settings dictionary
- `anthropic_api_key_present` and `database_url_present` will usually be `no` unless you created `.env`

## Break Lab

Run the short-log validation failure:

```bash
python3 - <<'PY'
from app.models import AnalyzeRequest
AnalyzeRequest(log="bad")
PY
```

Expected:

- validation error

## Explanation Lab

Question:
Why is `.env.example` useful before a real `.env` file exists?

Answer:
Because it documents the expected shape of configuration without leaking secrets.

## Defense Lab

Question:
Why introduce typed models before FastAPI?

Answer:
Because the service boundary becomes easier to build and reason about when the core data contracts already exist.
