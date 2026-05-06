#!/usr/bin/env bash

set -euo pipefail

source_name="manual-autosave"
keep_count=96
quiet=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      source_name="${2:-manual-autosave}"
      shift 2
      ;;
    --keep)
      keep_count="${2:-96}"
      shift 2
      ;;
    --quiet)
      quiet=true
      shift
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

repo_root="$(git rev-parse --show-toplevel)"
state_dir="$repo_root/.aois-state"
autosave_dir="$state_dir/autosaves"
timestamp="$(date -u +"%Y%m%dT%H%M%SZ")"
snapshot_dir="$autosave_dir/$timestamp"
latest_file="$state_dir/latest-autosave.md"

mkdir -p "$snapshot_dir"

branch="$(git -C "$repo_root" rev-parse --abbrev-ref HEAD)"
head_sha="$(git -C "$repo_root" rev-parse HEAD)"
last_commit="$(git -C "$repo_root" log -1 --pretty=%s)"

git -C "$repo_root" status --short --branch > "$snapshot_dir/status.txt"
git -C "$repo_root" diff --binary > "$snapshot_dir/unstaged.diff"
git -C "$repo_root" diff --cached --binary > "$snapshot_dir/staged.diff"
git -C "$repo_root" ls-files --others --exclude-standard -z > "$snapshot_dir/untracked-files.null"
tr '\0' '\n' < "$snapshot_dir/untracked-files.null" > "$snapshot_dir/untracked-files.txt"

if [[ -s "$snapshot_dir/untracked-files.null" ]]; then
  tar --null -czf "$snapshot_dir/untracked-files.tar.gz" \
    -C "$repo_root" \
    -T "$snapshot_dir/untracked-files.null"
fi

cat > "$snapshot_dir/metadata.txt" <<EOF
timestamp=$timestamp
source=$source_name
branch=$branch
head=$head_sha
last_commit=$last_commit
repo=$repo_root
EOF

cat > "$latest_file" <<EOF
# AOIS Autosave Snapshot

- Timestamp: $timestamp
- Source: $source_name
- Branch: $branch
- HEAD: $head_sha
- Snapshot: $snapshot_dir
- Status: $snapshot_dir/status.txt
- Unstaged diff: $snapshot_dir/unstaged.diff
- Staged diff: $snapshot_dir/staged.diff
- Untracked files: $snapshot_dir/untracked-files.txt
EOF

if [[ "$keep_count" =~ ^[0-9]+$ ]] && (( keep_count > 0 )); then
  mapfile -t old_snapshots < <(find "$autosave_dir" -mindepth 1 -maxdepth 1 -type d | sort -r | tail -n "+$((keep_count + 1))")
  for old_snapshot in "${old_snapshots[@]}"; do
    case "$old_snapshot" in
      "$autosave_dir"/*)
        rm -rf "$old_snapshot"
        ;;
    esac
  done
fi

"$repo_root/scripts/aois_checkpoint.sh" \
  --source "$source_name" \
  --next "Resume from latest reader position or autosave snapshot." \
  --note "Autosave snapshot written to $snapshot_dir" >/dev/null || true

if [[ "$quiet" != true ]]; then
  echo "$snapshot_dir"
fi
