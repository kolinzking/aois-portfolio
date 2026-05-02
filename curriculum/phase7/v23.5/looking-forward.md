# v23.5 Looking Forward

Authoring status: authored

## What You Should Carry Forward

Agent quality is a system property.

Carry forward these rules:

- evaluate connected behavior, not only single functions
- keep safety-block cases critical
- keep approval cases in the corpus
- keep budget and loop-guard regressions visible
- review metric weights before changing thresholds
- do not promote runtime autonomy without a passing evaluation gate

## What The Next Version Will Build On

v23.8 will use this evaluation gate as an operational control.

The next step is runtime operations and autonomy control: deciding when an agent
can run, what mode it runs in, how it is observed, when it pauses, and how
operators disable it if evaluation or live signals degrade.
