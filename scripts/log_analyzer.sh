#!/usr/bin/env bash

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <log message>" >&2
  exit 2
fi

message="$*"
normalized="$(printf '%s' "$message" | tr '[:upper:]' '[:lower:]')"

if [[ "$normalized" == *"oomkilled"* || "$normalized" == *"exit code 137"* ]]; then
  echo "classification=memory-pressure severity=high action='inspect memory, limits, and recent restarts'"
elif [[ "$normalized" == *"crashloopbackoff"* || "$normalized" == *"restarting"* ]]; then
  echo "classification=restart-loop severity=high action='inspect process logs and last exit reason'"
elif [[ "$normalized" == *"5xx"* || "$normalized" == *"gateway"* ]]; then
  echo "classification=service-error severity=medium action='inspect HTTP path, upstream service, and recent deploy'"
elif [[ "$normalized" == *"permission denied"* ]]; then
  echo "classification=permission-error severity=medium action='inspect path, owner, mode, and execution context'"
else
  echo "classification=unknown severity=unknown action='preserve raw message and escalate to richer analysis'"
fi
