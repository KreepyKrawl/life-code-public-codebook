# LIFE-CODE EXP-0003 — Phylogenetic Quotient Transfer

Status: PROTOCOL DRAFT — NO EXP-0003 SCIENTIFIC RESULT MAY BE CLAIMED FROM THIS FILE.

## Source authority

EXP-0003 reuses the frozen EXP-0002 biological corpus and triad structure. EXP-0002 remains immutable and is not rerun.

Canonical sealed EXP-0002 bundle SHA-256:

`76fb482a368af757a53688ef947d2a219280a2db8c3bc4d5bb5906bc6978a713`

## Question

Does a preregistered lower-resolution nucleotide representation preserve null-adjusted held-out genomic transfer across increasing phylogenetic depth better than native ACGT identity?

## Representations

- ACGT: native identity
- R/Y: A,G -> R; C,T -> Y
- M/K: A,C -> M; G,T -> K
- W/S: A,T -> W; C,G -> S

Mappings are deterministic and coordinate-preserving. Projection must be performed only from a normalized FASTA whose SHA-256 matches the frozen source binding.

## Fold architecture

For every frozen triad, retain the EXP-0002 folds:

- AB_C
- AC_B
- BC_A

For representation pi, triad t, and fold f, define the observed transfer frontier L*(pi,t,f) as the longest exact candidate learned from the two training genomes that transfers to the held-out genome under the frozen direct-orientation semantics selected for EXP-0003.

Raw L* values are descriptive only and MUST NOT be compared directly between four-symbol and two-symbol alphabets as the primary inference.

## Primary normalization

Each representation receives its own empirical null distribution. At minimum the primary N1 null preserves:

- record lengths,
- projected symbol composition,
- first-order transition frequencies,
- record boundaries.

For N null replicates:

p(pi,t,f) = (1 + count[L*_null >= L*_observed]) / (N + 1)

S(pi,t,f) = -log10(p(pi,t,f))

Triad score:

S(pi,t) = median over the three folds.

Quotient gain relative to native sequence:

G(pi,t) = S(pi,t) - S(ACGT,t)

## Depth-transfer statistic

Within each frozen ladder g, compute the preregistered association between depth ordinal and S(pi,g,d). Spearman rank correlation is the default candidate statistic because EXP-0002 used rank-based depth structure, but the exact support rule remains UNFROZEN until implementation validation and null-compute budgeting are complete.

Define descriptive differential depth retention:

DeltaRho(pi,g) = rho(pi,g) - rho(ACGT,g)

Positive DeltaRho means the quotient's null-adjusted transfer degrades less strongly with phylogenetic depth.

## Required controls

The experiment must distinguish a chemically meaningful quotient from generic information loss. Controls must therefore include at least one frozen transformation/null family that does not encode one of the three canonical 2+2 base partitions.

## Identifiability

A winning representation is not automatically unique. Report the performance gap and uncertainty between the best and second-best representation and preserve equivalence classes when multiple representations are statistically indistinguishable.

## Anti-drift rules

1. No taxon substitution after freeze.
2. No representation substitution after freeze.
3. No change to fold ordering after freeze.
4. No primary claim from raw binary block length.
5. No biological annotation enters discovery/scoring.
6. Failed/non-monotonic results remain in the primary table.
7. Every cloud chunk must bind inputs and outputs by SHA-256.
8. The support rule, null replicate count, random seeds, and resource plan must be frozen before the first primary EXP-0003 result is inspected.

## Current execution gate

EXP-0003 may run engineering projection tests before freeze, but those tests are PILOT/VALIDATION only. Primary scoring is blocked until the complete frozen corpus manifest, null generator, scorer, support rule, seeds, and execution plan are committed and hashed.
