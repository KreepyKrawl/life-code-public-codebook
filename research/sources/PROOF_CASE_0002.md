# Proof Case 0002 — Blind Recovery of a Conserved Metabolic Module

**Project:** LIFE-CODE  
**Date:** 2026-08-18  
**Status:** CALIBRATION / POST-FREEZE VALIDATION  
**Primary EXP-0001:** unchanged and still NOT RUN

## 1. What was frozen before annotation

The sequence-only scan compared the complete frozen *E. coli* and *S. cerevisiae* genomes without gene or functional annotations.

Among **19,112 unique exact 16-mers shared by the two genomes**, it mapped all occurrence pairs, grouped them by exact colinear coordinate offset, merged consecutive anchors into maximal exact blocks, applied a predeclared sequence-complexity floor, and found only **six** multi-block high-complexity colinear clusters.

Five involved the yeast mitochondrial chromosome and overlapped Proof Case 0001 territory.

The sole non-mitochondrial cluster was frozen before biological lookup:

### BLOCK_C
`CAGTAGAACCGGAACCACCGTGGAA` — 25 bp

### BLOCK_D
`TCTTCTTCACCACCGGT` — 17 bp

In raw genomic orientation, the block starts were exactly **263 bp apart in both genomes** and both occurrence pairs had the same genome-to-genome coordinate diagonal.

The frozen discovery files and SHA-256 hashes precede this annotation pass.

## 2. What annotation revealed afterward

The *E. coli* coordinates fall inside **fbaA (b2925 / EG10282)**, annotated as fructose-bisphosphate aldolase class II. EcoCyc places the reverse-strand gene at 3,070,165–3,071,244 on U00096.3.

The yeast coordinates fall inside **FBA1 (YKL060C)** on chromosome XI. The S288C/sacCer3 coding region is a reverse-strand 1,080-bp gene at 326,408–327,487 and encodes fructose-bisphosphate aldolase.

Published phylogenetic work independently places the *E. coli* and *S. cerevisiae* proteins in the class-II A fructose-1,6-bisphosphate aldolase family.

## 3. The stronger coordinate result

Both annotated coding regions are exactly **1,080 bp** long.

After orienting both genes in the coding direction:

- whole-gene positionwise nucleotide identity: **550/1,080 = 50.9%**
- protein identity at corresponding positions: **139/359 = 38.7%**
- the gene-start coordinate difference itself is exactly the same diagonal that the blind block-clustering algorithm discovered.

The two exact blocks land at identical coding coordinates:

| Block | Coding start (0-based), E. coli | Coding start (0-based), yeast | Codon boundary | Exact coding-oriented sequence | Complete codons encoded |
|---|---:|---:|---|---|---|
| C | 789 | 789 | yes | `TTCCACGGTGGTTCCGGTTCTACTG` | `FHGGSGST` |
| D | 534 | 534 | yes | `ACCGGTGGTGAAGAAGA` | `TGGEE` |

Thus BLOCK_C preserves **25 consecutive DNA bases exactly** at the same coding position; its first 24 bases preserve eight complete codons encoding:

`FHGGSGST`

BLOCK_D independently preserves another exact DNA segment at the same corresponding coding position.

## 4. Why this matters to LIFE-CODE

The discovery algorithm was not told:

- that either locus was a gene;
- that the genes were homologous;
- that they encoded an enzyme;
- that glycolysis existed;
- that fructose-bisphosphate aldolase existed;
- where either coding region began;
- or that the two genes happened to have the same length.

It was only asked to find exact recurring DNA and recurring spatial/colinear structure.

It nevertheless selected two exact blocks that reconstruct a known conserved enzyme-family module across a bacterium and a eukaryote.

This is a cleaner calibration than a single conserved string because the algorithm recovered **multiple separated exact blocks plus their shared coordinate architecture**.

## 5. What this does NOT prove

This does not establish that FBA homology is novel; it is well known.

It does not establish that every biological function maps to one universally conserved nucleotide sequence.

It does not convert “DNA is software” from analogy into a literal claim.

It **does** demonstrate, using the project's annotation-blind procedure, that reusable biological architecture can be recovered directly from whole-genome A/C/G/T recurrence and then independently identified afterward.

## 6. A useful third-domain contrast

The pilot archaeon, *Pyrococcus furiosus*, did not participate in this exact class-II FBA block pair. That is biologically informative rather than a failure: published work describes *P. furiosus* as using a phylogenetically unrelated archaeal class-I fructose-bisphosphate aldolase mechanism, while bacterial and lower-eukaryotic class-II A enzymes include *E. coli* and *S. cerevisiae*.

In the project's working analogy, this is compatible with:

`same broad biochemical operation -> different inherited implementation`

That statement remains an **interpretation**, not a sequence-only observation.

## Sources recorded during post-freeze annotation

- EcoCyc, *E. coli* fbaA / EG10282: U00096.3 coordinates 3,070,165–3,071,244, reverse strand.
- RegulonDB, fbaA: 1,080 bp at 3,070,165–3,071,244.
- Saccharomyces Genome Database: FBA1 / YKL060C / S000001543.
- UCSC sacCer3: FBA1 coding region chrXI:326,408–327,487, reverse strand, 1,080 bp, 359 aa.
- Pickl, Johnsen & Schönheit (2012), *Journal of Bacteriology*, doi:10.1128/JB.00200-12: phylogenetic analysis includes *E. coli* and *S. cerevisiae* class-II A FBA and contrasts archaeal class-I systems including *P. furiosus*.

## Reproducibility files

- `PROOF_CASE_0002_DISCOVERY_FREEZE.md`
- `PROOF_CASE_0002_FREEZE_SHA256.txt`
- `COLINEAR_EXACT_CLUSTERS_ECOLI_YEAST.csv`
- `annotation_pass_0002/ANNOTATION_INPUT_0002.json`
- `annotation_pass_0002/ANNOTATION_RESULT_0002.json`
- `annotation_pass_0002/annotate_candidate_0002.py`
