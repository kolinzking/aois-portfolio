# v6.5 Looking Forward

Authoring status: authored

## What You Should Carry Forward

- pods need identity
- identity should be least privilege
- unused API tokens are risk
- network reach is part of security
- RBAC changes are live-cluster mutations after apply

## What The Next Version Will Build On

`v7` will build on the manifest set by turning it into a Helm chart.

The chart must preserve namespace, limits, provider gates, identity, and network policy controls.
