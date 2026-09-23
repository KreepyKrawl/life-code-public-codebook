# EXP-0003 — Triad Binding Recovery Status

**Status:** SOURCE-BOUND — EXACT EXP-0002 TRIAD MANIFEST RECOVERED FROM CANONICAL v0.1.33 PACKAGE

## Recovery

The original authoritative file `EXP0002_TRIADS.csv` has now been recovered directly from the nested canonical archive `LIFE_CODE_v0.1.33.zip` inside the uploaded `LIFE_CODE_EXECUTION_KIT_v0.1.33 (2).zip`.

The nested canonical archive SHA-256 is the already-locked v0.1.33 authority:

`23b50cc7fbac84736ad2c2762044013dbf90d227154a754238c7a0f3c1ce963f`

The recovered exact triad manifest bytes have SHA-256:

`81e98c2bd235609cada938519b8d7890ff180b03f406f6ad9852c0fed6c198f4`

The recovered manifest has been committed to:

`cloud/canonical/v0.1.33/EXP0002_TRIADS.csv`

This satisfies Gate A from the previous recovery status. No phylogenetic inference, recollection, or EXP-0003 outcome was used to fill any row.

## Exact frozen triads

| Triad | Ladder | Depth | Stratum | genome_1 | genome_2 | genome_3 |
|---|---|---:|---|---|---|---|
| B1 | Bacterial | 1 | Enterobacterales | B_ECOLI | B_SALM | B_KLEB |
| B2 | Bacterial | 2 | Gammaproteobacteria | B_ECOLI | B_PAER | B_VCHO |
| B3 | Bacterial | 3 | Bacteria | B_ECOLI | B_BSUB | B_MTUB |
| F1 | Fungal | 1 | Saccharomycetes | F_SCER | F_KLAC | F_CALB |
| F2 | Fungal | 2 | Ascomycota | F_SCER | F_NCRA | F_SPOM |
| F3 | Fungal | 3 | Fungi | F_SCER | F_SPOM | F_CNEO |
| P1 | Plant | 1 | Brassicaceae | P_ATHA | P_ALYR | P_CRUB |
| P2 | Plant | 2 | eudicotyledons | P_ATHA | P_PTRI | P_SLYC |
| P3 | Plant | 3 | Embryophyta / land plants | P_ATHA | P_PTRI | P_PPAT |
| A1 | Animal | 1 | Primates | A_HSAP | A_PTRO | A_MMUL |
| A2 | Animal | 2 | Mammalia | A_HSAP | A_MMUS | A_BTAU |
| A3 | Animal | 3 | Vertebrata | A_HSAP | A_GGAL | A_DRER |

## Binding gate

**PASS.** EXP-0003 is no longer blocked on triad identity.

The remaining pre-execution gate is the preregistered outcome-blind runtime qualification and freeze of the primary N1 null replicate count. No EXP-0003 quotient-transfer outcome may be inspected before that count and its deterministic seed schedule are committed.
