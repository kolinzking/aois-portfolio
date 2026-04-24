#!/usr/bin/env bash

set -euo pipefail

source_name="manual"
active_version="unspecified"
next_step="unspecified"
note="No note recorded."

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      source_name="${2:-manual}"
      shift 2
      ;;
    --lesson|--active-version)
      active_version="${2:-unspecified}"
      shift 2
      ;;
    --next)
      next_step="${2:-unspecified}"
      shift 2
      ;;
    --note)
      note="${2:-No note recorded.}"
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

repo_root="$(git rev-parse --show-toplevel)"
state_dir="$repo_root/.aois-state"
checkpoint_file="$state_dir/latest-checkpoint.md"
history_file="$state_dir/history.log"

mkdir -p "$state_dir"

timestamp="$(date -u +"%Y-%m-%d %H:%M:%S UTC")"
branch="$(git -C "$repo_root" rev-parse --abbrev-ref HEAD)"
head_sha="$(git -C "$repo_root" rev-parse HEAD)"
last_commit="$(git -C "$repo_root" log -1 --pretty=%s)"
status_short="$(git -C "$repo_root" status --short)"

if [[ -z "$status_short" ]]; then
  status_block="clean"
else
  status_block="$status_short"
fi

cat > "$checkpoint_file" <<EOF
# AOIS Checkpoint

- Timestamp: $timestamp
- Source: $source_name
- Branch: $branch
- HEAD: $head_sha
- Last commit: $last_commit
- Active version: $active_version
- Next step: $next_step

## Working Tree

\`\`\`text
$status_block
\`\`\`

## Note

$note
EOF

printf '%s | %s | %s | %s | %s\n' \
  "$timestamp" "$source_name" "$branch" "$head_sha" "$next_step" >> "$history_file"

echo "$checkpoint_file"
