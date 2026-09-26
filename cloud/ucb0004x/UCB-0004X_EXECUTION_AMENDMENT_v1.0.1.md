# UCB-0004X Execution Amendment v1.0.1

Date: 2026-09-26
Scientific protocol: UCB-0004X v1.0 (unchanged)
Execution patch: v1.0.1
Prior failed GitHub Actions run: 36273814889

## Failure observed

The frozen target runner passed checkout, runner-byte verification, environment freeze, target download, and all three target MD5 checks. It then stopped before producing a target-result artifact with:

`SHAPE_MISMATCH h1=(81, 11) h2=(81, 11) U=(80, 2)`

The public Zenodo record describes h1.csv and h2.csv as 81x11 and U.csv as 81x2 at file level. The frozen CSV loader accepts numeric rows only; for the exact hash-pinned U.csv it yields 80 numeric control rows. No target score, target signature, null result, holdout result, or LIFE-CODE EXP-0003 output was inspected.

## Repair classification

Implementation / input-schema correction only. No scientific hypothesis, state threshold, operation threshold, discovery/validation/holdout split, Jeffreys alpha, null count, seeds, grammar, wrong-grammar control, identifiability rule, classification threshold, bridge mapping, or reveal rule is changed.

## Frozen repair

The original scorer remains byte-identical and must still verify as:

`9dc57fe6ebdf5d92109547f1f267197d5d5caec0781562e59acfb595945df897  cloud/ucb0004x/ucb0004x_target_runner_v1.0.py`

A separate execution-only adapter is introduced:

`d1de3c1fa482eae48cd5dc20ae2c92cdbed0738ca90ef043611709b8b746b8d5  cloud/ucb0004x/ucb0004x_target_exec_adapter_v1.0.1.py`

The adapter imports the frozen scorer and changes only the representation presented to its loader: when the exact U.csv produces 80 numeric rows at 4-second spacing, it appends one structural sentinel row at `last_time + 4 s` carrying a duplicate of the final control value. The frozen scorer immediately discards that appended final control value through its pre-existing `[:-1]` operation, leaving exactly the original 80 real control intervals for the 80 state transitions. The scorer's own timebase and sample-period checks must still pass.

## Integrity consequence

The original failed attempt remains preserved as a failed execution. The rerun is not a re-fit and does not use any observed target outcome. It is an auditable parser/shape repair made before any target result existed. UCB-0004X remains eligible for its preregistered interpretation if the amended execution completes and all other gates remain satisfied.
