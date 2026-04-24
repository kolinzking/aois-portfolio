#!/usr/bin/env bash

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
checkpoint_file="$repo_root/.aois-state/latest-checkpoint.md"

if [[ ! -f "$checkpoint_file" ]]; then
  echo "No AOIS checkpoint found at $checkpoint_file" >&2
  exit 1
fi

cat "$checkpoint_file"
