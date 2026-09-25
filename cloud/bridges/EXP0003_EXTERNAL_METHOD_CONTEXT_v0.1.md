# EXP-0003 External Method Context v0.1

Status: **POST-FREEZE CONTEXT ONLY**

This document was added after EXP-0003 primary execution had begun. It does **not** modify the preregistration, frozen representations, controls, null family, thresholds, seeds, scoring engine, corpus, or interpretation rules. It exists only to preserve external methodological context for later interpretation and follow-up design.

## 1. Reduced-state nucleotide recoding is established

Purine/pyrimidine (RY) coding is an established phylogenetic recoding strategy. Published literature describes RY recoding as replacing A/G with R and C/T with Y, thereby emphasizing transversions, reducing some transition saturation, and potentially reducing some GC-associated compositional bias. It has historically been used when resolving deep divergences.

This means an eventual EXP-0003 result in which RY carries more transferable structure than literal ACGT would **not**, by itself, establish a previously unknown biological representation. A narrower novelty question remains: whether the frozen biological quotients show a reproducible transfer advantage under this exact sequence-transfer statistic and whether they exceed the frozen non-biological reduced-alphabet controls.

## 2. Recoding can help or hurt depending on the data-generating process

The broader phylogenetics literature cautions that reduced alphabets can either improve or degrade inference depending on saturation, compositional heterogeneity, model misspecification, and the recoding scheme. Reduced apparent compositional heterogeneity alone is not sufficient evidence that a recoding is more faithful to the underlying evolutionary process.

Interpretation consequence for EXP-0003: any observed quotient advantage should be described first as a property of held-out transferable exact-sequence structure under the frozen scorer. It should not automatically be translated into improved tree accuracy, improved evolutionary-model fidelity, or recovery of a privileged biological code.

## 3. Lumpability / Markov-process caveat

Published work on recoded DNA shows that state aggregation can reduce compositional heterogeneity while failing to preserve the Markov property of the original process; this can produce distortions such as altered inferred edge lengths.

Interpretation consequence for EXP-0003: an RY/MK/WS advantage, if present, does not by itself demonstrate that the recoded alphabet is a sufficient state representation of nucleotide evolution. A separate post-primary lumpability/model-fidelity test would be required for that claim.

## 4. First-order sequence nulls are established, but null choice matters

First-order Markov and dinucleotide-controlled randomization are established approaches for asking whether genomic-sequence structure exceeds what is expected from local composition/dependency. The literature also shows that significance can change materially when moving from weaker mononucleotide controls to dinucleotide/first-order controls.

EXP-0003's frozen N1 family therefore has a defensible methodological role: preserve sequence length, projected-symbol composition, first-order transitions, and record boundaries while destroying longer-range exact transfer. However, a first-order Markov simulation is not identical to an exact dinucleotide-preserving shuffle. The distinction must remain explicit.

Potential future robustness test, **not part of the active primary family**: compare the frozen N1 results against an exact first-order/dinucleotide-preserving shuffle where computationally feasible. This may test whether any signal depends on expected versus exact transition-count preservation.

## 5. Why the frozen non-biological controls matter

Because reduced alphabets can improve apparent transfer simply by collapsing state space, a biological quotient cannot be privileged solely because it outperforms ACGT. EXP-0003's preregistered memory-1 balanced controls provide a direct compression/control family. The primary interpretation remains bounded by the frozen comparison:

- biological quotient versus literal ACGT;
- biological quotient versus frozen non-biological reduced-alphabet controls;
- depth dependence across frozen ladders;
- equivalence-class reporting if biological quotients do not separate from one another or from controls.

## 6. No active-analysis changes

As of this context note:

- primary outcomes remain unrevealed;
- no result artifact was inspected to write this note;
- no resource allocation was changed using scientific outcomes;
- the preregistration remains authoritative;
- any literature-inspired follow-up must be labeled post hoc and frozen separately before execution.

## External sources reviewed

1. Foster et al., *Recoding Amino Acids to a Reduced Alphabet may Increase or Decrease Phylogenetic Accuracy*, Systematic Biology 72(3), 2023. DOI 10.1093/sysbio/syac042.
2. Blanquart & Lartillot / related nonstationary-sequence modeling literature discussing RY coding, compositional bias, saturation, and deep divergences; Molecular Biology and Evolution 23(11), 2006.
3. Vera-Ruiz et al. / recoded-DNA lumpability work, *A Likelihood-Ratio Test for Lumpability of Phylogenetic Data: Is the Markovian Property of an Evolutionary Process Retained in Recoded DNA?*, 2021, PMID 34498090.
4. Statistical tests for appropriate nucleotide recoding in molecular phylogenetics, 2014, PMC4015178.
5. Workman & Krogh, *No evidence that mRNAs have lower folding free energies than random sequences with the same dinucleotide distribution*, Nucleic Acids Research 27(24), 1999.
6. Gesell & Washietl, *Dinucleotide controlled null models for comparative RNA gene prediction*, BMC Bioinformatics 9:248, 2008.
7. Acquisti et al., *Nullomers and High Order Nullomers in Genomic Sequences*, PLOS ONE, 2016.

These references provide methodological context only; none is treated as evidence for the EXP-0003 biological hypothesis.