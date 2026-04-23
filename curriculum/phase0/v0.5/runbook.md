# v0.5 Runbook

## Purpose

Use this when Python config or model behavior is unclear.

## Primary Checks

```bash
sed -n '1,200p' app/config.py
sed -n '1,220p' app/models.py
cat .env.example
python3 -m py_compile app/config.py app/models.py
```

## Recovery Steps

If config values are missing:

- inspect `.env.example`
- create a local `.env`
- re-run `get_settings()`

If validation is failing:

- inspect field constraints in `app/models.py`
- compare the failing input against the model rules
