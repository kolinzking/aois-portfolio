#!/usr/bin/env bash

set -euo pipefail

install_cron=false
interval_minutes=5

while [[ $# -gt 0 ]]; do
  case "$1" in
    --install-cron)
      install_cron=true
      shift
      ;;
    --interval-minutes)
      interval_minutes="${2:-5}"
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if ! [[ "$interval_minutes" =~ ^[0-9]+$ ]] || (( interval_minutes < 1 || interval_minutes > 59 )); then
  echo "--interval-minutes must be between 1 and 59" >&2
  exit 2
fi

repo_root="$(git rev-parse --show-toplevel)"
state_dir="$repo_root/.aois-state"
mkdir -p "$state_dir"

git -C "$repo_root" config core.hooksPath .githooks

if [[ "$install_cron" == true ]]; then
  tmp_current="$(mktemp)"
  tmp_next="$(mktemp)"
  crontab -l > "$tmp_current" 2>/dev/null || true
  sed '/# AOIS autosave start/,/# AOIS autosave end/d' "$tmp_current" > "$tmp_next"
  {
    cat "$tmp_next"
    echo "# AOIS autosave start"
    echo "*/$interval_minutes * * * * cd $repo_root && ./scripts/aois_autosave.sh --source cron --quiet >/dev/null 2>&1"
    echo "# AOIS autosave end"
  } | crontab -
  rm -f "$tmp_current" "$tmp_next"
fi

"$repo_root/scripts/aois_checkpoint.sh" \
  --source hooks-installed \
  --next "Resume from latest reader paragraph, clicked link, question source, or autosave snapshot." \
  --note "Installed AOIS git hooks path. Cron autosave enabled: $install_cron every $interval_minutes minute(s)."

