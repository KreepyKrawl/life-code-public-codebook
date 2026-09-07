# LIFE-CODE v0.7 — Real Benchmark Ingestion

This bundle advances BENCH-P01A from synthetic fixtures to a real, published biological cohort.

## Canonical target
Heliconius cydno alithea male forewing color:
- 113 published males
- 57 yellow
- 56 white
- WGS available under PRJNA802836
- compact reference/GWAS/phenotype resources on Dryad DOI 10.5061/dryad.z8w9ghxjz

## Files
- `LIFE_CODE_REAL_BENCHMARK_INGESTION_v0.7_2026-09-03.docx` — canonical v0.7 pass
- `LIFE_CODE_BENCH_P01A_REAL_MANIFEST_v0.7.json` — machine-readable benchmark/source/split contract
- `lifecode_bench_p01a_freeze_split.py` — deterministic 91/22 split + truth sealing
- `lifecode_bench_p01a_ingest_preflight.py` — local source hash inventory
- `LIFE_CODE_REAL_BENCHMARK_LAB_v0.7.html` — local real benchmark lab

## Hard firewall
No EXP-0002 values or artifacts are used.
Known K-locus/aristaless biology is POST-REVEAL ONLY.

## Next action on the workstation
Acquire the Dryad benchmark files, hash them with the ingest preflight, extract the real phenotype table,
run the split utility, and physically isolate `SEALED_HOLDOUT_TRUTH.json` before any model fitting.
