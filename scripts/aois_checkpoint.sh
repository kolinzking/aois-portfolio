#!/usr/bin/env bash

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
state_dir="$repo_root/.aois-state"
mkdir -p "$state_dir"

source_name="manual"
active_version="unspecified"
next_step="unspecified"
note_text=""

while (($# > 0)); do
  case "$1" in
    --source)
      source_name="${2:-manual}"
      shift 2
      ;;
    --lesson)
      active_version="${2:-unspecified}"
      shift 2
      ;;
    --next)
      next_step="${2:-unspecified}"
      shift 2
      ;;
    --note)
      note_text="${2:-}"
      shift 2
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      exit 1
      ;;
  esac
done

timestamp="$(date -u '+%Y-%m-%d %H:%M:%S UTC')"
branch="$(git -C "$repo_root" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
head_commit="$(git -C "$repo_root" rev-parse HEAD 2>/dev/null || echo uncommitted)"
subject="$(git -C "$repo_root" log -1 --pretty=%s 2>/dev/null || echo 'no commits yet')"
status_output="$(git -C "$repo_root" status --short 2>/dev/null || true)"

cat > "$state_dir/latest-checkpoint.md" <<EOF
# AOIS Checkpoint

- Timestamp: $timestamp
- Source: $source_name
- Branch: $branch
- HEAD: $head_commit
- Last commit: $subject
- Active version: $active_version
- Next step: $next_step

## Working Tree

\`\`\`text
${status_output:-clean}
\`\`\`

## Note

${note_text:-No note recorded.}
EOF

printf '%s | %s | %s | %s\n' "$timestamp" "$source_name" "$head_commit" "$subject" >> "$state_dir/history.log"

printf 'Checkpoint written to %s\n' "$state_dir/latest-checkpoint.md"
