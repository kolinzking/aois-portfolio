#!/usr/bin/env bash

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
curriculum_dir="$repo_root/curriculum"

phase_numbers=(0 1 2 3 4 5 6 7 8 9 10)

ensure_file() {
  local path="$1"
  local content="$2"
  if [[ ! -f "$path" ]]; then
    printf '%s' "$content" > "$path"
  fi
}

for phase in "${phase_numbers[@]}"; do
  phase_dir="$curriculum_dir/phase${phase}"
  mkdir -p "$phase_dir"

  ensure_file "$phase_dir/00-introduction.md" "# Phase ${phase} Introduction

Authoring status: scaffolded

This file will introduce Phase ${phase}, define the phase objective, explain why it exists in AOIS, and describe how the versions in this phase build on one another.
"

  ensure_file "$phase_dir/CONTENTS.md" "# Phase ${phase} Contents

Authoring status: scaffolded

## Phase Files

TODO

## Phase Focus

TODO
"

  ensure_file "$phase_dir/looking-forward.md" "# Phase ${phase} Looking Forward

Authoring status: scaffolded

This file will close Phase ${phase}, summarize what was gained, identify remaining risks, and bridge to the next phase.
"
done

while IFS= read -r -d '' version_dir; do
  version_id="$(basename "$version_dir")"
  phase_id="$(basename "$(dirname "$version_dir")")"

  ensure_file "$version_dir/notes.md" "# ${version_id} - Scaffolded Lesson

Estimated time: TBD

Authoring status: scaffolded

## What This Builds

TODO

## Why This Exists

TODO

## AOIS Connection

TODO

## Learning Goals

TODO

## Prerequisites

TODO

## Core Concepts

TODO

## Build

TODO

## Ops Lab

TODO

## Break Lab

TODO

## Testing

TODO

## Common Mistakes

TODO

## Troubleshooting

TODO

## Benchmark

TODO

## Architecture Defense

TODO

## 4-Layer Tool Drill

TODO

## 4-Level System Explanation Drill

TODO

## Failure Story

TODO

## Mastery Checkpoint

TODO

## Connection Forward

TODO
"

  ensure_file "$version_dir/CONTENTS.md" "# ${version_id} Contents

Authoring status: scaffolded

## Start Here

TODO

## Topic Jumps

TODO

## Self-Paced Path

TODO
"

  ensure_file "$version_dir/introduction.md" "# ${version_id} Introduction

Authoring status: scaffolded

## What This Version Is About

TODO

## Why It Matters In AOIS

TODO

## How To Use This Version

TODO
"

  ensure_file "$version_dir/lab.md" "# ${version_id} Lab

Authoring status: scaffolded

## Build Lab

TODO

## Ops Lab

TODO

## Break Lab

TODO

## Explanation Lab

TODO

## Defense Lab

TODO
"

  ensure_file "$version_dir/runbook.md" "# ${version_id} Runbook

Authoring status: scaffolded

## Purpose

TODO

## Primary Checks

TODO

## Recovery Steps

TODO
"

  ensure_file "$version_dir/benchmark.md" "# ${version_id} Benchmark

Authoring status: scaffolded

## Measurements

TODO

## Interpretation

TODO
"

  ensure_file "$version_dir/failure-story.md" "# ${version_id} Failure Story

Authoring status: scaffolded

## Symptom

TODO

## Root Cause

TODO

## Fix

TODO

## Prevention

TODO
"

  ensure_file "$version_dir/summarynotes.md" "# ${version_id} Summary Notes

Authoring status: scaffolded

## What Was Built

TODO

## What Was Learned

TODO

## Core Limitation Or Tradeoff

TODO
"

  ensure_file "$version_dir/next-version-bridge.md" "# ${version_id} Next Version Bridge

Authoring status: scaffolded

## What This Version Unlocks

TODO

## Why The Next Version Exists

TODO
"

  ensure_file "$version_dir/looking-forward.md" "# ${version_id} Looking Forward

Authoring status: scaffolded

## What You Should Carry Forward

TODO

## What The Next Version Will Build On

TODO
"
done < <(find "$curriculum_dir" -maxdepth 2 -type d -name 'v*' -print0 | sort -z)

printf 'Curriculum corpus scaffolding complete.\n'
