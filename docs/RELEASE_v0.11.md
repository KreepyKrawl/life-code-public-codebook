# Core v0.11: the research record

This release publishes the eligible historical research inside archive v0.0.81 as a lossless, queryable extension to the recovered calibration core. It does not announce newly executed experiments.

## Public coverage

- 66 of 69 historical Codebook entries; 47 of 51 prediction records.
- 260 original evidence statements, retaining E0/E1/E2/I1/P1/H1 classes.
- 202 explicit links between research records; targets outside this release remain identified as unavailable.
- 109 original source references with hashes and byte counts: 92 source files bundled, 14 indexed without bundled bytes, and 3 held for disclosure review.
- Nine guided reading stages from literal matching through masked representations, semantic failures, replication, stronger controls, and fresh model-v3 predictions.

Seven records are withheld because they contain primary-run results, related unreleased predictions, or a broader claim requiring disclosure review. Full archive bytes remain unchanged and private. The release manifest fixes the exact hash of each allowed record and source. No published record is silently redacted or reworded.

## What readers can now do

Follow the Research journey, filter the ledger by prediction status, search statements and unknowns, open linked records, compare original support/falsification conditions with recorded outcomes, and download original evidence. Research mode opens the complete JSON by default; every mode retains access to it.

The stored statuses are historical. In particular, LC-PRED-0049, LC-PRED-0050 and LC-PRED-0051 remain FROZEN_UNTESTED. A positive development diagnostic is not prospective validation. Counts across heterogeneous predictions are not a success rate. Research links are record dependencies, not newly asserted evolutionary-history edges.

## Verification and technical scope

The new database preserves every v0.10 scientific and audit table unchanged. New immutable tables hold original record JSON, separately queryable assertions, source metadata, source links, research links, reading-guide copy, and a hashed ingestion event. Public core and research projections identify the same SQLite file and hash. The original archive and source hashes are verified during generation; historical experiments are not rerun by this publishing step.

Run `python tools/test_research_v011.py` to verify payload identity, preserved statuses, original source bytes, source coverage, excluded records, snapshot/SQLite agreement and the navigation regression. Rebuild with `python tools/build_research_v011.py --archive /path/to/LIFE_CODE_CODEBOOK_v0.0.81.zip` in a clean checkout with the v0.11 generated SQLite output removed or relocated first; the builder refuses to overwrite an existing output.

The navigation bug caused by a global `history()` function is corrected, and navigation tolerates an unavailable History API. Changed assets have versioned URLs to avoid stale browser scripts.
