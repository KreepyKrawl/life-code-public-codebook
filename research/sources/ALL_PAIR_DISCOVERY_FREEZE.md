# All-Pair Colinear Calibration Freeze

**Date:** 2026-08-18  
**Status:** SEQUENCE-ONLY OUTPUT FROZEN  
**Scope:** RUN-0001 calibration only; primary EXP-0001 unchanged.

The exact same annotation-blind rule used to discover/freeze Proof Case 0002 was applied unchanged to every unordered pair of the three frozen pilot genomes.

## Rule

- exact shared 16-mers
- all occurrence pairs
- identical cross-genome coordinate diagonal
- consecutive anchors collapsed to maximal exact blocks
- base entropy >= 1.5 bits/base
- report diagonals with >=2 distinct blocks
- no biological labels

## Exhaustive pair results

### ECOLI__PYRO
- unique shared 16-mers: 2,462
- anchor occurrence pairs: 2,730
- maximal blocks: 1,937
- multi-block high-complexity colinear clusters: 0

### PYRO__YEAST
- unique shared 16-mers: 16,479
- anchor occurrence pairs: 18,217
- maximal blocks: 13,016
- multi-block high-complexity colinear clusters: 2
- cluster spans (bp): 62177, 273741

### ECOLI__YEAST
- unique shared 16-mers: 19,112
- anchor occurrence pairs: 21,185
- maximal blocks: 15,245
- multi-block high-complexity colinear clusters: 6
- cluster spans (bp): 1506, 280, 136, 136, 136, 136

## Sequence-only calibration observation

The rule does not generate compact multi-block structure indiscriminately:

- E. coli / Pyrococcus: no qualifying clusters.
- Pyrococcus / yeast: two same-diagonal coincidences, but the reported blocks are separated across 62,177 bp and 273,741 bp spans.
- E. coli / yeast: six clusters. Five involve yeast mitochondrial DNA / prior Proof Case 0001 territory. The sole nuclear cluster spans only 280 bp and is the already-frozen Proof Case 0002 candidate.

No new functional interpretation is introduced by this file.

The long-span Pyrococcus/yeast outputs are retained rather than discarded. They may later serve as negative/ambiguous calibration cases.
