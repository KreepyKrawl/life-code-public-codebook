# LIFE-CODE EXP-0003 — Execution Amendment A1 v1.0

## Status

FROZEN BEFORE PRIMARY OUTCOME INSPECTION.

This amendment repairs execution infrastructure only. It does not alter the
EXP-0003 hypothesis, corpus, representations, controls, folds, N1 replicate
count, replicate IDs, deterministic seeds, scoring statistic, threshold ladder,
support rules, or reveal/interpretation boundary.

## Triggering operational evidence

The original A3 primary workflow run is GitHub Actions run `36160342712`,
bound to commit `ad5a3fcd81eeee8419981f213e5d86b8feeba023`.

Before this amendment was written, execution metadata showed repeated score-job
termination at the GitHub-hosted 360-minute wall-clock limit, including both
N1 chunks and observed (`OBS`) cells. The A3 run artifact inventory contained
only the prepared-corpus artifact and no completed A3 score artifact.

No A3 scientific result artifact was opened or interpreted in deciding this
amendment. Runtime, cancellation state, logs, artifact names, hashes, sizes,
and existence/nonexistence were inspected as permitted by the frozen
outcome-blind resource rule.

## Frozen scientific implementation

The following pre-amendment files remain authoritative for scientific semantics:

- `cloud/scripts/exp0003_triad_transfer_prod.py`
- `cloud/scripts/exp0003_engine.py`
- `cloud/protocols/EXP-0003_PRIMARY_EXECUTION_RESOURCE_PLAN_v1.0.md`
- all previously frozen EXP-0003 orientation/null/control/preregistration records.

The production scorer itself is not replaced. Amendment A1 adds an execution
adapter that delegates scientific operations to the frozen scorer and changes
only scheduling of independent MUMmer calls.

## A1 execution changes

1. Independent training reference-shard/query-orientation MUMmer calls may run
   concurrently on the same GitHub-hosted runner.
2. Independent held-out shard membership tests for a fixed candidate batch and
   fixed length may run concurrently.
3. The frozen 25/25/25/24 N1 chunks may be transported as deterministic
   five-replicate execution packets. Packets are mechanically merged back into
   the original frozen chunk boundaries before any scientific aggregation.
4. `OBS` remains one scientific score; only its internal independent MUMmer
   calls are parallelized.
5. Reference sharding remains exactly the frozen production default. No
   within-record sequence split is introduced.
6. The exact MUMmer version remains 4.0.1.
7. A synthetic parity gate must compare the frozen serial scorer and A1
   parallel adapter before any A1 primary packet is allowed to execute.

## Exactness requirements

For every scientific score, A1 must preserve:

- the same oriented datasets;
- the same N1 seed derivation and replicate identity;
- the same reference-shard boundaries;
- the same MUMmer command semantics and minimum-match threshold;
- the same set union of training candidate sequences;
- the same candidate counts and match-record counts;
- the same descending candidate-length test;
- the same returned `L*`;
- the same per-threshold detail fields.

Parallel completion order and SQLite row IDs are explicitly non-scientific.
They may differ because the reducer uses set-union semantics. They may not alter
candidate membership, counts, threshold decisions, or `L*`.

## A3 authoritative-chain rule

For triad A3, once A1 primary execution is launched, A1 is the sole
authoritative A3 scoring chain. The original run `36160342712` is retained as
failure/provenance evidence only. Any score artifact that the original A3 run
might later produce is quarantined from scientific aggregation and must not be
mixed with, substituted for, or selected against A1 output.

This rule is frozen before inspecting any A3 score value and prevents
value-dependent rescue or cherry-picking.

## Prepared corpus carrier

A1 may reuse the original A3 prepared artifact
`exp0003-A3-prepared-36160342712`, artifact ID `10901643257`, whose GitHub
artifact digest is
`sha256:c754b105a7a9d7be1fe5a694c00f4fc0611e90601dc89b676e2716e744807cdc`.

Operational transport through a GitHub Actions cache is allowed only after
normalized FASTA hashes are rechecked against `cloud/FROZEN_CORPUS_BINDING.tsv`.
The cache is not scientific evidence; it is only a byte carrier. Scientific
provenance remains the frozen corpus hashes plus the original prepared-artifact
binding.

## Outcome blindness

A1 resource decisions may use only execution metadata: elapsed time, failure
state, cancellation state, CPU/RAM/disk behavior, file sizes, artifact
existence, and hashes. `L*`, `p`, `S`, `G`, `rho`, `delta_rho`, crossover, or
any other scientific outcome must remain unopened until the original
preregistered completion/reveal boundary.

## Interpretation

A1 is an execution-infrastructure amendment, not a new scientific experiment
and not a reset of EXP-0003. No EUREKA status changes as a result of this
amendment alone.
