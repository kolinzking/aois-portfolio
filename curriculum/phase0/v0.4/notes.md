# v0.4 - Networking And HTTP Inspection

Estimated time: 7-9 focused hours

Authoring status: authored

## What This Builds

This version builds first-principles HTTP inspection.

You will build `scripts/http_probe.sh`, a small wrapper around `curl` that reports:

- HTTP status code
- total request time
- remote IP when available
- content type
- response body size
- a small body preview

The core lab uses a local HTTP server so the lesson works without public internet access.

## Why This Exists

AOIS is moving toward services.

Once systems talk over HTTP, debugging changes.
You are no longer only asking:

- what file exists?
- what process is running?
- what script ran?

You are also asking:

- did a request reach the service?
- what status code came back?
- how long did the request take?
- was the response body what I expected?
- is the failure local, network, server, or client-side?

If HTTP remains vague, later FastAPI, model APIs, dashboards, agents, and cloud services become guesswork.

## AOIS Connection

The AOIS path is now:

`machine -> shell -> Git history -> local HTTP request -> service boundary visibility`

`v0.4` prepares AOIS for API work.
Before building a FastAPI service in `v0.6`, you need to understand what an HTTP request and response look like from the terminal.

## Learning Goals

By the end of this version you should be able to:

- explain client, server, request, response, URL, port, and status code
- use `curl` to inspect an HTTP endpoint
- start a local static HTTP server for testing
- distinguish connection failure from HTTP error status
- explain why `localhost` and `127.0.0.1` mean local machine access
- use `scripts/http_probe.sh` to inspect response metadata
- explain how HTTP inspection prepares AOIS for APIs, model calls, and service debugging

## Prerequisites

You should have completed:

- `v0.1` Linux inspection
- `v0.2` Bash automation
- `v0.3` Git discipline

Required commands:

```bash
pwd
git status --short
curl --version
python3 --version
```

Expected behavior:

- `pwd` shows the AOIS repo
- `git status --short` tells you whether the tree is clean or dirty
- `curl --version` confirms HTTP client tooling exists
- `python3 --version` confirms the local lab server command is available

Boundary:

- this version uses `python3 -m http.server` only as a local test server
- Python programming starts in `v0.5`

## Core Concepts

## Client And Server

A client sends a request.
A server receives the request and sends a response.

In this lesson:

- `curl` is the client
- a temporary local HTTP server is the server
- `scripts/http_probe.sh` wraps `curl` to make inspection repeatable

## URL

A URL identifies where to send a request.

Example:

```text
http://127.0.0.1:8765/
```

Parts:

- `http` is the scheme
- `127.0.0.1` is the host
- `8765` is the port
- `/` is the path

## Localhost

`127.0.0.1` means the local machine.

Use it when you want to test a service running on your own machine without relying on the public internet.

## Port

A port identifies which service on a host should receive the request.

If no process is listening on the port, the connection fails before HTTP can succeed.

That is different from an HTTP `404`.

## Status Code

HTTP status codes summarize response outcome.

Common examples:

- `200`: success
- `301` or `302`: redirect
- `400`: bad request
- `401` or `403`: auth or permission problem
- `404`: path not found
- `500`: server error
- `502` or `503`: upstream or availability problem

Status code is a signal, not the full diagnosis.

## Headers And Body

An HTTP response has metadata and content.

- headers describe the response
- body carries the content

Examples of useful headers:

- `Content-Type`
- `Content-Length`
- `Date`
- `Server`

## Build

Create or replace `scripts/http_probe.sh` with this:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <url>" >&2
  echo "example: $0 http://127.0.0.1:8765/" >&2
  exit 2
fi

url="$1"

tmp_body="$(mktemp)"
cleanup() {
  rm -f "$tmp_body"
}
trap cleanup EXIT

echo "AOIS HTTP probe"
echo "URL: $url"

curl \
  --silent \
  --show-error \
  --location \
  --output "$tmp_body" \
  --write-out 'status=%{http_code} total_time=%{time_total}s remote_ip=%{remote_ip} content_type=%{content_type}\n' \
  "$url"

bytes="$(wc -c < "$tmp_body" | tr -d ' ')"
echo "body_bytes=$bytes"

if [[ "$bytes" -gt 0 ]]; then
  echo "body_preview:"
  head -c 200 "$tmp_body"
  printf '\n'
fi
```

Make it executable:

```bash
chmod +x scripts/http_probe.sh
```

Start a local server in one terminal:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

In another terminal, run:

```bash
./scripts/http_probe.sh http://127.0.0.1:8765/
```

Expected output shape:

```text
AOIS HTTP probe
URL: http://127.0.0.1:8765/
status=200 total_time=...s remote_ip=127.0.0.1 content_type=text/html...
body_bytes=...
body_preview:
...
```

Stop the local server with `Ctrl-C` when done.

## Ops Lab

Run:

```bash
curl -I http://127.0.0.1:8765/
curl -sS http://127.0.0.1:8765/ | head
./scripts/http_probe.sh http://127.0.0.1:8765/
```

Questions:

1. Which command shows headers only?
2. Which command shows body content?
3. Which output line shows the status code?
4. What does `127.0.0.1` prove about where the server is?
5. Why is this more useful than only opening a page in a browser?

Answer key:

1. `curl -I` shows response headers.
2. `curl -sS ... | head` shows the beginning of the response body.
3. `status=200` in the probe output shows the status code.
4. The server is on the local machine.
5. Terminal inspection exposes status, headers, timing, and body evidence directly.

## Break Lab

Do not skip this.

### Option A - Connection failure

Stop the local server.

Then run:

```bash
./scripts/http_probe.sh http://127.0.0.1:8765/
```

Expected symptom:

- `curl` reports it could not connect

Lesson:

- no service is listening on that port
- this is not an HTTP `404`

False conclusion this prevents:

- "the endpoint returned an error" when no HTTP response happened at all

### Option B - Missing path

Start the local server again.

Run:

```bash
./scripts/http_probe.sh http://127.0.0.1:8765/not-real
```

Expected symptom:

- status is likely `404`
- the server responded, but the path did not exist

Lesson:

- connection succeeded
- HTTP returned an application-level not-found response

False conclusion this prevents:

- "the server is down" when only the path is wrong

## Testing

The version passes when:

1. `scripts/http_probe.sh` parses without Bash syntax errors
2. a local HTTP server can be started
3. the probe returns status and timing for `http://127.0.0.1:8765/`
4. you can distinguish connection failure from `404`
5. you can explain URL, host, port, path, headers, body, and status code
6. you can explain why HTTP inspection matters before FastAPI and model APIs

## Common Mistakes

- confusing "server not running" with HTTP `404`
- forgetting to start the local server
- probing the wrong port
- assuming browser success means you understand the request
- ignoring status code and only reading body text
- treating `localhost` as remote internet

## Troubleshooting

If the probe cannot connect:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Then retry:

```bash
./scripts/http_probe.sh http://127.0.0.1:8765/
```

If the status is `404`:

- the server is running
- the requested path does not exist
- check the URL path

If the script says usage:

- you forgot to pass a URL

If output is confusing:

- run `curl -I` for headers
- run `curl -sS URL | head` for body preview
- run the probe for combined metadata

## Benchmark

Measure:

- can you start the local server in under 60 seconds?
- can you get a `200` response from the probe?
- can you intentionally create and explain a connection failure?
- can you intentionally create and explain a `404`?
- can you identify status code, total time, content type, and body size?

Score yourself:

| Score | Meaning |
|---|---|
| 5/5 | You can run, inspect, break, and explain HTTP behavior without hints. |
| 4/5 | You can complete the lab, but one concept needs review. |
| 3/5 | You can run commands, but failure classification needs help. |
| 2/5 | You can get a response, but cannot explain it. |
| 1/5 | HTTP still feels like browser magic. |

Minimum pass: `4/5`.

## Architecture Defense

Why teach HTTP before FastAPI?

Because FastAPI is an HTTP service framework.
If you cannot inspect raw requests and responses, framework behavior becomes magic.

Why use `curl`?

Because `curl` is direct, scriptable, and common in operations work.
It shows evidence that browsers hide.

Why use a local server?

Because the core lesson should be self-contained.
Public internet access can be useful, but it should not be required to learn request and response basics.

## 4-Layer Tool Drill

Tool: `curl`

1. Plain English
`curl` sends requests and shows responses from the terminal.

2. System Role
It lets AOIS inspect service boundaries before and after APIs are built.

3. Minimal Technical Definition
`curl` is a command-line client for transferring data with URLs, including HTTP.

4. Hands-on Proof
If `curl` cannot connect, you can prove the problem is below HTTP response handling; if it returns `404`, you can prove the server responded but the path was wrong.

## 4-Level System Explanation Drill

1. Simple English
I learned how to inspect web requests from the terminal.

2. Practical Explanation
I can start a local server, send requests with `curl`, read status codes and headers, and tell whether a failure is connection-level or HTTP-level.

3. Technical Explanation
This version teaches URL structure, local host access, ports, HTTP request/response behavior, headers, body, status codes, and timing through `curl` and a Bash probe script.

4. Engineer-Level Explanation
AOIS now has service-boundary visibility: before building APIs or calling model providers, the learner can inspect HTTP behavior directly, classify connection versus application failures, and capture response metadata in repeatable terminal workflows.

## Failure Story

Representative failure:

- Symptom: the probe failed before showing a status code
- Root cause: no server was listening on `127.0.0.1:8765`
- Fix: start the local server or use the correct host and port
- Prevention: distinguish connection failure from HTTP error status
- What this taught me: not every request failure is an HTTP response

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v0.4` solve in AOIS?
2. What is a client?
3. What is a server?
4. What are the main parts of `http://127.0.0.1:8765/not-real`?
5. What is a port?
6. What is the difference between connection failure and HTTP `404`?
7. Why does `curl -I` matter?
8. Why use a local HTTP server instead of relying on public websites?
9. How does HTTP inspection prepare for FastAPI and model APIs?
10. Explain `curl` using the 4-layer tool rule.
11. Explain `v0.4` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v0.4` solve in AOIS?

It teaches service-boundary inspection.
AOIS will soon expose APIs and call model providers, so the learner must understand requests, responses, status codes, ports, and failure types.

2. What is a client?

A client sends a request.
In this lesson, `curl` and `scripts/http_probe.sh` act as clients.

3. What is a server?

A server listens for requests and sends responses.
In this lesson, `python3 -m http.server` is the temporary local server.

4. What are the main parts of `http://127.0.0.1:8765/not-real`?

- `http`: scheme
- `127.0.0.1`: host
- `8765`: port
- `/not-real`: path

5. What is a port?

A port identifies which service on a host should receive the request.
The host gets you to the machine; the port gets you to the listening service.

6. What is the difference between connection failure and HTTP `404`?

Connection failure means no HTTP response was received, often because nothing is listening or the address is unreachable.
HTTP `404` means the server did respond, but the requested path was not found.

7. Why does `curl -I` matter?

It shows response headers without downloading the full body.
That helps inspect status, content type, server metadata, and other response information quickly.

8. Why use a local HTTP server instead of relying on public websites?

A local server makes the lesson self-contained and repeatable without public internet access.
It also keeps the failure modes simple and under the learner's control.

9. How does HTTP inspection prepare for FastAPI and model APIs?

FastAPI endpoints and model APIs are reached through HTTP.
Understanding status codes, headers, body, timing, host, and port makes later API debugging evidence-based.

10. Explain `curl` using the 4-layer tool rule.

- Plain English: `curl` sends requests from the terminal.
- System Role: it lets AOIS inspect service and API boundaries.
- Minimal Technical Definition: it is a command-line data transfer client that supports HTTP and URL-based protocols.
- Hands-on Proof: it can show whether a URL connects, redirects, returns `200`, returns `404`, or fails before HTTP.

11. Explain `v0.4` using the 4-level system explanation rule.

- Simple English: I learned how to inspect HTTP requests and responses.
- Practical explanation: I can start a local server, send requests, read status codes, inspect headers, and classify failures.
- Technical explanation: `v0.4` teaches URL structure, ports, local host access, HTTP metadata, body content, and timing through `curl`.
- Engineer-level explanation: AOIS now has service-boundary visibility, which is required before building APIs, calling model providers, debugging service failures, or operating distributed systems.

## Connection Forward

`v0.4` teaches the fourth AOIS habit:

`inspect the boundary`

`v0.5` moves into Python so AOIS can start expressing system logic in maintainable application code instead of only shell scripts.

## Source Notes

This version uses stable HTTP and `curl` concepts.
No fast-moving external source is required for the core local lab.

If this version later adds TLS, DNS provider behavior, cloud load balancers, or browser security rules, add source notes for those specific systems.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v0.4 Introduction](introduction.md)
- Next: [v0.4 Lab](lab.md)
<!-- AOIS-NAV-END -->
