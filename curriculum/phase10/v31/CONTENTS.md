# v31 Contents

Authoring status: authored

## Start Here

Read in this order:

1. [introduction.md](introduction.md)
2. [notes.md](notes.md)
3. [lab.md](lab.md)
4. [runbook.md](runbook.md)
5. [failure-story.md](failure-story.md)
6. [benchmark.md](benchmark.md)
7. [summarynotes.md](summarynotes.md)
8. [looking-forward.md](looking-forward.md)
9. [next-version-bridge.md](next-version-bridge.md)

## Topic Jumps

- Multimodal contract: [notes.md](notes.md)
- Hands-on checks: [lab.md](lab.md)
- Multimodal recovery: [runbook.md](runbook.md)
- Multimodal failure mode: [failure-story.md](failure-story.md)
- Measurement: [benchmark.md](benchmark.md)
- v32 bridge: [next-version-bridge.md](next-version-bridge.md)

## Self-Paced Path

1. Inspect `frontier/aois-p/multimodal-aois.plan.json`.
2. Run `python3 examples/validate_multimodal_aois_plan.py`.
3. Run `python3 examples/simulate_multimodal_aois.py`.
4. Explain each allow, block, hold, and fallback decision.
5. Break and restore one media validation gate, one privacy gate, one accessibility gate, one evidence gate, and one fallback gate.
6. Read the bridge into v32 edge and offline inference.
