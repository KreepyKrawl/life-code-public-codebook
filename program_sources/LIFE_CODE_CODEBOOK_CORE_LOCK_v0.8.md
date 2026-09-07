# LIFE-CODE Codebook Core Lock v0.8

**Status:** EXECUTABLE CONTINUATION CORE  
**Date:** 2026-09-04  
**EXP-0002 outcome data included:** NO

## Canonical correction
The Codebook is the scientific product. The UI is a client.

`raw genome / frozen experiment artifact -> validated ingest -> Codebook -> query/analysis engine -> UI`

No scientific fact may originate in presentation code.

## What v0.8 actually is
`LIFE_CODE_CODEBOOK_CONTINUATION_v0.8.sqlite` is a real SQLite database populated from already released LIFE-CODE calibration evidence.

It does **not** reconstruct or overwrite `LIFE_CODE_CODEBOOK_v0.0.81.zip`. That 112 MB recovered archive remains protected by its recorded SHA-256 until physically mounted and inspected.

## Implemented scientific objects
- source artifact + SHA-256 provenance
- taxa
- experiments
- PRIMITIVE / BLOCK / MODULE / FALSIFIED_MODEL objects
- graph edges: CONTAINS, HAS_MEMBER, ORDERED_NEIGHBORHOOD, EXACT_COLINEAR_SPACING
- occurrence table ready for exact genomic coordinates
- numeric measurements
- post-freeze annotations
- claims + evidence boundaries
- evidence tier/state and explicit completeness flags

## Seeded released evidence
- Proof Case 0001: 54 three-domain 16-mers, nested 24/16-bp structure, second 25-bp block, six observed A→B spacings, composition/null context and post-freeze rRNA annotation.
- Proof Case 0002: exact BLOCK_C and BLOCK_D sequences, graph membership, exact 263-bp relation, coding-coordinate/identity measurements and post-freeze FBA annotation.
- Complete 8–32 bp pairwise/all-three vocabulary ladder and composition-preserving null means.
- Complete ordered-window negative calibration with 540 / 989 / 1,395 training modules and zero held-out transfers.
- Complete tested flat-dictionary compression table for k=14,16,18,20,24.
- Exact-gap negative model as a first-class falsified object.

## Missing means missing
The exact PC0001 sequence strings are not present in the currently mounted recovery text. v0.8 therefore stores their lengths, relationships and evidence but marks the sequence fields `SEQUENCE_NOT_RECOVERED_IN_CURRENT_MOUNT`.

The database is forbidden from inventing missing sequence.

## Merge gate for v0.0.81
When the recovered old archive is mounted:
1. verify SHA-256 `081ad5bab0cb2c125297b9acb32905fca70f9d09d5e0911f75e91f5a6d9f44e2`;
2. inspect its actual schema/IDs/data;
3. diff it against this continuation database;
4. preserve historical IDs and conflicts;
5. migrate rather than overwrite;
6. only then issue a merged canonical Codebook release.
