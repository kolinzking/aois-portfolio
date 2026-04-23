# v0.6 Summary Notes

## What Was Built

You built the first real AOIS API boundary.

## What Was Learned

- service structure and inference quality are separate concerns
- FastAPI plus Pydantic makes a strong local contract layer
- regex logic can live behind a clean API and still remain weak

## Core Limitation Or Tradeoff

The interface is now solid enough for real requests, but the intelligence is still narrow.
