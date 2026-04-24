# v0.4 Summary Notes

Authoring status: authored

## What Was Built

An HTTP probe script that inspects status, timing, content type, body size, and body preview.

## What Was Learned

HTTP is a service boundary.
The terminal can inspect requests and responses directly through `curl`.

## Core Limitation Or Tradeoff

The local server is simple on purpose.
It teaches HTTP mechanics, not production networking, TLS, DNS, authentication, or load balancing yet.
