# LIFE-CODE EXP-0003 — Primary Execution Resource & Checkpoint Plan v1.0

## Status
FROZEN BEFORE PRIMARY INTERPRETATION. This record changes execution granularity only; it does not change any scientific statistic, null, seed, representation, fold, control, or support rule.

## Atomic scientific cell
A primary cell is exactly one `(representation, triad_id, fold)` combination.
Each cell contains:
- one observed `L*` score;
- exactly 99 N1 replicate `L*` scores using frozen replicate IDs `0..98`.

No cell is interpreted until all required primary cells are complete or explicitly recorded as failed.

## Chunking
For cloud execution, each cell is split into five immutable execution chunks:
- `OBS`: observed score only;
- `N1_00_24`: replicates 0..24;
- `N1_25_49`: replicates 25..49;
- `N1_50_74`: replicates 50..74;
- `N1_75_98`: replicates 75..98.

A failed chunk may be retried byte-for-byte with the same code, corpus hashes, seeds, and replicate IDs. No successful replicate may be selectively replaced because of its value.

## Matrix size
The frozen primary family contains:
`16 representations × 12 triads × 3 folds = 576 cells`.
Each cell has five execution chunks, for `2880` execution chunks total.

Triads are executed as independent cloud tranches. One triad tranche therefore contains:
`16 × 3 × 5 = 240` matrix jobs, within the GitHub Actions matrix limit.

## Corpus preparation
Each triad tranche reacquires its three frozen RefSeq assemblies once in a preparation job, verifies frozen raw SHA-256 values, runs the exact canonical v0.1.33 normalizer, verifies normalized FASTA and coordinate-map SHA-256 values, and publishes only those verified normalized FASTAs to the tranche scoring jobs.

Scoring jobs must not use unverified raw or normalized sequence data.

## Primary output discipline
Each chunk writes a machine-readable result containing exact representation, triad, fold, chunk, replicate IDs, `L*` values, code SHA bindings, and corpus hashes. Chunk artifacts are immutable evidence.

A triad aggregate may compute preregistered fold-level `p` and `S` only after all five chunks for that cell are present. Global `G`, `rho`, `delta_rho`, control maxima, crossover, and support interpretation are deferred until all 12 triads are complete.

## Failure discipline
- `fail-fast` is disabled across primary matrix jobs.
- Missing or failed chunks remain explicit failures.
- No representation/control/triad/fold is silently dropped.
- Resource exhaustion permits an identical retry only; it does not permit changing thresholds, null count, seeds, or scoring semantics after outcome generation.

## Outcome-blind resource rule
Execution order and parallelism may be changed for operational reasons without reading or ranking scientific outcomes. Runtime, memory, artifact size, and job success/failure may be inspected. Scientific `L*`, `p`, `S`, or downstream support metrics are not used to tune resources.
