# LIFE-CODE Scientific Release Policy v0.9

1. The Codebook is the scientific product; the UI is a client.
2. No scientific fact originates in presentation code.
3. Public snapshots are generated from the local SQLite Codebook.
4. A public export fails closed if EXP-0002-sensitive or Tier-C records are present.
5. Missing evidence remains missing; it is never filled for presentation convenience.
6. Falsified models remain first-class public records.
7. Post-freeze annotation remains distinguishable from blind discovery.
8. Every public snapshot records its source-database SHA-256.
9. The canonical workstation/archive remains recoverable without Cloudflare or GitHub.
10. Heavy computation stays local or on explicitly rented compute; the public site is primarily read-only.

## Core v0.10 recovery scope

Use `tools/release_v010.py` for this release. Its reviewed-source and experiment allowlists, source-byte checks, coordinate/identity checks, tier checks, and schema allowlist replace the legacy v0.9 publishing command for v0.10. The original archive remains private. This bounded recovery does not implement a general freeze/reveal state machine; historical event timestamps are not reconstructed. Legacy unknown source hashes remain unknown.
