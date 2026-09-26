# UCB-0004X Execution Amendment v1.0.2

Date: 2026-09-26
Experiment: UCB-0004X
Scientific protocol version: 1.0
Prior execution patch: 1.0.1
New execution patch: 1.0.2

## Classification

Infrastructure-only runner-allocation amendment. This amendment does not change the frozen scientific protocol, target data, source interface, state encoding, operation encoding, discovery/validation/held-out splits, smoothing, transition grammar, null construction, seeds, support gates, PASS/FAIL/UNIDENTIFIABLE rules, bridge signature, specificity test, representation robustness test, reveal procedure, or claim ceiling.

## Trigger for amendment

GitHub Actions run 36275536604 remained queued with no runner assignment (`runner_id = 0`, blank runner name/group). At the same time, the repository showed multiple queued runs and no active jobs. The scientific job had not started and therefore had produced no target score or target result.

## Authorized execution-only change

The replacement execution workflow changes only the GitHub-hosted runner label from:

`ubuntu-latest`

to:

`ubuntu-22.04`

The frozen scientific scorer remains byte-identical with SHA-256:

`9dc57fe6ebdf5d92109547f1f267197d5d5caec0781562e59acfb595945df897`

The execution-only input-shape adapter remains byte-identical with SHA-256:

`d1de3c1fa482eae48cd5dc20ae2c92cdbed0738ca90ef043611709b8b746b8d5`

NumPy remains pinned to `2.1.3`. The execution environment is recorded in the sealed artifact. The three authorized Zenodo files and their frozen MD5 gates are unchanged.

## Scientific integrity

This change is permitted only because run 36275536604 never received a runner and no target numerical result was produced or inspected. LIFE-CODE EXP-0003 remains sealed and uninspected. No target result may be printed to logs; only execution status, hashes, and the seal receipt may be inspected before legitimate source reveal.

If the replacement runner also cannot be assigned, UCB-0004X remains OPEN / EXECUTION BLOCKED. No scientific interpretation is authorized from queue behavior.
