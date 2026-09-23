# LIFE-CODE EXP-0003 — N1 Execution Qualification Freeze v1.0

## Status
FROZEN BEFORE ANY EXP-0003 QUOTIENT-TRANSFER OUTCOME IS INSPECTED.

## Purpose
This record closes the remaining pre-execution gate identified by the EXP-0003 preregistration and control-family freeze: the primary first-order Markov null replicate count and deterministic seed schedule.

No EXP-0003 ACGT/RY/MK/WS/control transfer result was inspected to choose these settings.

## Primary N1 replicate count
For every representation × triad × held-out fold cell, run exactly:

`N1_REPLICATES = 99`

This yields the preregistered finite-sample p estimator:

`p = (1 + count[L*null >= L*observed]) / 100`

and therefore a minimum attainable fold p-value of `0.01` and maximum fold surprisal `S = 2.0`.

The replicate count is fixed for the complete primary family. There is no outcome-dependent early stopping, extension, or selective rerun. A failed or inconvenient cell may not receive extra primary replicates after reveal.

## Resource qualification rationale
The frozen family contains native ACGT, three biological balanced binary quotients, and twelve non-biological controls across 12 triads and three held-out folds. The primary null therefore already creates a large cloud workload. N=99 provides two-decimal Monte Carlo p resolution while keeping the complete preregistered family computationally feasible for chunked cloud execution.

The selection is based on resource scale and inferential resolution, not on observed EXP-0003 outcomes.

## Deterministic seed schedule
For each primary N1 replicate `r` in `0..98`, derive a cell-specific seed from the UTF-8 string:

`LIFE_CODE|EXP-0003|N1|<representation>|<triad_id>|<fold>|<r>`

Compute SHA-256 of that exact string. Interpret the first 16 hexadecimal characters as an unsigned 64-bit integer and use that integer as the random seed.

Representations include `ACGT`, `RY`, `MK`, `WS`, and frozen control IDs `C01` through `C12`.

Fold names are exactly `AB_C`, `AC_B`, and `BC_A`.

This schedule makes every replicate reproducible without storing mutable random-state files.

## Null construction boundary
The primary N1 generator remains exactly the preregistered first-order Markov null: generate separately for each representation and source record, preserving record length and representation-specific first-order transition probabilities in the fitted generator, never crossing record/source ambiguity boundaries.

Observed and null data must pass through the same transfer-scoring implementation for a given representation. Null generation may be parallelized or chunked, but scoring semantics may not differ between observed and null cells.

## Primary-family completeness
Primary EXP-0003 inference is not complete until all required cells for all 16 representations, 12 triads, three folds, and 99 N1 replicates either complete or are explicitly recorded as execution failures. Missing inconvenient controls or quotient cells may not be silently dropped.

## Sensitivity nulls
N0 remains sensitivity-only under the original preregistration. N2 remains unavailable unless separately frozen before any N2 results are inspected. Neither may replace the N1 primary result.

## Claim boundary
This record fixes computation and randomization only. It contains no EXP-0003 scientific outcome and does not alter the already sealed EXP-0002 result or the completed EXP-0002A forensic interpretation.
