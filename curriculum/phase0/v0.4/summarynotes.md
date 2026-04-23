# v0.4 Summary Notes

## What Was Built

You built `scripts/http_probe.sh`, a small AOIS network inspection tool for reading the anatomy of an HTTP response.

## What Was Learned

- HTTP is a concrete request/response protocol, not background magic
- headers and body tell different parts of the story
- status codes classify outcomes but do not replace deeper debugging
- DNS or host failures are different from HTTP failures

## Core Limitation Or Tradeoff

`v0.4` gives inspection, not application structure.
It lets you understand remote calls, but it does not yet build a Python service that serves or consumes them systematically.
