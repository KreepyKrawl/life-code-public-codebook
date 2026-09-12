# Proof Case 0002 — Sequence-Only Discovery Freeze

**Status:** FROZEN BEFORE BIOLOGICAL ANNOTATION  
**Date:** 2026-08-18  
**Context:** EXP-0001 / RUN-0001 calibration extension  
**Primary EXP-0001 status:** unchanged / NOT RUN

## Annotation-blind procedure

Using only the already-frozen complete E. coli and S. cerevisiae DNA:

1. enumerate every exact shared direct-orientation 16-mer;
2. map every occurrence pair;
3. group anchors by exact colinear diagonal (`yeast position - E. coli position`);
4. collapse consecutive anchors into maximal exact blocks;
5. retain blocks with base entropy >= 1.5 bits/base;
6. report every diagonal containing at least two distinct maximal blocks.

No biological annotation was read.

## Exhaustive result

- shared unique 16-mers: **19,112**
- multi-block high-complexity colinear clusters: **6**
- complete ranking: `COLINEAR_EXACT_CLUSTERS_ECOLI_YEAST.csv`

Five of six reported clusters use yeast `chrM`, overlapping the already-frozen Proof Case 0001 calibration territory.

The sole non-`chrM` cluster is therefore frozen as **CANDIDATE-0002** before annotation.

## CANDIDATE-0002

- E. coli record: `ENA|U00096|U00096.3`
- yeast record: `chr11`
- diagonal: **-2743757**
- distinct maximal blocks: **2**
- exact bases across those blocks: **42**
- first-block-start through final-block-end span: **280 bp**

### BLOCK_C
- E. coli start0: **3070430**
- yeast start0: **326673**
- length: **25 bp**
- sequence: `CAGTAGAACCGGAACCACCGTGGAA`
- entropy: **1.850564**

### BLOCK_D
- E. coli start0: **3070693**
- yeast start0: **326936**
- length: **17 bp**
- sequence: `TCTTCTTCACCACCGGT`
- entropy: **1.783859**

## Sequence-only observation

BLOCK_D starts exactly **263 bp**
after BLOCK_C in E. coli and exactly
**263 bp**
after BLOCK_C in yeast.

Thus the raw sequence preserves:

`BLOCK_C -> 263 bp start-to-start -> BLOCK_D`

with zero offset drift between these two observed genomic copies.

## Interpretation barrier

No biological meaning is assigned in this freeze.

The next permitted operation is post-freeze annotation of these exact frozen coordinates/sequences. The result must be recorded even if it is uninteresting or contradicts the working model.
