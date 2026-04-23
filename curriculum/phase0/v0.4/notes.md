# v0.4 - HTTP And Network Inspection Before APIs Get Fancy

Estimated time: 3-4 focused hours

## What This Builds

You will build `scripts/http_probe.sh`, a simple inspection script that makes an HTTP request and reports the parts that matter operationally:

- method
- URL
- status code
- content type
- response headers
- response time
- body preview

This is the first AOIS component that intentionally crosses the network boundary.

## Why This Exists

Every AI system you care about is full of HTTP:

- model providers
- internal services
- health checks
- ingress paths
- cloud control planes

When one of those calls fails, you need to answer:

- did the request go out?
- what status came back?
- what headers mattered?
- was the payload what I expected?
- was this an auth problem, a path problem, or a server problem?

`v0.4` exists so that later API usage never feels like copy-paste ritual.

## AOIS Connection

The system path is now:

`URL -> HTTP request -> response -> inspection`

That is the substrate for:

- `v0.6` FastAPI
- `v0.7` raw model calls
- `v1+` model routing and AI inference

## Learning Goals

By the end of this version you should be able to:

- explain the difference between a URL, an HTTP method, a header, and a body
- read status codes without guessing what class of problem they represent
- use `curl` deliberately instead of blindly pasting it
- inspect headers and response bodies separately
- explain `scripts/http_probe.sh` line by line
- describe how HTTP debugging connects directly to later AOIS work

## Prerequisites

Run these commands first:

```bash
pwd
curl --version | head -n 1
python3 --version
```

You should confirm:

- you are inside the AOIS repo
- `curl` exists
- Python exists for later API work, even though this version is curl-first

## Core Concepts

### URL

The address of the thing you are calling.

### Method

The action you are taking.
For now, the important baseline is `GET`.

### Status Code

The coarse outcome class.

- `2xx` = success
- `3xx` = redirect
- `4xx` = client-side problem
- `5xx` = server-side problem

### Headers

Metadata about the request or response.

Examples:

- `Content-Type`
- `Authorization`
- `Server`
- `Date`

### Body

The actual payload.
It might be JSON, HTML, plain text, or nothing at all.

## Build

Inspect the new script:

```bash
sed -n '1,220p' scripts/http_probe.sh
```

Then make it executable:

```bash
chmod +x scripts/http_probe.sh
```

Run it against GitHub:

```bash
./scripts/http_probe.sh https://api.github.com
```

Expected behavior:

- you see `Status: 200`
- `Content-Type` should be JSON-like
- headers are printed
- the body preview contains JSON

The point is not to memorize GitHub's exact response.
The point is to inspect the response shape confidently.

## Ops Lab

Run these drills:

```bash
curl -I https://api.github.com
curl -s https://api.github.com | head
./scripts/http_probe.sh https://api.github.com
./scripts/http_probe.sh https://httpbin.org/status/404
```

Expected observations:

- `curl -I` shows headers only
- the plain `curl -s` call shows body only
- the probe combines the useful parts into one report
- the `404` case still returns a valid HTTP response; it is not a transport failure

## Break Lab

Cause two failure classes on purpose:

```bash
./scripts/http_probe.sh https://api.github.com/not-a-real-path
./scripts/http_probe.sh https://not-a-real-host-for-aois.invalid
```

Expected lesson:

- a real host with a bad path usually gives an HTTP status such as `404`
- a fake host fails before any valid HTTP response exists

That difference matters.
One is an application-level failure.
The other is a network or DNS failure.

## Testing

Baseline check:

```bash
./scripts/http_probe.sh https://api.github.com | grep "Status:"
./scripts/http_probe.sh https://httpbin.org/status/404 | grep "Status:"
```

Expected:

- first run shows `Status: 200`
- second run shows `Status: 404`

## Common Mistakes

### Mistake 1 - Treating all failures as “the API is down”

A `404` is not the same thing as a DNS failure.
A `401` is not the same thing as a timeout.

### Mistake 2 - Looking only at the body

Headers often tell you the real story:

- wrong content type
- auth challenge
- server identity
- cache or redirect behavior

### Mistake 3 - Using `curl` without making the method visible

If you do not know what method you sent, you are not debugging clearly.

## Troubleshooting

If the request hangs:

```bash
curl -I --max-time 10 https://api.github.com
```

If DNS fails:

- check the hostname
- compare with a known-good host like `api.github.com`

If output is too noisy:

```bash
curl -s https://api.github.com | head -20
curl -I https://api.github.com | head -20
```

## Benchmark

Measure response time:

```bash
for i in 1 2 3; do ./scripts/http_probe.sh https://api.github.com | grep "Total Time"; done
```

What matters:

- you are learning that network requests have measurable latency
- later model calls will be judged partly on this same dimension

## Architecture Defense

Why build `http_probe.sh` instead of stopping at raw `curl` examples?

- it turns repeated inspection into a concrete AOIS artifact
- it teaches response anatomy in one place
- it becomes a reusable diagnostic tool for later phases

Why not a Python client yet?

- `v0.4` is about protocol literacy first
- Python would add a second learning surface too early

## 4-Layer Tool Drill

### `curl`

1. Plain English
`curl` makes HTTP requests from the terminal.

2. System Role
It is AOIS's first direct network inspection tool.

3. Minimal Technical Definition
`curl` is a command-line client for transferring data via URLs using protocols like HTTP and HTTPS.

4. Hands-on Proof
Without `curl`, later API debugging becomes slower and more indirect.

### HTTP Status Codes

1. Plain English
They tell you what class of result came back.

2. System Role
They are the first response signal AOIS can use to decide whether a call succeeded or failed.

3. Minimal Technical Definition
They are numeric codes in the HTTP response line representing the outcome category of the request.

4. Hands-on Proof
Without status handling, you can treat `404`, `401`, and `500` as the same thing when they are not.

## 4-Level System Explanation Drill

1. Simple English
`v0.4` teaches AOIS how to talk to web services and inspect what comes back.

2. Practical Explanation
It gives you a repeatable way to send requests, inspect headers and bodies, and distinguish between wrong paths, auth issues, and host failures.

3. Technical Explanation
It adds a shell-based HTTP inspection layer using `curl`, status-code interpretation, and response metadata parsing.

4. Engineer-Level Explanation
`v0.4` establishes protocol-level debugging literacy so later FastAPI, model-provider, and cloud-service integrations can be reasoned about through request/response anatomy instead of trial-and-error.

## Failure Story

The representative failure here is misclassifying a DNS failure as an application error.

If the host cannot be resolved, there is no valid HTTP response yet.
That means you are debugging the network path, not the application route.

## Mastery Checkpoint

You are ready to leave `v0.4` when you can:

1. run `curl -I` and explain what you are looking at
2. explain the difference between headers and body
3. explain why `404` and DNS failure are different classes of problem
4. run `./scripts/http_probe.sh` and interpret every line of its output
5. explain why this version is load-bearing for later API and model work

## Connection Forward

`v0.5` moves from protocol literacy into Python systems work:

- typed models
- environment variables
- Python execution patterns

That matters because later HTTP and model work will not stay in shell scripts forever.
