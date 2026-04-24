# v8 Looking Forward

Authoring status: authored

## What You Should Carry Forward

- GitOps uses Git as deployment intent
- ArgoCD sync mutates the cluster
- automated sync must be deliberate
- namespace clarity still matters
- desired state must preserve safety controls

## What The Next Version Will Build On

`v9` will build autoscaling and event-driven planning on top of the GitOps flow.

The next question is how AOIS should scale safely under changing load.
