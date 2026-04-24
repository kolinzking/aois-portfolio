# v15.5 Introduction

Authoring status: authored

## What This Version Is About

`v15.5` is about quantization and memory economics.

It compares FP16, INT8, and INT4 placeholder tradeoffs without quantizing or downloading a model.

## Why It Matters In AOIS

Model serving is constrained by memory and cost.

Quantization can help, but lower precision can harm quality. AOIS needs measurement before choosing smaller artifacts.

## How To Use This Version

Run the validator and simulator.

Focus on what each precision option gains in memory and what it risks in quality.
