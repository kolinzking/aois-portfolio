#!/usr/bin/env bash

set -euo pipefail

url="${1:-https://api.github.com}"
method="${2:-GET}"

body_file="$(mktemp)"
headers_file="$(mktemp)"
metrics_file="$(mktemp)"
trap 'rm -f "$body_file" "$headers_file" "$metrics_file"' EXIT

curl -sS \
  -X "$method" \
  -D "$headers_file" \
  -o "$body_file" \
  -w 'STATUS=%{http_code}\nTIME_TOTAL=%{time_total}\nREMOTE_IP=%{remote_ip}\nSIZE_DOWNLOAD=%{size_download}\nCONTENT_TYPE=%{content_type}\n' \
  "$url" > "$metrics_file"

printf 'HTTP Probe Report\n'
printf 'URL: %s\n' "$url"
printf 'Method: %s\n' "$method"

while IFS='=' read -r key value; do
  case "$key" in
    STATUS) printf 'Status: %s\n' "$value" ;;
    TIME_TOTAL) printf 'Total Time: %ss\n' "$value" ;;
    REMOTE_IP) printf 'Remote IP: %s\n' "$value" ;;
    SIZE_DOWNLOAD) printf 'Bytes Downloaded: %s\n' "$value" ;;
    CONTENT_TYPE) printf 'Content-Type: %s\n' "${value:-unknown}" ;;
  esac
done < "$metrics_file"

server_header="$(grep -i '^server:' "$headers_file" | head -n1 | cut -d' ' -f2- | tr -d '\r')"
date_header="$(grep -i '^date:' "$headers_file" | head -n1 | cut -d' ' -f2- | tr -d '\r')"

printf 'Server Header: %s\n' "${server_header:-not-present}"
printf 'Date Header: %s\n' "${date_header:-not-present}"

printf '\nResponse Headers (first 10):\n'
head -n 10 "$headers_file"

printf '\nResponse Body Preview (first 10 lines):\n'
head -n 10 "$body_file"
