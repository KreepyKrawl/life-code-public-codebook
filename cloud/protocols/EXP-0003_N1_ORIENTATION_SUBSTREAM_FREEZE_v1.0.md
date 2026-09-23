# LIFE-CODE EXP-0003 — N1 Orientation Substream Freeze v1.0

## Status
FROZEN BEFORE ANY EXP-0003 PRIMARY GENOMIC OUTCOME IS INSPECTED.

## Purpose
The preregistration freezes representation-specific first-order Markov N1 nulls and the cell seed schedule. The later orientation freeze requires scoring both `P_pi(x)` and `P_pi(RC(x))`. This record fixes how N1 nulls are generated for those two oriented projected streams so observed and null scoring use identical orientation structure.

## Frozen construction
For every representation `pi`, triad `t`, fold `f`, replicate `r`, source FASTA record `(name,index)`, and orientation `o in {FWD,RC}`:

1. Compute the already-frozen cell seed from:
   `LIFE_CODE|EXP-0003|N1|<pi>|<t>|<f>|<r>`
   using the first 16 SHA-256 hex characters as an unsigned 64-bit integer.
2. Form the oriented raw DNA record:
   - `FWD`: `x`
   - `RC`: `RC(x)`
3. Project that oriented raw record with the frozen representation map: `P_pi(oriented_raw)`.
4. Derive the deterministic record/orientation substream seed as:
   `cell_seed XOR u64(SHA256("<name>|<index>|<orientation>")[:16])`.
5. Fit the N1 first-order Markov generator to that one projected oriented record only and generate exactly the same record length.

The FWD and RC null streams are therefore reproducible but distinct substreams. They are never obtained by reverse-complementing a null projected output.

## Boundary rules
- Fit and generate separately for every source FASTA record.
- Never cross record or ambiguity boundaries.
- Memory-1 projection state restarts independently for each oriented raw record before N1 fitting.
- The observed scorer and the null scorer receive the same pair of explicit orientation files and use forward-only MUMmer on each.

## Why this is required
A quotient or memory-1 control generally has no invertible projected-space reverse-complement operation. Generating one projected null and attempting to derive its opposite strand would silently change the frozen representation semantics. The raw-orientation-first construction preserves the orientation rule while keeping N1 representation-specific.

## Qualification requirement
Before primary execution, synthetic tests must show deterministic FWD/RC null reproduction, record-length preservation, record-boundary isolation, representation alphabet preservation, distinct orientation substreams when source orientations differ, and identical scorer behavior for observed and null orientation-file interfaces.

## Claim boundary
This record only completes execution semantics. It does not inspect, alter, or predict any EXP-0003 primary genomic result.