# Phase 2 Looking Forward

Authoring status: authored

Phase 2 established packaging and security foundations:

`container plan -> resource limits -> local security inspection -> provider gate`

## What Was Gained

- Dockerfile and Compose plan exist.
- Build context is controlled by `.dockerignore`.
- Portfolio resources use `aois-p` names.
- Container runtime is resource-gated.
- Prompt-injection signals are locally detected.
- Secret-like content is redacted.
- Provider calls remain blocked by default.

## What Is Still Missing

- approved Docker build/run validation
- image vulnerability scanning
- real secret manager integration
- authentication and authorization
- rate limiting
- Kubernetes security controls
- policy-as-code

## Phase 3 Direction

Phase 3 can begin infrastructure and GitOps only if these remain true:

- portfolio resources are clearly named
- primary AOIS stays protected
- provider calls remain gated
- secrets stay out of repo files
- resource usage is measured after every runtime step
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v5 Next Version Bridge](../v5/10-next-version-bridge.md)
- Next: [Phase 3 Start Here](../../03-phase3/00-phase-start/00-start-here.md)
<!-- AOIS-NAV-END -->
