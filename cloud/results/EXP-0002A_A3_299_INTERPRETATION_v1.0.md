# LIFE-CODE EXP-0002A — A3 299-bp Post-Freeze Forensic Interpretation v1.0

## Status
COMPLETE — POST-FREEZE FORENSIC INTERPRETATION. This document does not modify EXP-0002's sealed primary result or its preregistered support decision.

## Authority and provenance
- Source experiment: EXP-0002, A3 (Vertebrata: A_HSAP, A_GGAL, A_DRER).
- Frozen EXP-0002 A3 LONGEST_BLOCK result: AB_C=299, AC_B=299, BC_A=299; triad median=299.
- Cloud forensic run: GitHub Actions run `35804419600`.
- Aggregate forensic artifact: `EXP0002A_A3_299_FORENSICS.json`.
- Aggregate artifact SHA-256: `2ff3a501481ee199192183a176602fbad613da1119c7055b0738995295ee6113`.
- Canonical LONGEST_BLOCK wrapper reference SHA-256: `f3b9fb457a4ee11fe41af70962b7d268f4f12ef22e2441b20160379c9208db5e`.
- The cloud corpus had already passed 26/26 raw and 26/26 canonical-normalization hash equivalence before this forensic run.

## Forensic question
Did the identical 299-bp fold frontier in all three A3 held-out folds arise from the same exact 299-bp sequence, or from unrelated loci that happened to share the same length?

## Result
Yes. One exact 299-bp sequence was recovered as a winner in all three folds.

Common sequence SHA-256:
`4773111cb157a55635ab83aeb6aa2f525abe9be1e40c37aa566c9f80f5e85285`

Composition:
- T: 224
- C: 75
- A: 0
- G: 0

The sequence is the simple periodic motif `TCTT` repeated across the 299-bp window (with the terminal truncation implied by length 299).

Fold summary:

| Fold | 299-bp candidates in training pair | Held-out hits >=299 | Winners | Common winner present |
|---|---:|---:|---:|---|
| AB_C | 12 | 1 | 1 | yes |
| AC_B | 10 | 102 | 1 | yes |
| BC_A | 5 | 32 | 2 | yes |

BC_A also contains a second 299-bp winner with SHA-256 `6b5e949955a7537ff505b26b22f0be3c01599977b57fce88ca851c8d9d9d1022`, composition A=224/G=75, corresponding to the reverse-complement periodic form `AGAA...`.

## Interpretation
The 299-bp A3 exact-transfer frontier is real under the frozen EXP-0002 metric, but the post-freeze forensic evidence shows that this frontier is driven by a very low-complexity periodic repeat rather than a demonstrated unique high-information conserved locus.

Accordingly:
- EXP-0002 remains unchanged and canonically supported under its frozen primary scoring rule.
- The A3 LONGEST_BLOCK=299 observation should not be cited by itself as evidence of a unique conserved 299-bp biological instruction.
- The forensic result strengthens the need for representation-specific null correction and identifiability controls in EXP-0003.

## Claim boundary
This result establishes sequence identity and low-complexity character for the recovered A3 299-bp frontier under the forensic procedure. It does not yet establish the repeat's annotation, repeat-family classification, function, evolutionary origin, or biological mechanism. Those require a separately scoped annotation/repeat analysis.
