# LIFE-CODE EXP-0003 — Orientation-Aware Transfer Semantics Freeze v1.0

## Status
FROZEN BEFORE ANY EXP-0003 PRIMARY TRANSFER OUTCOME IS INSPECTED.

## Problem closed by this record
The frozen EXP-0002 transfer engine used nucleotide reverse-complement semantics directly on A/C/G/T. EXP-0003 includes lossy projections whose output symbols are recoded to A/C for vendor compatibility. Applying a vendor DNA reverse-complement operation to the projected A/C stream would be biologically and mathematically wrong because it would transform A/C to T/G rather than reverse the original nucleotide strand and then apply the frozen projection.

This record fixes the orientation rule before primary execution.

## Frozen orientation rule
For every source FASTA record `x` and representation `pi`, construct exactly two query orientations:

1. forward: `P_pi(x)`
2. reverse: `P_pi(RC(x))`

where `RC` is the ordinary DNA reverse complement on the raw A/C/G/T record and `P_pi` is the frozen EXP-0003 representation projection.

The projected reference is always `P_pi(reference_raw_record)` in its stored forward orientation.

The exact-match engine is then run in **forward-only mode** separately against the forward and reverse projected query files. The union of those match sets is the representation-aware equivalent of both-strand searching.

The vendor engine MUST NOT be allowed to reverse-complement the projected A/C stream internally.

## Why this applies to all frozen representations
For ACGT this construction is equivalent to ordinary DNA both-strand exact matching.

For RY, MK, and WS it correctly induces strand orientation from the raw DNA before quotienting.

For the 12 memory-1 controls, the projection depends on the previous raw nucleotide. Therefore no transformation of the projected output alone can in general reconstruct the reverse orientation. The reverse raw strand must be formed first, and the memory-1 projection state must restart at the record boundary exactly as frozen: virtual previous raw state `A` at the first base of each oriented record.

## Record/boundary rule
- Reverse complement each FASTA record independently.
- Never join records.
- Never carry memory-1 state across records or ambiguity boundaries.
- Record identifiers may receive an orientation suffix for execution, but source record identity and length must remain recoverable.

## Vendor command rule
For MUMmer 4.0.1, EXP-0003 transfer scoring will use the exact-match command in forward-only mode. The `-b` both-strands option used in the frozen ACGT engine is prohibited for projected EXP-0003 streams. Output-format flags may be retained, but orientation is supplied explicitly through the two projected query files above.

## Qualification requirement
Before primary execution, the implementation must pass synthetic cases for all 16 frozen representations showing that:

1. forward matches are recovered;
2. raw reverse-complement matches are recovered after `P_pi(RC(x))`;
3. a naive reverse-complement of the projected A/C stream is not used;
4. memory-1 controls restart state at oriented record boundaries;
5. vendor MUMmer forward-only maxima equal a separate brute-force exact matcher on the same synthetic cases.

No primary genomic EXP-0003 result may be inspected until this qualification passes.

## Claim boundary
This record defines execution semantics only. It contains no EXP-0003 biological outcome and does not alter sealed EXP-0002 or completed EXP-0002A.