# v12 Introduction

Authoring status: authored

## What This Version Is About

`v12` is about managed-runtime governance.

It answers one question:

Before AOIS creates managed cloud runtime infrastructure, what controls must already exist?

The plan covers:

- managed Kubernetes/runtime placeholders
- IAM boundaries
- workload identity
- observability
- cost controls
- operational controls
- primary AOIS separation

## Why It Matters In AOIS

Managed infrastructure reduces some operational burden, but it does not remove responsibility.

If AOIS creates a managed cluster without budget limits, IAM review, observability, rollback, and clear naming, the result is still fragile infrastructure.

This project also shares a server and possibly future provider accounts with primary AOIS. That means the portfolio must remain visibly separate as `aois-p`.

## How To Use This Version

Use this version as a governance checklist and break lab.

Run the local validator, inspect every required control, and practice explaining why the plan rejects live cloud approval.

Do not create cloud runtime resources during this lesson.
