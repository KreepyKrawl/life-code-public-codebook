# Vocabulary Ladder Calibration — Exact Cross-Domain Word-Length Landscape

**Date:** 2026-08-18  
**Status:** FROZEN CALIBRATION / SECONDARY ANALYSIS  
**Primary EXP-0001:** unchanged and NOT RUN  
**Biological annotations used:** NO

## Question

At what exact sequence length does three-domain recurrence stop being dominated by the small four-letter alphabet and begin behaving like a constrained biological signal?

The same three frozen pilot genomes were compared at every even k from 8 through 32. No genes, proteins, pathways, phenotypes, or functional annotations were used.

## Complete exact-recurrence ladder

| k | E. coli ↔ Pyrococcus | E. coli ↔ yeast | Pyrococcus ↔ yeast | all three |
|---:|---:|---:|---:|---:|
| 8 | 64,583 | 65,360 | 64,759 | 64,583 |
| 10 | 560,535 | 873,046 | 646,996 | 554,725 |
| 12 | 350,018 | 1,516,805 | 948,854 | 232,939 |
| 14 | 34,763 | 240,601 | 178,801 | 5,561 |
| 16 | 2,462 | 19,112 | 16,479 | 54 |
| 18 | 200 | 1,471 | 1,392 | 0 |
| 20 | 32 | 134 | 148 | 0 |
| 22 | 10 | 20 | 21 | 0 |
| 24 | 3 | 8 | 4 | 0 |
| 26 | 0 | 3 | 0 | 0 |
| 28 | 0 | 1 | 0 | 0 |
| 30 | 0 | 0 | 0 | 0 |
| 32 | 0 | 0 | 0 | 0 |

## Composition-preserving null challenge

Five mononucleotide-preserving and five exact dinucleotide-preserving shuffled three-genome corpora were evaluated at k = 12, 14, 16, 18, and 20.

| k | Real three-domain | Mono null range (mean) | Dinuc null range (mean) | Real / dinuc mean |
|---:|---:|---:|---:|---:|
| 12 | 232,939 | 232,777–233,462 (233,199.8) | 248,828–249,581 (249,202.0) | 0.93× |
| 14 | 5,561 | 2,247–2,328 (2,287.8) | 3,676–3,798 (3,742.6) | 1.49× |
| 16 | 54 | 6–14 (10.6) | 14–27 (19.2) | 2.81× |
| 18 | 0 | 0–0 (0.0) | 0–1 (0.2) | 0.00× |
| 20 | 0 | 0–0 (0.0) | 0–0 (0.0) | — |

## Sequence-only observation

The ladder separates into three regimes in this pilot:

1. **Short words (8–12 bp): saturation/chance-dominated.** At 8 bp almost the entire possible vocabulary is present across all three genomes. At 12 bp the real three-domain count is not elevated over the dinucleotide controls.
2. **Intermediate exact words (14–16 bp): enriched real recurrence.** The real genomes retain substantially more three-domain exact vocabulary than either composition-preserving control family. The enrichment relative to the dinucleotide null mean increases from 14 to 16 bp.
3. **Longer universal exact words (18+ bp): literal three-way identity disappears.** No exact 18–32 bp word is shared across all three real pilot genomes. Pair-specific exact words continue beyond that point, including through 28 bp in E. coli/yeast.

This is consistent with a hierarchical picture in which very short strings are too common to be informative, a narrower band retains cross-domain exact cores above compositional expectation, and longer literal identity becomes lineage/module-specific rather than universal.

## Critical boundary

This does **not** establish a universal biological word length. Three genomes are not all life, and exact identity is only the first layer of LIFE-CODE. The primary eight-genome experiment and approximate/variant grammar are separate future stages.

The five null replicates per class are intentionally reported descriptively. They are insufficient for a publication-grade tail probability and are not presented as one.

## Why this matters

The algorithm was not given a preferred k. The data themselves show where exact recurrence changes from nearly inevitable to enriched to absent across these deeply separated genomes. That empirical transition provides a principled starting scale for the eventual recursive vocabulary rather than choosing a motif length by intuition.
