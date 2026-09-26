# UCB-0004X Execution Amendment v1.0.3

Date: 2026-09-26
Experiment: UCB-0004X
Scientific protocol version: 1.0
Prior execution patches: 1.0.1, 1.0.2
New execution patch: 1.0.3

## Classification

Infrastructure-only GitHub-hosted runner-pool fallback. No scientific parameter, scorer byte, adapter byte, target file, source interface, threshold, split, null, seed, classification rule, bridge rule, robustness rule, reveal procedure, or claim ceiling is changed.

## Trigger for amendment

The original repaired run 36275536604 on `ubuntu-latest` remained queued with no runner assignment. The v1.0.2 alternate run 36279396238 on `ubuntu-22.04` also remained queued with no runner assignment. Repository and account inspection found no active workflow jobs in the connected repositories. Because both full-VM Linux labels were unassigned before any scientific step executed, this amendment tests the separate standard public `ubuntu-slim` hosted-runner pool.

## Authorized execution-only change

Use the standard public GitHub-hosted label:

`ubuntu-slim`

instead of `ubuntu-latest` / `ubuntu-22.04`.

The frozen scientific scorer remains SHA-256:

`9dc57fe6ebdf5d92109547f1f267197d5d5caec0781562e59acfb595945df897`

The execution-only shape adapter remains SHA-256:

`d1de3c1fa482eae48cd5dc20ae2c92cdbed0738ca90ef043611709b8b746b8d5`

NumPy remains pinned to `2.1.3`. The three authorized Zenodo files and MD5 gates remain unchanged. The sealed result must not be printed or inspected before legitimate LIFE-CODE EXP-0003 source reveal.

## Scientific integrity

This fallback is authorized only because neither queued predecessor received a runner and neither produced a target numerical result. LIFE-CODE EXP-0003 remains sealed and uninspected. If `ubuntu-slim` also receives no runner, execution remains infrastructure-blocked and no scientific inference is permitted from the queue behavior.
