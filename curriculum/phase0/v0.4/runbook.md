# v0.4 Runbook

## Purpose

Use this runbook when an HTTP call is unclear and you need a fast answer about what actually happened on the wire.

## Primary Checks

Headers only:

```bash
curl -I https://api.github.com
```

Body only:

```bash
curl -s https://api.github.com | head -20
```

Combined AOIS probe:

```bash
./scripts/http_probe.sh https://api.github.com
```

Known failure path:

```bash
./scripts/http_probe.sh https://api.github.com/not-a-real-path
```

## Recovery Steps

If status is `4xx`:

- inspect the path
- inspect auth headers
- confirm the method

If status is `5xx`:

- inspect server-side availability
- retry carefully
- confirm the service is healthy

If the host fails before status:

- inspect DNS
- confirm the hostname
- compare against a known-good host
