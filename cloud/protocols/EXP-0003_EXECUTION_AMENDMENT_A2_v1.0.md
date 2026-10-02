# LIFE-CODE EXP-0003 — Execution Amendment A2 v1.0

## Status

FROZEN BEFORE PRIMARY OUTCOME INSPECTION.

This amendment refines execution infrastructure for the A3 observed (`OBS`)
cells only. It does not alter the EXP-0003 hypothesis, corpus, representations,
controls, folds, null model, N1 replicate count, deterministic seeds, scoring
statistic, threshold ladder, support rules, or reveal/interpretation boundary.

## Triggering operational evidence

Execution Amendment A1 preserved scientific semantics but several A3 `OBS`
jobs still reached the A1 `350` minute GitHub-hosted job timeout. At least the
following cells terminated at that limit based on Actions metadata alone:
`RY/BC_A`, `WS/AC_B`, `MK/BC_A`, and `C02/AC_B`. One `WS/AB_C` OBS job failed
earlier during execution. No A1 OBS result artifact existed when A2 was frozen.

No A3 scientific result artifact or score value was opened or interpreted in
deciding this amendment. Only execution state, timestamps, conclusions,
artifact existence, hashes, and workflow/code metadata were inspected.

## Frozen scientific implementation

The following remain authoritative for scientific semantics:

- `cloud/scripts/exp0003_triad_transfer_prod.py`
- `cloud/scripts/exp0003_engine.py`
- `cloud/protocols/EXP-0003_PRIMARY_EXECUTION_RESOURCE_PLAN_v1.0.md`
- all previously frozen EXP-0003 orientation/null/control/preregistration records.

A2 calls the frozen production scorer's exact orientation, sharding,
`candidate_db`, and `heldout_best` functions. It does not replace those
scientific operations.

## A2 execution change

The frozen `score_fold` loop is checkpointed only at its pre-existing threshold
boundaries.

For one `representation × fold × OBS` scientific cell:

1. The exact frozen descending threshold ladder is derived.
2. A stage resumes from the next not-yet-completed threshold.
3. At most two consecutive frozen thresholds are executed in one GitHub job.
4. After each threshold, the exact frozen detail row is stored in a checkpoint.
5. If the frozen transfer condition is satisfied, the checkpoint is marked
   complete with that threshold's exact `L*`.
6. Otherwise a later stage resumes at the next threshold.
7. If the ladder is exhausted without transfer, `L*=0`, exactly as in the
   frozen scorer.
8. Completed checkpoints are mechanically carried through later workflow
   stages without recomputing or changing their scientific contents.

No threshold is changed, inserted, deleted, reordered, or selected by a human.
Automatic early stopping is the same data-dependent early stopping already
present in the frozen scorer.

## Exactness requirements

For every A2 OBS cell, the completed checkpoint must contain exactly the same:

- oriented datasets;
- reference-shard boundaries;
- MUMmer 4.0.1 command semantics;
- threshold order;
- candidate-set construction;
- unique candidate count;
- training match-record count;
- held-out longest-first membership test;
- per-threshold detail rows visited by the frozen scorer;
- stopping threshold; and
- final `L*`

as an uninterrupted call to the frozen production `score_fold`.

A pre-primary synthetic qualification must run the uninterrupted frozen scorer
and the A2 checkpoint/resume implementation on the same cases and require exact
equality of `(L*, detail)` before A2 primary OBS execution is allowed.

## Authoritative-chain rule

For A3 `OBS` only, once A2 execution is launched, A2 is the sole authoritative
observed-score chain.

A1 remains authoritative for A3 N1 execution unless separately amended.
Any A1 OBS artifact produced later is quarantined from scientific aggregation
and must not be mixed with, substituted for, or selected against A2 output.

The original pre-A1 A3 run remains failure/provenance evidence only.

## Prepared corpus carrier

A2 may reuse the same verified A3 prepared bytes already bound by A1:

- artifact: `exp0003-A3-prepared-36160342712`
- artifact ID: `10901643257`
- digest:
  `sha256:c754b105a7a9d7be1fe5a694c00f4fc0611e90601dc89b676e2716e744807cdc`

Any cache is an operational byte carrier only. Normalized FASTA hashes must be
rechecked against `cloud/FROZEN_CORPUS_BINDING.tsv` before primary execution.

## Outcome blindness

Human resource decisions may use only execution metadata: elapsed time, job
state, failure/cancellation state, CPU/RAM/disk behavior, artifact
existence/size/hash, and code/provenance metadata.

A2 checkpoints necessarily contain scientific intermediate values because
they are the computation being resumed. They may be consumed automatically by
later workflow stages but must not be opened or interpreted by the investigator
before the original preregistered completion/reveal boundary.

## Interpretation

A2 is an execution-infrastructure amendment, not a new scientific experiment
and not a reset of EXP-0003. No EUREKA status changes as a result of this
amendment alone.
