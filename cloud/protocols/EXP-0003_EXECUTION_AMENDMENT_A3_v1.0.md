# LIFE-CODE EXP-0003 — Execution Amendment A3 v1.0

## Status

FROZEN BEFORE PRIMARY OUTCOME INSPECTION.

This amendment repairs A3 N1 execution only. It does not alter the EXP-0003
hypothesis, corpus, representations, controls, folds, N1 replicate count,
replicate IDs, deterministic seeds, scoring statistic, threshold ladder,
support rules, or reveal/interpretation boundary.

## Triggering operational evidence

Execution Amendment A1 reduced the original 25/25/25/24 N1 chunks to
five-replicate packets and parallelized independent MUMmer calls. Despite that
repair, A3 N1 five-replicate jobs repeatedly reached the GitHub-hosted
350-minute execution timeout or otherwise failed, and no successful A1 A3 N1
score artifact existed when A3 was frozen.

No A3 scientific result artifact or score value was opened or interpreted in
deciding this amendment. Only workflow/job state, elapsed time,
failure/cancellation state, artifact existence, hashes, and code/provenance
metadata were inspected.

## Frozen scientific implementation

The following remain authoritative for scientific semantics:

- `cloud/scripts/exp0003_engine.py`
- `cloud/scripts/exp0003_triad_transfer_prod.py`
- all previously frozen EXP-0003 orientation/null/control/preregistration records.

A3 also reuses the A1 parallel execution adapter
`cloud/scripts/exp0003_triad_transfer_a1.py`, whose admissible change was
already restricted to scheduling of independent MUMmer calls and set-union
reduction.

## A3 execution change

A3 changes only N1 execution granularity.

For one frozen A3 N1 scientific score
`(representation, fold, replicate)`:

1. The exact frozen null-oriented datasets are regenerated from the same
   deterministic seed derivation.
2. The exact frozen descending threshold ladder is derived.
3. One workflow stage executes at most one previously uncompleted frozen
   threshold.
4. Candidate generation and held-out tests inside that threshold use the A1
   parallel adapter with the same scientific semantics.
5. After the threshold completes, the exact per-threshold detail row and
   resume index are written to a sealed checkpoint artifact.
6. If the frozen transfer condition is satisfied, the checkpoint is marked
   complete with that threshold's exact `L*`.
7. Otherwise a later workflow stage resumes at the next frozen threshold.
8. If the ladder is exhausted without transfer, `L*=0`, exactly as in the
   frozen production scorer.
9. Completed checkpoints are carried forward mechanically without recomputing
   or changing their scientific contents.
10. Final per-replicate artifacts are mechanically merged back into the
    original frozen N1 chunk boundaries `00..24`, `25..49`, `50..74`,
    and `75..98`.

No threshold is changed, inserted, deleted, reordered, or selected by a human.
Automatic early stopping is the same data-dependent early stopping already
present in the frozen scorer.

## Exactness requirements

For every A3 N1 score, the completed checkpoint must preserve:

- the same raw/normalized input bytes and hashes;
- the same representation and reverse-complement handling;
- the same N1 replicate identity and deterministic seed derivation;
- the same reference-shard boundaries;
- MUMmer 4.0.1 command semantics;
- the same frozen threshold order;
- the same candidate-set union;
- the same unique candidate count;
- the same training match-record count;
- the same held-out membership condition;
- the same transfer decision at each visited threshold;
- the same stopping threshold; and
- the same final `L*`.

Parallel completion order and SQLite row IDs are non-scientific. They may differ
only where set-union semantics guarantee identical candidate membership and
therefore identical threshold-level scientific output.

Before any A3 primary N1 checkpoint may execute, a synthetic parity gate must
compare the uninterrupted frozen production scorer with the complete A3
checkpoint/resume path on N1 cases and require exact equality of
`(L*, detail)`.

## Authoritative-chain rule

For A3 N1 only, once A3 execution is launched, A3 becomes the sole
authoritative N1 scoring chain.

A1 A3 N1 output, including any artifact produced after this freeze, is
quarantined from scientific aggregation and must not be mixed with,
substituted for, or selected against A3 output.

A2 remains the authoritative execution amendment for A3 observed (`OBS`)
scores unless separately amended.

The original pre-A1 A3 run remains failure/provenance evidence only.

## Prepared corpus carrier

A3 may reuse the same verified A3 prepared bytes:

- artifact: `exp0003-A3-prepared-36160342712`
- artifact ID: `10901643257`
- digest:
  `sha256:c754b105a7a9d7be1fe5a694c00f4fc0611e90601dc89b676e2716e744807cdc`

Any GitHub Actions cache is an operational byte carrier only. Normalized FASTA
hashes must be rechecked against `cloud/FROZEN_CORPUS_BINDING.tsv` before
primary execution.

## Outcome blindness

A3 checkpoint artifacts necessarily contain scientific intermediate values
because they are the computation being resumed. They may be consumed
automatically by later workflow stages but must not be opened or interpreted
by the investigator before the original preregistered completion/reveal
boundary.

Human resource decisions may use only execution metadata: elapsed time, job
state, failure/cancellation state, CPU/RAM/disk behavior, artifact
existence/size/hash, and code/provenance metadata.

## Interpretation

A3 is an execution-infrastructure amendment, not a new scientific experiment
and not a statistical reset of EXP-0003. No EUREKA status changes as a result
of this amendment alone.
