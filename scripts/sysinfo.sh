#!/usr/bin/env bash

set -euo pipefail

print_header() {
  printf '==== %s ====\n' "$1"
}

print_timestamp() {
  printf 'Timestamp: %s\n\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
}

get_cpu_usage() {
  local line user nice system idle iowait irq softirq steal total idle_total usage

  read -r _ user nice system idle iowait irq softirq steal _ < /proc/stat
  total=$((user + nice + system + idle + iowait + irq + softirq + steal))
  idle_total=$((idle + iowait))

  sleep 0.5

  read -r _ user nice system idle iowait irq softirq steal _ < /proc/stat
  local total_next=$((user + nice + system + idle + iowait + irq + softirq + steal))
  local idle_next=$((idle + iowait))
  local total_diff=$((total_next - total))
  local idle_diff=$((idle_next - idle_total))

  if (( total_diff == 0 )); then
    usage="0.0"
  else
    usage=$(awk -v total="$total_diff" -v idle="$idle_diff" 'BEGIN { printf "%.1f", ((total - idle) / total) * 100 }')
  fi

  printf 'Usage: %s%%\n' "$usage"
}

get_memory_usage() {
  awk '
    /^Mem:/ {
      printf "Used: %s / %s\n", $3, $2
    }
  ' < <(free -h)
}

get_disk_usage() {
  df -h / | awk 'NR==2 { printf "Used: %s / %s\n", $3, $2 }'
}

print_timestamp

print_header "CPU"
get_cpu_usage
printf '\n'

print_header "MEMORY"
get_memory_usage
printf '\n'

print_header "DISK"
get_disk_usage
