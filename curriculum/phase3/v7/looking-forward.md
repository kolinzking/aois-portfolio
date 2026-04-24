# v7 Looking Forward

Authoring status: authored

## What You Should Carry Forward

- Helm packages resources
- values are deployment policy
- install mutates the cluster
- charts must preserve safety controls
- provider gates must not disappear in templates

## What The Next Version Will Build On

`v8` will build GitOps on top of this chart.

The next goal is to make desired deployment state reviewable through Git before cluster sync.
