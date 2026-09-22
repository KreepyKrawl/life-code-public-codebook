# EXP-0003 — Triad Binding Recovery Status

**Status:** EXECUTION BLOCKED — EXACT EXP-0002 TRIAD BINDING NOT YET FULLY RECOVERED

## Why this file exists

EXP-0003 is preregistered to reuse the exact 12 EXP-0002 triads. The 26 frozen assemblies and their canonical normalized FASTAs are online in the cloud, but the original manifest file that supplied the production runner's `rowmap[triad_id]` is not currently present in the repository or accessible saved Library.

The original authoritative filename is:

`EXP0002_TRIADS.csv`

The v0.1.33 production runner read rows containing at least `triad_id`, `genome_1`, `genome_2`, and `genome_3`, built `rowmap[tid]`, and executed each frozen triad from that row. The completed-run validator later checked each triad against the `SEALED_RESULT.input_ids` binding.

## Source-precedence rule

The September 3 LIFE-CODE recovery control established the scientific/execution source order:

1. newest verified canonical execution package and its frozen files;
2. sealed/checkpoint artifacts from the actual run;
3. recovery control and dated execution snapshots;
4. interpretive/book notes;
5. older chat recollections.

It also explicitly states that if the newest canonical package is unavailable, it must not be reconstructed from memory or an older package.

Therefore **taxonomy, biological similarity, filename order, or recollection must not be used to fill missing triad rows**.

## Directly recovered rows

### A1 — source recovered

Direct live execution evidence names the exact three canonical normalized FASTAs passed to the A1 LONGEST_BLOCK runner:

- `A_HSAP`
- `A_PTRO`
- `A_MMUL`

The corresponding preserved A1 checkpoint also binds these three paths to their canonical normalized SHA-256 values:

- `A_HSAP`: `c36698b7e3945bdefb5e2c7782853db6d91b1ea30001e474d9a1e89880a69131`
- `A_PTRO`: `3aeaf0161f56749a1b5b4b5339e4a6b648fb04bd344d01b3398742754a835a1b`
- `A_MMUL`: `7233a0bb967602e795b0d1688b98032759468d124ce047822e274d45fe7de1c8`

Recovery status: **SOURCE-BOUND**.

### A2 — cryptographic source recovered

`MAX_K_RESUME_PROOF.json` preserved the A2 input identity and normalized FASTA hashes:

- `A_HSAP`: `c36698b7e3945bdefb5e2c7782853db6d91b1ea30001e474d9a1e89880a69131`
- `A_MMUS`: `5ad32b30e909fa894e673dcd5b5561d45711b86f028c2d40882f79e0b384b156`
- `A_BTAU`: `1aac63d4a7caf4d462a794a98eec7618bbe17d12cc3c519be437bec18046acf7`

Recovery status: **SOURCE-BOUND**.

## Rows not yet source-bound

The following exact rows remain unresolved from authoritative input-binding evidence:

- B1
- B2
- B3
- F1
- F2
- F3
- P1
- P2
- P3
- A3

Their prior sealed result artifacts are independently verified, but the accessible logs currently preserve artifact hashes rather than the member `input_ids`/source rows.

Known sealed-result SHA-256 values:

- B1 `57c599f17e06eb523f887d2b8284391e7b425043af1065e52d2ff596f5593404`
- B2 `bedbae7eb7c2e62380e899e5d9b9faa1bf4c9bd164cbbbf4ff5c29eb6de6d45f`
- B3 `cbfbff44299aff21b47b461847d1a9c9b35035537d72a62f31b2ed88b1f2b35e`
- F1 `085e92b9ce5d8c193897cb95e2e10d7ee8feb7bf89ed63b16ee59f8f2b8c6174`
- F2 `79f1a8a721d5eedfce662c2566d026905b5a9398eb5974415ef1e14719639155`
- F3 `de4482f623109272d5cdc521e50c5251db237d7a6d5d3db2433a6ec56c1b8929`
- P1 `f4ad83c771e025db7422250d3523d1a5071b9e1ac196b97493b989294c25800e`
- P2 `a7d0bae8657cb4cedcafe349ac98e49e27a7e27f7c1eead3cf670c84ecf4f05c`
- P3 `fe8973f22d986513c8b0b755cb96434048dca2106710d1bdefb0f5737d72a9b1`

A1 sealed result SHA-256 for reference: `23fd1df605c3092c6225cbc4636589d73e6e8d57c7c936047b926bb240dfef52`.

## Binding gate

EXP-0003 **must not execute primary transfer scoring** until one of these conditions is satisfied:

### Gate A — exact source recovery

The original `EXP0002_TRIADS.csv`, or equivalent sealed `input_ids` for all 12 rows, is recovered from the canonical v0.1.33 execution lineage and cryptographically/provenance verified.

### Gate B — separately frozen forensic recovery

If exact source recovery is exhausted, a separate forensic metadata-recovery protocol may be preregistered before execution. It may use only pre-existing EXP-0002 artifacts/fingerprints and the frozen 26-assembly corpus, never EXP-0003 outcomes. A row may be promoted only if the historical binding is uniquely determined by independent prior fingerprints; ambiguous rows remain blocked.

A forensic reconstruction must be explicitly labeled as reconstructed metadata and must never be represented as the original manifest.

## Additional EXP-0003 gate

The EXP-0003 primary Markov-null replicate count is not yet frozen. It must be selected and committed using outcome-blind runtime/resource qualification before any EXP-0003 primary outcome is inspected.

## Anti-drift rule

Do not:

- infer missing rows from phylogenetic intuition;
- use taxonomic closeness to choose among candidate triples;
- use EXP-0002 metric monotonicity alone to manufacture a desired ladder;
- inspect any EXP-0003 representation outcome before triad binding and null replicate count are frozen;
- substitute a different triad architecture because the original manifest is inconvenient to recover.

Until the binding gate passes, EXP-0003 remains **PREREGISTERED / EXECUTION BLOCKED**.
