# v0.4 Runbook

Authoring status: authored

## Purpose

Use this runbook when HTTP probing fails or the output is confusing.

## Primary Checks

Run:

```bash
pwd
chmod +x scripts/http_probe.sh
curl --version
python3 --version
```

Start the local server:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Probe:

```bash
./scripts/http_probe.sh http://127.0.0.1:8765/
```

## Recovery Steps

If the probe cannot connect:

1. confirm the local server is running
2. confirm the port is `8765`
3. confirm the URL uses `127.0.0.1`
4. retry the probe

If the response is `404`:

1. the server is running
2. the requested path is missing
3. check the URL path

If the script prints usage:

1. pass a URL argument
2. use `http://127.0.0.1:8765/` for the local lab

If the server terminal is busy:

- that is normal
- leave it running while probing from another terminal
- stop it with `Ctrl-C` when finished
