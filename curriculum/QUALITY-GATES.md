# AOIS Quality Gates

This file turns the curriculum standard into a practical review checklist.

Use it before marking any version `authored`, `reviewed`, or `taught`.

## Version Gate

A version passes only when all checks below are true.

| Check | Pass condition |
|---|---|
| Purpose | The learner can say what capability AOIS gains from this version. |
| Prerequisites | Required prior knowledge and commands are explicit. |
| Build | A real artifact is created or a deliberate pre-automation operation is completed. |
| Ops | The learner inspects behavior using real terminal evidence. |
| Break | At least one realistic failure is triggered or analyzed. |
| Benchmark | The learner records a concrete measurement, score, or timed capability check. |
| Explanation | The 4-layer tool drill and 4-level system explanation drill are answered. |
| Defense | Tradeoffs and alternatives are named without hand-waving. |
| Recovery | The runbook can recover the most likely stuck states. |
| Continuity | The bridge to the next version is specific and accurate. |
| Status | `CORPUS-STATUS.md` matches the real state of the lesson. |

## Phase Gate

A phase passes only when:

- every version in the phase is at least `authored`
- the phase introduction explains the capability jump clearly
- the phase has a capstone or phase-level mastery check
- the phase proves a connected AOIS system change, not disconnected topic coverage
- all scripts, app code, infra, or docs referenced by the lessons exist
- the next phase depends on capabilities that were actually built or practiced

## Frontier Gate

A frontier-facing phase must also pass these checks:

- official or primary sources were checked during authoring
- source notes are dated or clearly version-independent
- the lesson separates durable principles from tool-specific behavior
- risk, cost, observability, and governance are part of the lesson, not afterthoughts
- benchmarks measure the frontier capability under at least one real constraint

## Review Verdicts

Use these verdicts during review:

- `pass`: ready for self-paced use
- `pass-with-notes`: usable, but improvement notes should be scheduled
- `revise`: do not teach yet
- `blocked`: missing artifact, missing source, or impossible to validate locally

## Minimum Evidence Per Version

Every completed version should leave behind:

- command output or expected output shape
- a failure story
- a benchmark interpretation
- a mastery checkpoint answer path
- a commit or checkpoint showing when the version was completed

The curriculum is not complete when the learner has read it.
It is complete when the learner can reproduce, explain, debug, defend, and extend the system.
