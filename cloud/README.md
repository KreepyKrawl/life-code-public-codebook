# LIFE-CODE Cloud Runner

This branch begins the migration of LIFE-CODE execution away from the local workstation.

## Scientific authority

EXP-0002 is already complete and sealed. It MUST NOT be rerun as part of this migration.

Canonical references:

- EXP-0002 sealed bundle SHA-256: `76fb482a368af757a53688ef947d2a219280a2db8c3bc4d5bb5906bc6978a713`
- A3 sealed result SHA-256: `769b21fe5f1f1caff44399eff563f1f8d29a48dcdfc1729c9a036a2eb16c7258`
- A3 LONGEST_BLOCK SHA-256: `cf72f5783b799b1b5f53acfcfd60071299248b6c7efbfce87ae76425c003ebf9`
- v0.1.33 execution kit SHA-256: `23b50cc7fbac84736ad2c2762044013dbf90d227154a754238c7a0f3c1ce963f`

The cloud migration may reference these artifacts but must not reconstruct or mutate them.

## Online operating model

The target mirrors the Reality-Code operating pattern:

1. GitHub stores source, protocols, manifests and workflow definitions.
2. Cloud jobs are split into bounded chunks rather than relying on a single multi-day process.
3. Every chunk emits a checkpoint, SHA-256 manifest and machine-readable status artifact.
4. Later jobs resume only from hash-verified checkpoints.
5. Final experiment bundles are immutable and independently hashable.
6. A lightweight web/mobile status surface reads run state; it is not scientific authority.
7. LIFE-CODE and Reality-Code remain separate experimental tracks.

## Planned online experiments

### EXP-0002A — A3 299 Forensics

Post-freeze follow-up only. Recover the actual 299-bp winners for AB_C, AC_B and BC_A, map coordinates/orientation/copy number, and add post-freeze annotation. It must not modify EXP-0002.

### EXP-0003 — Phylogenetic Quotient Transfer

Reuse the frozen EXP-0002 corpus and triads. Compare native ACGT with preregistered R/Y, M/K and W/S representations using representation-specific null models and null-adjusted held-out transfer scores.

## Migration rule

Canonical source is never recreated from chat snippets. If an exact canonical source file is not available online, the cloud runner must stop at a provenance gate rather than silently substitute reconstructed code.
