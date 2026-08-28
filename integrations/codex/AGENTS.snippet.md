# Architecture Harness checkpoint

Before significant implementation, identify a relevant graph node and run:

`arch-harness agent context --focus <relevant-node> --format json`

Use the compact result as architectural guidance. After a meaningful checkpoint and before completion, run:

`arch-harness graph refresh --format json`

`arch-harness gate --format json`

Exit 1 means correct every blocking violation and repeat. Exit 2 means run `arch-harness doctor`. Never change validated rules to force PASS; request human review when policy is obsolete.
