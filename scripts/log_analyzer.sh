#!/usr/bin/env bash

message="${1:-}"

if [[ "$message" == *"OOMKilled"* ]]; then
  echo "Detected: Memory Issue"
elif [[ "$message" == *"CrashLoopBackOff"* ]]; then
  echo "Detected: Crash Issue"
elif [[ "$message" == *"5xx"* ]]; then
  echo "Detected: Server Error"
else
  echo "Detected: Unknown Issue"
fi
