# LIFE-CODE Public Codebook Core v0.8

This repository publishes the evidence-bounded LIFE-CODE Codebook Core v0.8.

The **SQLite Codebook is the scientific product**. The Cloudflare Pages interface is a read-only client generated from the database; scientific facts do not originate in presentation code.

## Release contents

- `LIFE_CODE_CODEBOOK_CONTINUATION_v0.8.sqlite` — canonical continuation database
- `lifecode_codebook.py` — standard-library CLI and JSON exporter
- `lifecode_codebook_server.py` — standard-library local browser server
- `LIFE_CODE_CODEBOOK_UI_v0.8.html` — original local database-backed interface
- `index.html` — static Cloudflare Pages client
- `codebook-v0.8.json` — deterministic public export from the SQLite database
- `README_CODEBOOK_v0.8.md` — local operating instructions

## Verify locally

```bash
python3 lifecode_codebook.py verify
python3 lifecode_codebook.py stats
python3 lifecode_codebook.py show PC2-MODULE-FBA
```

## Public boundary

- Released Tier-A LIFE-CODE calibration/proof evidence only.
- No EXP-0002 outcome values.
- No invented Proof Case 0001 sequences.
- No reconstruction of the unmounted `LIFE_CODE_CODEBOOK_v0.0.81.zip` archive.

The protected prior archive remains separately identified by SHA-256 `081ad5bab0cb2c125297b9acb32905fca70f9d09d5e0911f75e91f5a6d9f44e2` and must not be overwritten or reconstructed until its 112,174,983 bytes are physically mounted and verified.

## Data path

`raw evidence → validated ingest → Codebook → query/analysis engine → UI`

The UI is not an authority and must never be used to create scientific facts.
