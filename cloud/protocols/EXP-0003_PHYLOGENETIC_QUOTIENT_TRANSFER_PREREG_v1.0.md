# LIFE-CODE EXP-0003 — Phylogenetic Quotient Transfer

## Status
PREREGISTERED DESIGN — freeze before any EXP-0003 quotient-transfer result is inspected.

## Authority boundary
EXP-0003 is a new experiment. It does not alter, reinterpret, or rerun EXP-0002. EXP-0002 remains immutable sealed authority.

## Source corpus
Use exactly the 26 RefSeq assemblies frozen for EXP-0002, with the same 12 triads, four ladders, three depth ordinals, and two-train/one-held-out fold structure. The cloud corpus must first pass byte-level equivalence to the frozen EXP-0002 normalized FASTA and coordinate-map hashes.

## Question
Does a lower-resolution nucleotide representation preserve more non-random held-out transferable genomic structure across phylogenetic depth than literal A/C/G/T identity?

## Frozen representations
1. ACGT native identity.
2. RY: A,G -> R; C,T -> Y.
3. MK: A,C -> M; G,T -> K.
4. WS: A,T -> W; C,G -> S.

Projection is coordinate-preserving and may not join across source ambiguity boundaries.

## Fold-level observed statistic
For representation pi, triad t, fold f:

L*(pi,t,f) = maximum exact block length generated from the two training genomes that transfers exactly to the held-out genome under the same direct-sequence orientation semantics used by the frozen transfer engine unless a separately preregistered engine-equivalence test proves another implementation exactly equivalent.

Raw L* is descriptive only and is NOT the primary cross-representation statistic because binary alphabets increase chance match length.

## Primary null
First-order Markov null (N1), generated separately for each representation and source record, preserving:
- record lengths,
- representation-specific single-symbol composition,
- first-order transition probabilities,
- record boundaries.

Null generation must destroy long-range exact transfer. Random seeds are frozen before execution.

## Sensitivity nulls
N0 composition null: preserve record lengths and single-symbol frequencies.
N2 stronger local-structure null may be added only if its algorithm is frozen before N2 results are inspected. N2 cannot replace the N1 primary inference after results are known.

## Null-adjusted fold statistic
For N null replicates:

p(pi,t,f) = (1 + count[L*null >= L*observed]) / (1 + N)

S(pi,t,f) = -log10(p(pi,t,f))

For each triad:

S(pi,t) = median across the three held-out folds.

## Primary quotient gain
G(pi,t) = S(pi,t) - S(ACGT,t)

G > 0 means the quotient retains stronger-than-null held-out transfer than native literal identity after representation-specific chance correction.

## Depth resistance
Within each ladder g:

rho(pi,g) = Spearman(depth ordinal, S(pi,g,depth))

delta_rho(pi,g) = rho(pi,g) - rho(ACGT,g)

Positive delta_rho means the quotient loses null-adjusted transfer more slowly with phylogenetic depth than native ACGT.

## Representation crossover
For each quotient and ladder:

C(pi,g) = [S(pi,g,depth3)-S(ACGT,g,depth3)] - [S(pi,g,depth1)-S(ACGT,g,depth1)]

Positive C means the quotient becomes relatively more useful at greater phylogenetic depth.

## Primary support rule
A quotient representation is supported only if ALL are true:
1. mean G(pi,t) across the 12 frozen triads is > 0;
2. mean delta_rho(pi,g) across the four frozen ladders is > 0;
3. the improvement exceeds the preregistered non-biological representation-control family;
4. no unique biological privilege is claimed unless the winning quotient separates from the other biological quotients under a preregistered comparison.

If multiple quotient representations are statistically/evidentially indistinguishable, report a representation equivalence class rather than a unique code.

## Control family
A non-biological lossy control must be frozen before primary execution. It may not be selected after quotient results are seen. At least one control must preserve output alphabet size while breaking the chemically meaningful nucleotide partition.

## Identifiability requirement
Report both transfer performance and representation identifiability. A high-performing quotient is not evidence of a unique latent biological encoding if alternative transforms yield equivalent scores.

## Claim discipline
A positive result supports only that a preregistered coarse representation preserves null-adjusted held-out transfer better than native literal identity under this protocol. It does not establish a universal biological language, a unique hidden code, a cross-domain physical mechanism, or that any one binary partition is fundamental.

## Failure is informative
Failure means the tested quotient family did not preserve transferable structure better under the frozen metric/null system. Do not rescue a failed primary hypothesis by changing nulls, folds, taxa, thresholds, or support rules after reveal.
