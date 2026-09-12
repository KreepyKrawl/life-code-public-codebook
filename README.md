# LIFE-CODE Public Codebook

**Codebook Core v0.10 · Interface v0.10.0**

[Open the live Codebook](https://kreepykrawl.github.io/life-code-public-codebook/).

The recovered calibration evidence is now part of the database and website:

- Three PC0001 literals and 19 focused locations checked against the original hash-verified genome files.
- All 54 shared exact 16-base vocabulary sequences, with occurrence counts independently checked in all three pilot genomes. Low-complexity sequences are retained.
- Corrected A25/B24 identities, containment, directional edges, and length measurements; two legacy IDs resolve through explicit aliases.
- 102 before/after audit records, one ingestion event, and source-to-archive provenance links. Original freeze timestamps are not invented.
- Searchable recovered evidence, location tables in all reading modes, original-source downloads, and complete JSON/SQLite exports.

The public dataset retains 10 objects, 7 structural edges, 190 measurements, 3 post-freeze annotations, and 4 bounded claims. There are still **zero object-specific evolutionary history assertions**. The full historical graph is not yet normalized. EXP-0002 outcomes remain excluded.

## Run locally

Python 3.10+; no external dependencies:

```sh
python lifecode_codebook_server.py
python lifecode_codebook.py show PC1-BLOCK-A24
python tools/release_v010.py downloads/LIFE_CODE_CODEBOOK_CORE_v0.10.sqlite
python tools/test_release_v010.py
```

The first command serves the site and read-only API at http://127.0.0.1:8765/. The second resolves an older ID to its corrected record.

## Rebuild from the protected archive

Keep the original archive private and unchanged. Its required SHA-256 is `081ad5bab0cb2c125297b9acb32905fca70f9d09d5e0911f75e91f5a6d9f44e2`.

```sh
python tools/build_core_v010.py --parent LIFE_CODE_CODEBOOK_CONTINUATION_v0.8.sqlite --archive /path/to/LIFE_CODE_CODEBOOK_v0.0.81.zip --output /tmp/rebuilt-v010.sqlite --sources /tmp/rebuilt-sources
```

The builder refuses to overwrite an existing output. It checks the parent, archive, three reviewed source files, genome hashes, focused substrings, independent block table, and all vocabulary occurrence counts. It does not ingest primary EXP-0002 outputs. Earlier releases remain available unchanged.

Current release hashes are in `SHA256SUMS-v0.10.txt`. See `docs/RELEASE_v0.10.md` for the scope and remaining work, and `SCIENTIFIC_RELEASE_POLICY.md` for disclosure rules.
