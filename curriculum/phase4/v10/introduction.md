# v10 Introduction

Authoring status: authored

## What This Version Is About

`v10` plans a managed model layer without cloud calls.

It uses a Bedrock-style placeholder plan to teach enterprise model-provider boundaries safely.

## Why It Matters In AOIS

Managed model services are useful, but they introduce credentials, cost, network, latency, data exposure, and provider-contract risk.

AOIS must understand those boundaries before live inference.

## How To Use This Version

1. inspect the managed model plan
2. run the validator
3. explain why credentials are absent
4. explain why budget is zero
5. explain what must happen before live provider use
