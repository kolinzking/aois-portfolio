# v0.6 Lab

## Build Lab

Run the app:

```bash
uvicorn app.main:app --reload
```

## Ops Lab

Call it:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"log":"gateway returned 503"}'
```

Expected:

- valid JSON in both cases

## Break Lab

Send:

```bash
curl -s -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"log":"bad"}'
```

Expected:

- validation error

## Explanation Lab

Question:
What improved from `v0.2`?

Answer:
The system now has a real service boundary and structured output contract.

Question:
What did not improve yet?

Answer:
The interpretation logic is still brittle regex matching.

## Defense Lab

Why split `app/main.py` and `app/analysis.py`?

Because transport and analysis are different responsibilities and should be changed independently.
