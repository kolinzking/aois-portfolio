# v0.4 Lab

## Build Lab

1. Make the probe executable:

```bash
chmod +x scripts/http_probe.sh
```

2. Run it against a known-good endpoint:

```bash
./scripts/http_probe.sh https://api.github.com
```

Expected behavior:

- `Status: 200`
- `Content-Type` is populated
- the first lines of the response body look like JSON

## Ops Lab

Run:

```bash
curl -I https://api.github.com
curl -s https://api.github.com | head -5
./scripts/http_probe.sh https://api.github.com
```

Answer key:

- `curl -I` prints headers only
- `curl -s ... | head -5` prints body lines only
- `http_probe.sh` combines status, metadata, and body preview into one inspection view

## Break Lab

Run:

```bash
./scripts/http_probe.sh https://api.github.com/not-a-real-path
./scripts/http_probe.sh https://not-a-real-host-for-aois.invalid
```

Expected observations:

- the bad path case still reaches a host and returns a real HTTP status
- the fake host case fails before a real HTTP response is available

Fix lesson:

- bad path: inspect route, method, or resource
- bad host: inspect DNS, hostname spelling, or network path

## Explanation Lab

Questions:

1. Why is `curl` in AOIS at all?
Answer: because the system will depend on APIs everywhere, and `curl` is the fastest direct inspection tool for request/response debugging.

2. What simpler alternative existed?
Answer: only reading docs or calling endpoints indirectly from application code.

3. Why does that stop being enough?
Answer: because once requests fail, you need a direct protocol-level debugging tool that bypasses application layers.

## Defense Lab

Why this tool:

- low friction
- universal
- real operational value

Why not Python first:

- too much indirection for the first HTTP lesson
- protocol visibility matters more than application structure at this point
