# ANNOTATION PASS 0001 — Performed After Raw Freeze

**Raw freeze file:** `FREEZE_SHA256.txt`  
**Rule:** This file was created only after the sequence-only outputs were frozen. The annotations below did not participate in discovery.

## BLOCK_A

Discovered maximal exact block (25 bp):

`CCGCCTGGGGAGTACGGCCGCAAGG`

Its first 16 bases are:

`CCGCCTGGGGAGTACG`

Post-freeze literature lookup identifies that exact 16-base sequence as the published **16sF primer targeting 16S rRNA**.

Reference: Kusumaningrum HD, Handayani L, Novrianti R. *Partial Sequencing of 16S rRNA Gene of Selected Staphylococcus aureus Isolates and its Antibiotic Resistance.* Media Peternakan. 2016;39(2):67–74. DOI: 10.5398/medpet.2016.39.2.67.

## BLOCK_B

Discovered exact block (24 bp):

`TAAGGTAGCGAAATTCCTTGTCGG`

Post-freeze literature lookup identifies this entire exact sequence as **Uni23S1926F**, a primer used to amplify bacterial **23S rRNA**.

Reference: Vingataramin L, Frost EH. *A Single Protocol for Extraction of gDNA from Bacteria and Yeast.* BioTechniques. 2015. DOI: 10.2144/000114263.

## Cluster interpretation

The raw discovery placed BLOCK_A and BLOCK_B approximately 2.94–3.04 kb start-to-start in five E. coli neighborhoods and 2.969 kb apart in Pyrococcus. Independent literature establishes that E. coli contains multiple rRNA operons containing 16S and 23S rRNA, and that Pyrococcus furiosus contains a cluster encoding 16S and 23S rRNA.

References include:
- Kurylo CM et al. *Endogenous rRNA Sequence Variation Can Regulate Stress Response Gene Expression and Phenotype.* Cell Reports. 2018. (E. coli K-12 has seven rDNA operons containing 16S, 23S, and 5S rRNA elements.)
- DiRuggiero J et al. *Regulation of ribosomal RNA transcription by growth rate in the hyperthermophilic archaeon Pyrococcus furiosus.* 1993. (Describes the single P. furiosus rRNA gene cluster encoding 16S and 23S rRNA.)

**Interpretation:** the sequence-only clustered-recurrence algorithm independently recovered two regions belonging to the same ancient rRNA organizational system without using rRNA annotation during discovery.

## CORE_0001

Three-domain exact core (16 bp):

`GTAGCGAAATTCCTTG`

Raw positions:
- E. coli: five copies, nested in BLOCK_B
- Pyrococcus: one copy, nested in BLOCK_B
- S. cerevisiae: chrM position 59,837 (0-based; 59,838 in 1-based coordinates)

Post-freeze annotation places the S. cerevisiae mitochondrial **21S_RRNA / Q0158** locus at bases 58,009–62,447. Therefore the independently found yeast core falls inside the mitochondrial 21S large-subunit rRNA locus.

Reference coordinates: SGD/S288C mitochondrial 21S_RRNA Q0158, 58,009–62,447.

## Validation conclusion

The raw algorithm was not told to search for genes, ribosomes, rRNA, operons, mitochondria, or conserved biological functions. It nevertheless recovered:

1. an exact block containing a known 16S rRNA primer sequence;
2. a nearby exact block that is itself a known 23S rRNA primer sequence;
3. repeated 16S/23S-like block neighborhoods at similar spacing in Bacteria and Archaea; and
4. a nested 16-base core of the 23S-associated block that persists in the yeast mitochondrial 21S large-subunit rRNA locus.

This is a **positive pipeline validation**, not a claim that rRNA conservation is newly discovered. The value of the result is that the annotation-blind recurrence method independently reconstructed a known conserved biological module, exactly as required for calibration before searching unknown patterns.
