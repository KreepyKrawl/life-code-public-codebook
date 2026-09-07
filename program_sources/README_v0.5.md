# LIFE-CODE Prediction Contract Bundle v0.5

Date: 2026-09-03

This C-pass formalizes the bridge between Biological Diff and the future Morph / Possibility Engine. It does not expose or use unreleased EXP-0002 results.

## Canonical rule added

**THE PACKET, NOT THE PICTURE, IS THE PREDICTION.** A renderer is downstream of scientific inference and cannot add scientific privilege. Every visualized trait must be represented in a frozen phenotype-state packet with provenance, support, uncertainty, constraints, and a declared prediction maturity level.

## Four contracts

1. **Inference contract** — explicit machine-readable phenotype channels only.
2. **Freeze contract** — prediction packet, model/config and input hashes sealed before reveal.
3. **Render contract** — renderer may visualize but may not silently invent predicted biological features.
4. **Score contract** — structured packet is scored after reveal; visual attractiveness is irrelevant.

## Files

- `LIFE_CODE_PREDICTION_CONTRACT_v0.5_2026-09-03.docx` — canonical C-pass architecture.
- `LIFE_CODE_PREDICTION_PACKET_LAB_v0.5.html` — static local demo of a synthetic P2 Blind Morph Reveal.
- `LIFE_CODE_PHENOTYPE_STATE_PACKET_SCHEMA_v0.1.json` — prediction packet schema.
- `LIFE_CODE_PREDICTION_REVEAL_SCHEMA_v0.1.json` — post-freeze truth-reveal schema.
- `LIFE_CODE_PREDICTION_SCORECARD_SCHEMA_v0.1.json` — score output schema.
- `lifecode_prediction_score.py` — runnable v0.1 score engine.
- `phenotype_packet.example.json`, `prediction_reveal.example.json`, `prediction_scorecard.example.json` — synthetic fixtures.

## Scoring principle

No single “AI confidence” number is authoritative. The first score engine preserves separate dimensions: categorical/discrete accuracy, probability calibration (Brier), continuous error, constraint integrity, uncertainty, out-of-distribution distance, support density and provenance. A future benchmark composite may exist for leaderboard convenience, but it cannot replace the multidimensional scientific scorecard.

## New visual truth state

`RETRODICTED` is now an explicit claim mode alongside OBSERVED, RECONSTRUCTED, LATENT, INTERPOLATED, EXTRAPOLATED, COUNTERFACTUAL and UNSUPPORTED. It identifies a state that is real but was deliberately hidden from the inference system until after freeze.

## Immediate next target

Implement the **feature-to-pixel provenance map** and **mask-level scoring** for BENCH-P01 so each rendered wing region is traceable to a packet channel and can be compared to a held-out real phenotype mask without relying on visual judgment.
