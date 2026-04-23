#!/usr/bin/env bash

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
checkpoint_file="$repo_root/.aois-state/latest-checkpoint.md"

if [[ ! -f "$checkpoint_file" ]]; then
  printf 'No AOIS checkpoint found.\n' >&2
  printf 'Run scripts/aois_checkpoint.sh first.\n' >&2
  exit 1
fi

cat "$checkpoint_file"
