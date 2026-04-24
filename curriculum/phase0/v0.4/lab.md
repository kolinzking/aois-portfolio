# v0.4 Lab

Authoring status: authored

## Build Lab

Create `scripts/http_probe.sh` exactly as shown in `notes.md`.

Make it executable:

```bash
chmod +x scripts/http_probe.sh
```

Start a local server in one terminal:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Probe it from another terminal:

```bash
./scripts/http_probe.sh http://127.0.0.1:8765/
```

Success state:

- the probe prints `status=200`
- the remote IP is local
- the output includes total time and body size

## Ops Lab

Run:

```bash
curl -I http://127.0.0.1:8765/
curl -sS http://127.0.0.1:8765/ | head
./scripts/http_probe.sh http://127.0.0.1:8765/
```

Expected learning:

- headers, body, and status are separate pieces of evidence
- terminal inspection shows what a browser hides
- local HTTP behavior is enough to learn the request/response model

## Break Lab

Stop the local server and run:

```bash
./scripts/http_probe.sh http://127.0.0.1:8765/
```

Expected result:

- connection failure
- no useful HTTP status code

Restart the server and run:

```bash
./scripts/http_probe.sh http://127.0.0.1:8765/not-real
```

Expected result:

- HTTP response with a not-found status, usually `404`

Explain:

- connection failure means no HTTP response happened
- `404` means the server responded but the path was missing

## Explanation Lab

Answer:

1. what is a URL?
2. what is a port?
3. what is a status code?
4. why is connection failure different from `404`?
5. why does AOIS need HTTP inspection before FastAPI?

## Defense Lab

Defend:

`using a local HTTP server is the right first networking lab`

## Benchmark Lab

Score yourself from `1` to `5`:

- `5`: I can run, inspect, break, and explain HTTP behavior without hints.
- `4`: I can complete the lab but one concept needs review.
- `3`: I can run commands but failure classification needs help.
- `2`: I can get a response but cannot explain it.
- `1`: HTTP still feels like browser magic.

Minimum pass: `4`.
