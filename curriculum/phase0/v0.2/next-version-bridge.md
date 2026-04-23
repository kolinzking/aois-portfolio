# v0.2 -> v0.3 Bridge

`v0.2` added interpretation, but it also added a new problem:

the system now has decisions worth preserving.

Once AOIS starts evolving through scripts, APIs, models, and infrastructure, you need more than the current files on disk.
You need durable engineering memory.

That is what `v0.3` introduces.

The next version is not about runtime intelligence.
It is about making AOIS development itself inspectable:

`working tree -> staging area -> commit history`

Without that layer, later progress becomes much harder to defend or recover.
