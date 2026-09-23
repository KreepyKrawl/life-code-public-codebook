# LIFE-CODE EXP-0003 — N1 Orientation Semantics Freeze v1.0

## Status
FROZEN BEFORE ANY EXP-0003 PRIMARY TRANSFER OUTCOME IS INSPECTED.

## Problem
Observed EXP-0003 transfer scoring uses two raw-DNA-derived projected orientations per source record:

1. `P_pi(x)`
2. `P_pi(RC(x))`

The primary N1 null is representation-specific and is generated in projected space. For quotient/control representations, a projected N1 sequence has no unique inverse raw DNA and therefore no scientifically defined DNA reverse complement. Applying DNA complement to the projected A/C compatibility alphabet is prohibited by the frozen orientation semantics.

## Frozen N1 orientation rule
For every raw A/C/G/T source record `x`, representation `pi`, cell `(triad_id, fold, replicate)`, generate **two N1 records independently**:

- forward null: fit the first-order Markov generator to `P_pi(x)` and generate a sequence of identical length;
- reverse null: fit the first-order Markov generator to `P_pi(RC(x))` and generate a sequence of identical length.

Thus observed and null scoring receive the same two-orientation interface, while each null orientation preserves its own representation-specific first-order transition structure and record length.

Never derive the reverse null by reversing, complementing, or otherwise transforming the forward null.

## Deterministic orientation-specific seed derivation
The already-frozen primary cell seed remains:

`cell_seed = first64(SHA256("LIFE_CODE|EXP-0003|N1|<representation>|<triad_id>|<fold>|<replicate>"))`

For each source FASTA record with identifier `name`, zero-based `record_index`, and orientation label exactly `FWD` or `RC`, derive:

`orientation_record_seed = cell_seed XOR first64(SHA256(name + "|" + record_index + "|" + orientation))`

where `first64` means the first 16 hexadecimal SHA-256 characters interpreted as an unsigned 64-bit integer.

This extends, rather than replaces, the frozen cell-specific seed schedule. It introduces no new random choice and is fixed before primary outcomes.

## Boundaries
- Fit/generate every FASTA record independently.
- Never join records.
- Never cross source ambiguity boundaries.
- For memory-1 controls, projection state restarts with virtual previous raw state `A` independently in each raw orientation before N1 fitting.
- N1 generation occurs after the raw-orientation projection.

## Primary inference boundary
This rule applies identically to ACGT, RY, MK, WS, and C01–C12 for all 99 frozen N1 replicates. It may not be changed after any real EXP-0003 transfer outcome is inspected.

## Claim boundary
This file defines null execution semantics only. It contains no EXP-0003 biological outcome and does not alter EXP-0002, EXP-0002A, or RCX-LCX-0001.
