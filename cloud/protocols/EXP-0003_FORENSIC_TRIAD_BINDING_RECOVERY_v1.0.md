# EXP-0003 — Forensic Recovery of the Lost EXP-0002 Triad Binding v1.0

## Status
FROZEN BEFORE ANY EXP-0003 PRIMARY OUTCOME IS INSPECTED.

This protocol exists only because the original authoritative `EXP0002_TRIADS.csv` has not been recovered into the current cloud repository or accessible saved Library. It is a metadata-recovery experiment, not a scientific re-analysis of EXP-0002 and not an EXP-0003 outcome analysis.

## Objective
Recover the missing mapping from frozen triad IDs

`B1,B2,B3,F1,F2,F3,P1,P2,P3,A1,A2,A3`

to the exact three frozen genome IDs originally bound by `EXP0002_TRIADS.csv`.

The recovered table, if any, MUST be labeled `FORENSIC_RECONSTRUCTION`, never represented as the original manifest.

## Hard exclusions
The recovery process MUST NOT use:

- EXP-0003 ACGT/RY/MK/WS/control outcomes;
- taxonomic closeness or biological intuition to select a triple;
- a requirement that recovered rows look monotone or support the published hierarchy;
- gene/protein annotation;
- post hoc changes to candidate universes or fingerprint thresholds after candidate results are inspected;
- the names `near`, `middle`, or `far` as a scoring signal.

The already released EXP-0002 outcome values may be used ONLY as historical fingerprints of a row whose values were fixed before this protocol.

## Frozen candidate universes
Candidate triples are unordered 3-genome subsets drawn only from the frozen seven-genome ladder for the same lineage.

### Bacteria
`B_BSUB,B_ECOLI,B_KLEB,B_MTUB,B_PAER,B_SALM,B_VCHO`

Candidate count: C(7,3)=35.

### Fungi
`F_CALB,F_CNEO,F_KLAC,F_NCRA,F_SCER,F_SPOM`

Candidate count: C(6,3)=20.

### Plants
`P_ALYR,P_ATHA,P_CRUB,P_PPAT,P_PTRI,P_SLYC`

Candidate count: C(6,3)=20.

### Animals
`A_BTAU,A_DRER,A_GGAL,A_HSAP,A_MMUL,A_MMUS,A_PTRO`

Candidate count: C(7,3)=35.

No candidate may be added or removed based on biological plausibility.

## Source-bound rows
These rows are already excluded from forensic selection because prior execution evidence independently binds them.

### A1
`A_HSAP + A_PTRO + A_MMUL`

### A2
`A_HSAP + A_MMUS + A_BTAU`

A1/A2 may be recomputed only as pipeline-validation controls. They may not be re-selected.

## Historical fingerprint classes
A candidate row may be promoted only from metrics that were defined and frozen in EXP-0002 before this forensic protocol.

Permitted fingerprints are:

1. **MAX_K fingerprint** — the full frozen MAX_K result object / exact frozen k-ladder recurrence values when available, not merely one scalar if the object contains more information.
2. **LONGEST_BLOCK fingerprint** — the exact frozen LONGEST_BLOCK transfer result under the canonical v0.1.33 semantics.
3. **ORDERED_TRANSFER fingerprint** — exact 16-mer ordered-module training/transferred values under the frozen relation when historical row values are available.
4. **EXACT_GAP fingerprint** — only if an original sealed row exposes it and the candidate implementation can reproduce the frozen metric exactly.
5. **Cryptographic artifact identity** — if candidate recomputation can reproduce an original sealed result serialization byte-for-byte under the canonical recovered implementation. This dominates all scalar metric matches.

Released LONGEST_BLOCK values alone are explicitly insufficient to promote a row.

## Minimum evidence for promotion
A row is `FORENSICALLY_RECOVERED` only if ALL are true:

1. exactly one candidate triple in the frozen candidate universe matches the historical row;
2. the match is supported by at least **two independent frozen fingerprint classes** from the list above, OR by exact cryptographic artifact identity;
3. no other candidate ties on the complete available fingerprint vector;
4. the same scoring/reproduction code is used for every candidate in that lineage;
5. the candidate search and all outcomes are preserved, including near-matches and failures.

If only one fingerprint class is available, or more than one candidate remains compatible, status is `AMBIGUOUS_BLOCKED`.

## Cross-row assignment constraint
After individual candidate scoring, the original manifest structure may be used only as a consistency check:

- each triad ID has exactly three genome IDs;
- all rows remain within their frozen lineage;
- source-bound A1/A2 remain fixed.

No optimization over the three rows in a ladder may choose a globally attractive assignment unless each row independently passes the promotion rule above.

## Canonical execution requirement
Candidate fingerprints must be produced from the cloud-reacquired raw RefSeq objects using the recovered canonical v0.1.33 normalizer and, where needed, the exact recovered production metric implementation.

If an exact production metric implementation is not available for a fingerprint class, that class is `UNAVAILABLE`; a substitute implementation does not count as independent source recovery unless an equivalence test against preserved canonical fixtures is frozen and passes first.

## Outcome-blind qualification
Before enumerating candidates, the recovery runner must:

1. verify all 26 frozen raw assembly bindings/hashes;
2. verify canonical normalized FASTA hashes where already bound;
3. reproduce A1 and A2 input bindings from their source evidence;
4. demonstrate metric-equivalence tests on canonical preserved fixtures for every fingerprint class used;
5. write a qualification record and SHA-256 before candidate scoring.

Failure of any required qualification blocks recovery.

## Output
The recovery job must emit:

- `EXP0003_TRIAD_FORENSIC_QUALIFICATION.json`
- `EXP0003_TRIAD_FORENSIC_CANDIDATES.csv`
- `EXP0003_TRIAD_FORENSIC_RESULT.json`
- `SHA256SUMS.txt`

For every unresolved triad ID, result must be one of:

- `FORENSICALLY_RECOVERED`
- `AMBIGUOUS_BLOCKED`
- `NO_MATCH_BLOCKED`
- `METRIC_UNAVAILABLE_BLOCKED`

## EXP-0003 execution gate
EXP-0003 primary transfer scoring remains blocked until all 12 rows are either:

- directly source-bound from original artifacts; or
- `FORENSICALLY_RECOVERED` under this protocol.

Any unresolved row keeps the primary experiment blocked.

## Claim boundary
A recovered binding is metadata reconstruction only. It does not add scientific support to EXP-0002, does not alter its released result, and does not count as evidence for EXP-0003.
