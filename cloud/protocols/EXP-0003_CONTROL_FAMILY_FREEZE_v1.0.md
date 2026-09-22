# LIFE-CODE EXP-0003 — Non-Biological Binary Control Family Freeze v1.0

## Status
FROZEN BEFORE ANY EXP-0003 QUOTIENT-TRANSFER RESULT IS INSPECTED.

This file operationalizes primary support rule 3 in `EXP-0003_PHYLOGENETIC_QUOTIENT_TRANSFER_PREREG_v1.0.md`. It does not alter EXP-0002 and does not use RCX-LCX-0001 Stage-A outcomes to choose a winning EXP-0003 representation.

## Why a fourth static balanced partition is impossible
For a four-symbol alphabet, a memoryless balanced binary projection partitions the four symbols into two unordered pairs. Up to output-bit complementation there are exactly three such 2+2 partitions:

1. RY: `{A,G}|{C,T}`
2. MK: `{A,C}|{G,T}`
3. WS: `{A,T}|{C,G}`

Therefore there is no independent fourth static balanced 2+2 nucleotide partition that can serve as a non-biological control. A random static balanced partition would necessarily reproduce RY, MK, or WS up to output-label reversal.

## Control class
The non-biological controls are deterministic **memory-1 state-switched balanced projections**.

At every position the active map is still one of the same three balanced 2+2 maps, so every state has the same binary output alphabet and the same 2+2 instantaneous degeneracy as the biological quotients. What is broken is the existence of one globally fixed biochemical nucleotide partition.

Let the previous raw nucleotide state be one of `A,C,G,T`. A control is specified by a four-tuple:

`(m_A, m_C, m_G, m_T)`

where every `m_x` is one of `RY, MK, WS`.

For position `i > 0`, project the current raw nucleotide with map `m_{x[i-1]}` selected by the immediately preceding raw nucleotide. For the first base of every source ACGT record/segment, use a virtual previous state `A`. Never carry state across source ambiguity/record boundaries.

The three constant tuples `(RY,RY,RY,RY)`, `(MK,MK,MK,MK)`, and `(WS,WS,WS,WS)` are excluded because they are exactly the biological memoryless quotients. The candidate non-biological universe therefore contains `3^4 - 3 = 78` controls.

This class is translation-local rather than absolute-coordinate phased: an insertion/deletion does not arbitrarily rephase the entire downstream chromosome. The control is deterministic and uses no annotation, taxonomy, outcome, or genomic coordinate as a selector.

## Frozen compute-budget family selection
EXP-0003 will evaluate exactly 12 non-biological controls.

Enumerate the 78 nonconstant tuples in lexicographic product order over map labels `(RY,MK,WS)` and base-state order `(A,C,G,T)`. For each tuple compute:

`SHA256("EXP0003_CONTROL_V1|" + m_A + "," + m_C + "," + m_G + "," + m_T)`

Sort ascending by that hex digest and select the first 12. This rule is data-independent and frozen before primary execution.

Frozen controls:

| ID | `(m_A,m_C,m_G,m_T)` | selection SHA-256 |
|---|---|---|
| C01 | `(RY,RY,MK,MK)` | `01d9e3b640f1922d001f933d3c4f796d5b4d0b524d83d3bd1c4128b378642465` |
| C02 | `(RY,WS,RY,MK)` | `03a2f213cdcc0e59dceb518d89837a6e542c9bf2e2d0fb4e34a1e1ccd071ac06` |
| C03 | `(MK,MK,MK,RY)` | `11c2a4c72bc89c5c11cb628224b72f753627e0e48bcc996427987a3aefc2ddf8` |
| C04 | `(RY,WS,MK,RY)` | `177539debc39f8d4ed940bfbcb623d00fffd69f146bdfdf6084e38e314543876` |
| C05 | `(MK,RY,MK,WS)` | `187f4ea302e1ed4da474650fde974826ebc368ddd53155031cdcae115bf70e81` |
| C06 | `(MK,MK,WS,RY)` | `193dab89ecdd8028fec3b6f4e3cd784d7ca701aef1e5b43ff720a5b32c671d8f` |
| C07 | `(MK,MK,MK,WS)` | `1a284f4388620178bd5febba1001181276e547c050e3b981053237d6bf181779` |
| C08 | `(WS,MK,WS,RY)` | `1b492b4fc5752fb5dc0c78315f24f01acfea6a5d67c80c7433fee3e8443795a3` |
| C09 | `(RY,MK,WS,WS)` | `1b4d4968466f6767c25fa79603725fd4661c368f019ff62f057c49a5cfc71552` |
| C10 | `(RY,MK,MK,WS)` | `1efe1d5a6444fe20bcb278f4597f509fe38cad81528fd9e6ec34f98dabe0f4ac` |
| C11 | `(WS,WS,RY,WS)` | `235ded51cbf77ea27b71660e51110709434c0be84eeff2bf353c3ed546d31933` |
| C12 | `(RY,MK,MK,RY)` | `279428acb155535b0643a772887477c3a5791c70d8dcae625f4e7ada73a016a7` |

## Scoring
Every control is processed by the same EXP-0003 transfer engine and the same representation-specific primary N1 null definition as ACGT/RY/MK/WS. Controls receive the same fold structure and produce the same quantities `L*`, `p`, `S`, `G`, `rho`, `delta_rho`, and `C`.

The ACGT reference remains the baseline for control `G` and `delta_rho`, exactly as for the biological quotients.

## Frozen control-family support criterion
For a biological quotient `pi` define:

- `MG(pi)` = mean `G(pi,t)` across the 12 frozen triads.
- `MR(pi)` = mean `delta_rho(pi,g)` across the four frozen ladders.

For every frozen control `c`, compute the same `MG(c)` and `MR(c)`.

Primary support rule 3 is satisfied only if BOTH are true:

1. `MG(pi) > max_c MG(c)`
2. `MR(pi) > max_c MR(c)`

This is a familywise max benchmark. No control may be dropped because it performs inconveniently well. No additional control may be added after biological quotient results are inspected.

Representation crossover `C` is reported for controls as a diagnostic but is not an additional pass gate.

## Identifiability / interpretation
A biological quotient that fails to beat the frozen control-family maxima does not establish biochemical privilege even if it beats ACGT. If multiple biological quotients pass but remain evidentially indistinguishable, report an equivalence class rather than selecting a unique representation.

A passing result still supports only a representation-level transfer statement under the frozen protocol. It does not establish a universal biological language, unique latent code, or common physical substrate with Reality-Code.

## Runtime/null-count boundary
This file freezes the control family and comparison rule, not the N1 replicate count. The N1 replicate count must be frozen in a separate execution-qualification record before any EXP-0003 outcome is inspected. It may be selected only from outcome-blind runtime/resource qualification, not from observed transfer values.
