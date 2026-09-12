# Codebook Core v0.10 release

The September 12 recovery release turns recovered calibration artifacts into queryable evidence. Interface v0.10.0 adds a Recovered evidence page and exposes the new records in the existing reading modes.

## Scientific changes

The frozen PC0001 source names the 25-base block A and the 24-base block B. The v0.8 continuation reversed those names. The migration restores the source identities, corrects the dependent edges and PC1-M02/PC1-M04 measurements, and keeps legacy aliases. The nested core belongs inside B24 at offset four.

The 19 focused occurrences are derived from raw source coordinates and checked against matching substrings of original, hash-verified FASTA records. All 54 shared 16-base vocabulary rows are imported without entropy filtering; their recurrence counts are independently recomputed, allowing overlapping matches and preventing cross-record matches. These counts are vocabulary observations, not new biological-function claims.

## Integrity and disclosure

The original v0.8 database is unchanged. An append-only audit table records 102 changed/added rows, including previous values. One ingestion event records the verified archive and parent hashes. The event date is a recovery date, not an invented freeze/reveal timestamp. The standard-library tools rebuild and validate this bounded calibration release.

Only three reviewed calibration source files are published. Full archive bytes are not mirrored. Legacy source hashes that have not been recovered remain explicit unknowns. The release does not populate historical freeze/reveal events, evolutionary-history edges, or primary EXP-0002 outcomes.

## Next scientific work

Continue staged normalization of the remaining archive, preserving original IDs, predictions, negative results, and semantic boundaries. General freeze/reveal enforcement and history-network ingestion remain separate engineering work. New primary results require their original completion, validation, and reveal gates.
