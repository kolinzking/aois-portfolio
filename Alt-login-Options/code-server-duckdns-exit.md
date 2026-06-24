# Code-Server DuckDNS Exit Plan

Goal: stop depending on `aois.duckdns.org` for code-server access.

Current public hostname:

- `aois.duckdns.org`

Important constraint: `aois.duckdns.org` cannot be transferred away from
DuckDNS because DuckDNS owns `duckdns.org`. Leaving DuckDNS means replacing that
hostname with either a private network name or a hostname under a domain you
control.

Current local shape observed on this host:

- code-server systemd unit: `code-server@collins.service`
- code-server config: `/home/collins/.config/code-server/config.yaml`
- current bind address: `0.0.0.0:8888`
- active public ingress: Kubernetes Traefik ingress `aois/code-server`
- primary HTTPS route: `aois.duckdns.org` -> service `code-server:8888`
- backup HTTPS route: `code.46.225.235.51.nip.io` -> service
  `code-server:8888`

## Current Working Backup Path

Use this if DuckDNS fails:

- `https://code.46.225.235.51.nip.io`

The `nip.io` name works because the server IP is embedded in the hostname. It
does not require a DuckDNS account or an IP updater. It still depends on a
third-party free DNS service and on the server keeping the same public IP
address.

Verification on 2026-05-14:

- `https://code.46.225.235.51.nip.io` returns the code-server login redirect
  over HTTPS with a valid certificate.
- External checks from Spain, Poland, and the US returned `302 Found`.

## Not a Public Backup

`http://46.225.235.51:8888` responds from the server itself, but external
checks from Ukraine, the UK, and the US timed out. Treat it as not working for
public access.

Do not open port `8888` publicly unless there is no other choice. It would
expose code-server over plain HTTP, which means the code-server password would
travel without HTTPS protection.

## Best Default: Tailscale

Use this when code-server is only for you and your own devices.

Why:

- no public DNS dependency
- no public inbound web route required
- no router port forward required
- access is limited to devices in your tailnet
- works well for a private editor/admin surface

Target shape:

- Install Tailscale on the server.
- Install Tailscale on your laptop/tablet/phone.
- Bind code-server to localhost or the Tailscale interface instead of
  `0.0.0.0`.
- Remove the public DuckDNS Caddy route after Tailscale access works.

Example final code-server config:

```yaml
bind-addr: 127.0.0.1:8888
auth: password
cert: false
```

Then expose it only over Tailscale using a private route, Tailscale Serve, or an
SSH tunnel over Tailscale.

## Best Public URL: Cloudflare Tunnel + Access

Use this when you want a normal browser URL from anywhere without joining every
device to Tailscale.

Why:

- replaces DuckDNS with your own domain
- avoids inbound port forwards
- Cloudflare Access adds an identity gate before code-server

Target shape:

- Buy or use a domain you control.
- Move DNS for that domain to Cloudflare.
- Create a Cloudflare Tunnel.
- Publish a hostname such as `code.example.com`.
- Configure the tunnel service URL as `http://127.0.0.1:8888`.
- Enable Cloudflare Access for that hostname and restrict it to your email.
- After validation, remove `aois.duckdns.org` from the Kubernetes
  `aois/code-server` ingress.

## Hardening To Do Either Way

Before retiring DuckDNS, change two things:

1. Rotate the code-server password. The current password is stored in plaintext
   in the code-server config file.
2. Stop binding code-server to `0.0.0.0:8888`. Bind it to `127.0.0.1:8888` if
   Caddy, Cloudflare Tunnel, or Tailscale Serve is the only frontend.

## Cutover Checklist

1. Bring up the replacement access path.
2. Open code-server through the replacement path.
3. Confirm login and workspace access.
4. Rotate the code-server password.
5. Change code-server bind address away from `0.0.0.0`.
6. Restart `code-server@collins.service`.
7. Remove the `aois.duckdns.org` rule from the Kubernetes `aois/code-server`
   ingress only after the replacement path is confirmed.
8. Reload or restart the affected frontend if the replacement path uses one.
9. Remove the DuckDNS updater if one exists outside this user account.

## Rollback

Restore the `aois.duckdns.org` rule on the Kubernetes `aois/code-server`
ingress if the new access path fails before DuckDNS is removed.
