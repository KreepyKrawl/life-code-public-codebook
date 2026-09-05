# LIFE-CODE Codebook Core v0.8

## Maturity
**EXECUTABLE TOOL / REAL LOCAL DATABASE**

This is not a posterboard. The supplied Python tools query a real SQLite database containing released LIFE-CODE evidence.

## Requirements
Python 3 only. No `pip install`, Node.js, cloud account, or external database is required.

## CLI
Keep the `.sqlite` and `lifecode_codebook.py` files together.

### WSL / Linux
```bash
python3 lifecode_codebook.py verify
python3 lifecode_codebook.py stats
python3 lifecode_codebook.py list
python3 lifecode_codebook.py show PC2-MODULE-FBA
python3 lifecode_codebook.py graph PC2-MODULE-FBA
python3 lifecode_codebook.py sequence CAGTAGAACCGGAACCACCGTGGAA
python3 lifecode_codebook.py measurements CAL-VOCAB
python3 lifecode_codebook.py claims
```

### Windows PowerShell
```powershell
python .\lifecode_codebook.py verify
python .\lifecode_codebook.py stats
```

## Real database-backed browser
This time the HTML must **not** be opened by itself.

Run:
```bash
python3 lifecode_codebook_server.py
```

Then open:
`http://127.0.0.1:8765/`

The browser fetches object/edge/annotation/provenance data from SQLite through the local server. If a database record changes, the UI changes.

## Current seed
- 7 provenance artifacts
- 6 calibration/proof experiments
- 10 scientific/model objects
- 7 structural graph edges
- 190 released measurements
- 3 post-freeze annotation objects
- 4 bounded claims

## Explicit exclusions
- No EXP-0002 outcome values.
- No invented PC0001 sequences.
- No reconstruction of the unmounted v0.0.81 codebook archive.
