# LIFE-CODE Proof Case 0001 — Annotation-Blind Recovery of an Ancient Cross-Domain Module

**Status:** CALIBRATION PROOF CASE, NOT YET A PUBLICATION CLAIM

## The simple test

Take complete DNA sequences from one bacterium, one archaeon, and one eukaryote. Do not provide genes, organs, pathways, protein names, rRNA labels, or functional annotations.

Search only the A/C/G/T strings for exact recurrence and recurring local neighborhoods.

## What the sequence-only pass found

Across the three real genomes it found:

- **54 exact unique 16-base strings shared by all three domains**;
- a 24-base block shared by E. coli and Pyrococcus containing a 16-base core also found in yeast;
- a second 25-base block recurring near that 24-base block;
- five E. coli copies and one Pyrococcus copy in which those two blocks occur about 3 kb apart.

The six observed A→B spacings are:

`3035, 2943, 3036, 3029, 2943, 2969 bp`

They occupy only a 93-bp range.

## Chance checks performed after discovery

Five composition-preserving pilot nulls per class produced substantially fewer three-domain shared 16-mers:

- observed: **54**
- mononucleotide-preserving null mean: **9.0**
- exact dinucleotide-preserving null mean: **19.8**

A separate spatial null held block counts fixed and randomized the positions of the B block in E. coli **5,000,000 times**.

Not one randomization placed a B block within 10 kb downstream of **all five** A blocks. The real data do this five times, with every spacing near 3 kb.

Because this exact block pair was selected from the pilot discovery, the Monte Carlo result is calibration evidence, not a multiple-testing-corrected publication p-value.

## Only then did we ask what the sequences were

Post-freeze annotation identified the discovered regions with the 16S/23S large ribosomal RNA organizational system; the shared yeast core falls within mitochondrial 21S large-subunit rRNA.

The method therefore rediscovered a known ancient biological module **without being told to look for it**.

## What this proves—and what it does not

It proves the pipeline can recover reusable, nested, spatially organized biological sequence structure directly from raw genomes.

It does **not** prove that the whole genome is reducible to a small instruction set, that every recurrent sequence has semantic meaning, or that the LIFE-CODE vocabulary/compression hypothesis is already confirmed.

That is what the preregistered full EXP-0001 is designed to test next.
