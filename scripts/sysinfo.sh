#!/usr/bin/env bash

set -euo pipefail

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

cpu_line() {
  top -bn1 | grep "Cpu(s)" || echo "CPU data unavailable"
}

memory_line() {
  free -h | awk 'NR==2 {print "Mem total=" $2 " used=" $3 " available=" $7}'
}

disk_line() {
  df -h / | awk 'NR==2 {print "Disk total=" $2 " used=" $3 " avail=" $4 " use=" $5}'
}

echo "AOIS system report"
echo "Timestamp: $(timestamp)"
echo "Host: $(hostname)"
echo "CPU: $(cpu_line)"
echo "MEMORY: $(memory_line)"
echo "DISK: $(disk_line)"
