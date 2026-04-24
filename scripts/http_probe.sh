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
