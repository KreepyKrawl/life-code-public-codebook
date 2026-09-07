# LIFE-CODE — Mainline Recovery & Continuation Lock v0.10

**Date:** 2026-09-05  
**Purpose:** Consolidate the LIFE-CODE framework / Codebook / UI / publication state after the separate deployment/Work-mode thread, prevent loss or version drift, and define the next scientific development point.

## 1. Project split remains locked

This mainline thread is canonical for the LIFE-CODE scientific framework, Codebook implementation, ingestion/provenance/query architecture, Biological Diff / History / Trait / Constraint / Possibility design, book integration, public-read-only explorer design, and post-freeze interpretation of already released calibration evidence.

The separate EXP-0002 execution thread remains quarantined for live process recovery, sealed primary experiment execution, checkpoint/resume, vendor/runtime verification, result sealing, and final validated reveal.

**Reveal barrier remains active.** No partial EXP-0002 values or trends may steer the framework.

## 2. Canonical architecture

The scientific product is the **Codebook**. The UI is only a client.

`raw genome / frozen experiment artifact -> validated ingest -> Codebook -> query/analysis engine -> UI`

No scientific fact may originate in presentation code.

Predictive path remains downstream:

`Codebook -> Biological Diff -> Constraint / Reachability Engine -> frozen prediction packet -> renderer`

Canonical prediction rule: **THE PACKET, NOT THE PICTURE, IS THE PREDICTION.**

Canonical visual rule: **THE PIXEL MUST HAVE A PROVENANCE PATH.**

## 3. Implemented Codebook Core — v0.8

The real local Codebook is SQLite and contains artifact provenance/hashes, taxa, experiments, code objects, occurrences, graph edges, measurements, post-freeze annotations, claims, claim links, evidence tiers/states, and explicit data-completeness states.

Verified released contents:
- 7 provenance artifacts
- 6 calibration/proof experiments
- 10 Codebook objects
- 7 graph edges
- 190 released scientific measurements
- 3 post-freeze annotations
- 4 bounded claims

Object types: 4 BLOCK, 3 FALSIFIED_MODEL, 2 MODULE, 1 PRIMITIVE.  Evidence states: 7 EXPERIMENTAL_RESULT, 3 FALSIFIED.

Important intentional incompleteness: the exact Proof Case 0001 sequence strings for the 24-bp block, nested 16-bp core, and 25-bp block remain NULL because they were not recovered in the currently mounted source set. They must never be invented.

## 4. Released Tier-A science preserved

### Proof Case 0001
Annotation-blind three-domain recurrence recovered 54 exact shared 16-mers, a 24-bp E. coli/Pyrococcus block, a nested 16-bp core also in yeast, a second 25-bp block, and six A->B spacings of 3035, 2943, 3036, 3029, 2943, 2969 bp (93-bp range). A 5,000,000-draw spatial null produced zero random all-five E. coli downstream hits. Post-freeze interpretation mapped the recovered architecture to the ribosomal organizational system; the yeast shared core lies in mitochondrial 21S LSU rRNA.

### Proof Case 0002
Annotation-blind E. coli/yeast recurrence recovered 19,112 shared exact 16-mers, six high-complexity multiblock clusters (five mitochondrial), and one non-mitochondrial FBA module with exact 25-bp and 17-bp blocks. Raw starts are exactly 263 bp apart in both genomes. Both coding regions are 1080 bp; nucleotide identity is 50.9% and protein identity is 38.7%. Exact recovered sequences:
- C25 raw: `CAGTAGAACCGGAACCACCGTGGAA`
- C25 coding-oriented: `TTCCACGGTGGTTCCGGTTCTACTG`
- D17 raw: `TCTTCTTCACCACCGGT`
- D17 coding-oriented: `ACCGGTGGTGAAGAAGA`

Post-freeze annotation identified E. coli `fbaA` and yeast `FBA1`.

### Vocabulary ladder
All-three exact recurrence: k=8 64,583; k=10 554,725; k=12 232,939; k=14 5,561; k=16 54; k>=18 0. This does **not** establish one universal biological word length.

### Negative calibrations
- Flat exact dictionary compression: no valid fixed-length exact dictionary beat the 2-bit/base baseline after dictionary/reference costs. **FALSIFIED_AT_THIS_ABSTRACTION_LEVEL**.
- Exact-gap syntax: strict A -> identical exact gap -> B transferred zero modules in every held-out deep-domain fold. **FALSIFIED_AT_THIS_ABSTRACTION_LEVEL**.
- Ordered-window syntax: exact 16-mer A before exact 16-mer B within 10 kb transferred zero training modules in all three held-out deep-domain folds and zero across 30 shuffled held-out null genomes. **FALSIFIED_AT_THIS_ABSTRACTION_LEVEL**.

These failures motivate testing evolutionary depth rather than loosening syntax post hoc.

## 5. Recovered canonical interpretive expansion

LIFE-CODE is an **annotation-blind genomic decompiler / software-archaeology system**:

`unknown raw sequence -> recurring signatures -> repeated routines -> physical relationships -> inferred modules -> freeze -> biological symbol/function recovery afterward`

A genome should be treated heuristically as **a multi-billion-year-old production codebase that has never been taken offline for a complete rewrite**.

The structural model must allow coexistence of current functional modules, duplicated routines, degraded/neutral residue, pseudogene-like dead branches, selfish elements, foreign insertions, historical patches, compatibility constraints, repurposed legacy components, lineage-specific forks, and merger-derived components. This is **not** a claim that every base is functional.

A falsifiable strata expectation is: ancient broad primitives -> narrower clade/domain modules -> lineage-specific combinations -> recent duplications/patches -> foreign/selfish insertions -> neutral/degraded remnants -> repurposed legacy elements.

## 6. Mitochondrial / merger correction

Mitochondrial ancestry is not merely a future LIFE-CODE benchmark. Proof Case 0001 already produced annotation-blind evidence relevant to historical layering: the sequence-only pass recovered a cross-domain ribosomal module, and only after freeze did annotation show the yeast member of the shared core lies in mitochondrial 21S LSU rRNA.

Bounded interpretation: this does **not** reconstruct the full endosymbiotic merger or prove all mitochondrial-to-nuclear dependency history. It **does** justify representing one organism as potentially containing multiple historical code lineages.

Long-term history representation should support a **network of code histories**, not only a species tree, with candidate mechanisms such as vertical inheritance, merger, endosymbiosis, horizontal transfer, viral insertion, plasmid exchange, duplication, deletion/degradation, and repurposing. Every history assignment must carry its own evidence state.

## 7. Anti-conventionality rule

For important structures, analysis should rotate through biologist, reverse-engineer/coder, adversarial/security, distributed-systems, evolutionary-archaeology, and information-theory lenses before semantic closure. Biology remains the validation layer, not the conceptual ceiling.

## 8. Public/deployment branch status

A separate **PUBLIC v0.9** static Codebook package exists as the free-hosting/publication layer. It is not a replacement for the canonical SQLite Codebook.

`canonical local SQLite Codebook -> fail-closed public snapshot -> static explorer -> GitHub / Cloudflare mirror`

PUBLIC v0.9 includes real Codebook data, search/filtering, object drill-down, experiment views, claims/boundaries, measurements, provenance, graph navigation, JSON export, and a public release firewall. No EXP-0002-sensitive artifacts or Tier-C records are permitted. Heavy genomic compute remains local.

Because PUBLIC v0.9 already exists, **do not reuse v0.9 as the next Codebook Core version.** The next scientific mainline version is **Codebook Core v0.10**.

## 9. Next Codebook Core target — v0.10

Priority:
1. Deterministic ingestion of released calibration artifacts into a fresh Codebook.
2. Immutable `ingest_events`, `freeze_events`, and `reveal_events` audit timeline.
3. Machine-enforced scientific gates for Tier-C leakage, reveal timing, provenance, sequence hashes, and coordinate basis.
4. Recursive provenance tracing from any object/measurement/claim to experiment and source artifact.
5. Deterministic stable IDs for primitives/blocks/relations.
6. History representation with `strata` and `history_edges`; candidate types: INHERITED, DUPLICATED, DELETED_OR_DEGRADED, REARRANGED, REPURPOSED, HGT_CANDIDATE, VIRAL_INSERTION_CANDIDATE, PLASMID_EXCHANGE_CANDIDATE, ENDOSYMBIOTIC_OR_MERGER_CANDIDATE, UNKNOWN.
7. Biological Diff integration against stable Codebook IDs and source DB hashes.
8. Fresh-build integration tests asserting current counts, C25/D17 lookup, 263-bp edge, ordered-window zeros, no Tier-C leakage, valid source hashes, PC0001 sequences remain NULL, and reveal timing remains explicit.

Do **not** spend the next pass on cosmetic UI. Do **not** advance to new real-data predictive modeling until ingestion/provenance is solid. Do **not** use partial EXP-0002 values.

## 10. Old Codebook archive protection

`LIFE_CODE_CODEBOOK_v0.0.81.zip`
- expected bytes: 112,174,983
- SHA-256: `081ad5bab0cb2c125297b9acb32905fca70f9d09d5e0911f75e91f5a6d9f44e2`

Do not overwrite, reconstruct, or merge it from memory. When mounted: verify byte count and hash, inspect internals, compare to current schema, build explicit migration/diff plan, preserve both old archive and continuation.

## 11. Mainline continuation point

Resume from:

> **Codebook Core v0.10 — deterministic ingest + immutable freeze/reveal audit + provenance tracing + history-network schema**

## 12. Canonical one-sentence frame

> **LIFE-CODE is an annotation-blind genomic decompiler and software-archaeology framework that discovers reusable sequence primitives, physical relationships, modules, and evolutionary history directly from raw DNA, freezes those structures before semantic reveal, and then uses biology to validate, falsify, or refine what the recovered code appears to mean.**
