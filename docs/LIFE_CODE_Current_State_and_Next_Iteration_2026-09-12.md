# LIFE-CODE current state and next iteration

The next scientific release should be **Codebook Core v0.10: verified recovery, deterministic ingestion, and traceable evidence**. The existing public interface already presents the broader project through CODE, HISTORY, POSSIBILITY, and RESILIENCE. The immediate opportunity is to connect that interface to more of the recovered scientific record, while correcting documented conflicts and retaining the experiment’s reveal barrier. This recommendation follows the published mainline recovery lock rather than inventing a new direction.[1]

This assessment has a September 12, 2026 cutoff. Public deployment and archive integrity were directly checked. Current workstation activity is reported by the operator; no direct inspection of the Windows/WSL experiment was available. Private recovery history provides useful operational checkpoints, but it does not substitute for a validated final experiment bundle.[2]

## Current state

| Layer | Established state | Meaning for the next iteration |
|---|---|---|
| Public hosting | GitHub Pages responds successfully; its HTML identifies interface v0.9.4 | Continue from the deployed site. No new hosting migration is needed for this release. |
| Repository | Main is commit `14131542d3793be1a2c2e41519ad63864645635a`, September 7; Pages deployment succeeded | This is the public implementation baseline, superseding older local drafts. |
| Scientific snapshot | Public v0.9, generated September 4 from SQLite Core v0.8 | Interface version changes have not increased the released scientific dataset. |
| Released records | 10 objects, 7 structural edges, 190 measurements, 4 claims, 0 occurrence rows | The public evidence store is real but remains a small continuation core. |
| Historical archive | v0.0.81 recovered; original size, SHA-256, and ZIP integrity verified | Reconciliation can now use actual source artifacts. |
| History capability | Ontology exposed; 0 released object-specific history edges | Defined vocabulary is not a populated evolutionary history network. |
| Prediction/resilience | Contracts and benchmark designs are public context | No predictive or longevity result follows from those pages. |
| EXP-0002 | Latest message reports it running following recovery; completion/reveal not established here | Preserve the frozen experiment and separate operational progress from scientific outcomes. |

The live URL is [LIFE-CODE Public Codebook](https://kreepykrawl.github.io/life-code-public-codebook/). The public snapshot’s exact downloaded SHA-256 is `44a204e458dbf9794d950ca506322835fc0f6d3e4fc8bbdd98e9fcb849bfe030`. Its JSON and JavaScript representations contain equal scientific data. The recorded source-database hash is `63910fdf80df38e543cb3b755c60cd3ce146e58140ab7fae9e051153b05b93bb`.[3–5]

Successful delivery of the page and data does not establish usability or accessibility conformance. The current review inspected source and deployment evidence, not a complete interactive browser or assistive-technology test.

## Recovery chronology and experiment boundary

The September 3 project-control files preserve an earlier state: ten sealed triads, A2 MAX_K complete, and an A2 longest-block checkpoint without its final result. Those files are useful historical records, but their status should no longer be displayed as the latest operational observation.[2]

Retrieved September 12 conversation context records a later parent-run attempt that recognized B1 through A2 as sealed and accepted A3 MAX_K, then failed at A3 LONGEST_BLOCK with `RuntimeError: mummer not found`. A subsequent attempt reportedly exited without output and showed no matching process. The environment check then located MUMmer in the `lifecode-exp0002-primary` environment. The latest operator report says the experiment is now running in the background.[2]

These observations support a bounded recovery narrative: progress survived the crash, the recorded continuation point moved into A3, and executable resolution interfered with resumption. They do not establish A3 completion, validate the entire sealed bundle, or justify interpreting the hierarchy score. The retrieved conversation is a secondary record of console observations; a fresh artifact inventory would be stronger evidence.

The next Codebook should distinguish three independent dimensions:

| Dimension | Example values | Why it matters |
|---|---|---|
| Execution | Running, checkpointed, failed, complete | A process can be running without a final result. |
| Validation | Unchecked, verified, rejected | A result file can exist without passing validation. |
| Disclosure | Sealed, released | A complete validated result may still be withheld pending the prescribed reveal. |

On the public site, “SEALED” should mean **results withheld under the release policy**, not imply that all computation is complete. Show a timestamp and evidence basis for operational status; avoid implying live telemetry when the source is a dated manual report. The public page does not need partial values, rankings, trends, or a progress percentage derived from scientific outputs.

Recovery evidence belongs in an operational audit: input identity, executable/version resolution, checkpoint identity, continuation command, resume validation, and final completion validation. Restore the required environment without changing the scientific procedure. Existing completed triads should not be rerun merely to simplify the workflow. The final bundle and reveal rules remain prerequisites for scientific interpretation.[1–2]

## Recovered archive and reconciliation findings

The protected archive is present at its original 112,174,983 bytes, with SHA-256 `081ad5bab0cb2c125297b9acb32905fca70f9d09d5e0911f75e91f5a6d9f44e2`. A fresh ZIP integrity test passed. Its extracted tree contains 594 files and 69 entry JSON files. Archive recovery is therefore established; full normalization into the continuation database is not.[6]

The live database still describes that archive as unmounted and leaves three PC0001 sequence fields NULL. That statement was appropriate for the original September 4 snapshot. It should remain intact in that immutable release, while a new release records the changed evidence state. The current frontier can now distinguish “archive verified” from “migration pending.”[4,6]

### PC0001 identity conflict

The frozen raw recurrence result establishes the following identities.[7]

| Raw source identity | Exact literal | Length | Recovery scope |
|---|---|---:|---|
| block_a | `CCGCCTGGGGAGTACGGCCGCAAGG` | 25 bp | Five E. coli and one Pyrococcus occurrences |
| block_b | `TAAGGTAGCGAAATTCCTTGTCGG` | 24 bp | Five E. coli and one Pyrococcus occurrences |
| core_0001 | `GTAGCGAAATTCCTTG` | 16 bp | Five E. coli, one Pyrococcus, one yeast mitochondrial occurrence |

The public continuation instead uses `PC1-BLOCK-A24` and `PC1-BLOCK-B25`, placing the nested core in the former. This is an A/B naming conflict between source and continuation, not evidence for a new biological result. The raw coordinates place the source’s A25 before B24; the core starts four bases inside B24.[4,7]

A correction must cover the whole dependency graph: identifiers and aliases, labels, containment, directional edges, module membership, length measurements, explanations, and exports. A September 5 local v0.9.1 draft already restores sequences and 19 occurrences, but direct inspection found its `block_a_length` and `block_b_length` measurements still set to 24 and 25. It must not be promoted wholesale. Its occurrence tuples also place record or strain identifiers in fields labeled assembly accession, requiring explicit source reconciliation.[8]

The recovered source supplies record identifiers and input hashes. Preserve these exactly. An assembly accession, sequence-record accession, chromosome label, strain name, and coordinate system are separate facts. Unknown assembly metadata should remain unknown until resolved from an authoritative artifact.

The released PC0002 C25 and D17 sequences were also checked: their actual lengths are 25 and 17, and both match their stored sequence hashes. There is no established length defect in those objects. That positive check prevents an unresolved concern in older draft notes from becoming an invented correction.[4]

### Historical research frontier

The archive contains considerably more research than the ten public objects. It includes masked-representation work, transfer tests, model revisions, prediction records, negative results, and explicit interpretation boundaries. These should be reconciled as evidence records, not condensed into an unqualified success story.

At the archive cutoff, model v3 was a development model trained on twenty previously observed genomes. Its positive direction in 12/20 leave-one-genome-out diagnostics is explicitly descriptive development evidence, not prospective validation. Predictions LC-PRED-0049 through LC-PRED-0051 were frozen for a fresh six-genome panel; acquisition, scanner, boundary analysis, and prediction status were all `NOT_RUN`.[9]

That fresh-panel track must remain separate from EXP-0002 and from the butterfly or rockfish benchmark designs. No newly retrieved artifact establishes that the fresh-panel predictions have since been adjudicated. Preserve their frozen tests and label the status as the last recovered archive state, with its version attached.

Archive preservation and public release are different operations. Retain all original bytes privately. Release only reviewed material whose provenance and disclosure status are established, including documentation, attachments, and derived exports. A blanket documentation mirror is not a substitute for record-level release review.

## Scientific goals that the next release must preserve

The recovered mainline defines LIFE-CODE as annotation-blind genomic decompilation and software archaeology. The operating sequence is discovery of recurring sequence structure and relationships, freezing those candidates, and adding biological interpretation afterward. The Codebook is the scientific product; the website is its client.[1,10]

The four public pillars are complementary:

| Pillar | Public question | Required scientific substance |
|---|---|---|
| CODE | What is actually there? | Literal or represented objects, physical relationships, coordinates, experiments, and provenance |
| HISTORY | How did it get here? | Evidence-bounded history edges with alternatives and unresolved states |
| POSSIBILITY | What other states might be reachable? | Frozen prediction packets, held-out retrodiction, constraints, scoring, and uncertainty |
| RESILIENCE | How does life survive failure? | Controlled comparisons of repeated biological solutions, including contradictory branches |

The history model already allows inheritance, duplication, degradation, rearrangement, repurposing, horizontal transfer, viral insertion, plasmid exchange, merger/endosymbiosis candidates, and unknown relationships. Seven existing structural edges must not be relabeled as seven historical events. Object-specific history requires its own evidence.[10]

The mitochondrial calibration supports a bounded historical interpretation; it does not reconstruct the complete endosymbiotic merger. Similarity alone does not distinguish inheritance, transfer, contamination, convergence, or assembly artifacts. A useful History view must display competing explanations and why an assignment remains unresolved.

The downstream predictive architecture remains `Codebook → Biological Diff → constraints/reachability → frozen prediction packet → renderer`. A visually persuasive output cannot increase evidence strength. Every scientific visual element needs a provenance path, and the prediction packet is what gets frozen and scored.[1,11]

BENCH-P01A is currently an ingestion contract for a published 113-subject butterfly cohort, with a specified 91/22 train/holdout split. The contract’s existence is not proof that ingestion, model fitting, holdout prediction, or scoring occurred. BENCH-R01 remains a resilience benchmark design. These are appropriate roadmap items; they should not be presented as achieved predictive capabilities.[11]

## Recommended Core v0.10 scope

The published September 5 lock already names deterministic ingestion, immutable ingest/freeze/reveal events, recursive provenance, stable IDs, and a history-network schema as the next target. Archive recovery makes that work more concrete. The limited local v0.9.1 draft should be treated as a source of candidate changes for review, while the September 7 deployed interface remains the website baseline.[1,8]

| Priority | Deliverable | Acceptance condition |
|---|---|---|
| 1 | Recovery inventory and source ledger | Every retained artifact has identity, hash, role, disclosure status, and reconciliation state. |
| 2 | PC0001 audited correction | Raw literals and coordinates generate records; all dependent measurements/edges agree; legacy links resolve. |
| 3 | Deterministic ingestion | The same frozen sources and configuration reproduce the same scientific records and stable IDs. |
| 4 | Provenance and event records | Each object, measurement, and claim can be traced to its source and relevant freeze/reveal events. |
| 5 | Public release enforcement | Unknown disclosure states fail closed; all exported scientific tables and downloadable artifacts are checked. |
| 6 | Historical graph normalization | Predictions, failures, boundaries, and unresolved states survive migration with original IDs or explicit mappings. |
| 7 | Website integration | All reading modes expose the same corrected records, with clear provenance and current release metadata. |

The existing exporter checks sensitivity flags and Tier-C records across several central tables. The separate snapshot validator is narrower: it checks the gate flag, Tier-C objects, artifact names, and sequence hashes. It does not independently enforce coordinate validity, length equality, source referential integrity, or all disclosure relationships. Some tables are exported wholesale. This establishes a coverage gap as the schema grows; it does not establish that the current snapshot contains a leak.[12]

Release tests should target those concrete risks: a sensitive dependency anywhere in an exported provenance path; an unapproved annotation or occurrence; a mismatched length or coordinate basis; a dangling legacy ID; and an explanation referring to superseded A/B labels. Require parsed equality between public JSON and browser data, which currently passes. Separate deterministic scientific content from generation timestamps so reproducibility does not depend on incidental packaging time.

Do not make final EXP-0002 results a dependency for these engineering improvements. The work can use already released calibration evidence while the sealed experiment continues. If the final experiment later passes its prescribed validation and reveal, ingest it as a separate versioned evidence release.

## Scientist and pre-teen accessibility

The current site already offers Explore, Learn, and Research modes, a glossary, failed-model pages, and claim boundaries. Continue that design rather than creating two disconnected products. The same object should retain its identity, values, evidence state, caveats, and sources in every mode.[3–4]

A strong evidence page has four layers: a short plain-language finding, the test that produced it, the limits of the conclusion, and the complete record. Technical terms should remain available beside their explanation. For example, “annotation-blind” can be introduced as “we searched the DNA before looking up the biological labels.” This describes the procedure without implying that all prior biological knowledge was absent.

For PC0001, an approachable explanation could read: “We found matching DNA pieces in very different kinds of life. In two genomes, some pieces also appeared in a repeated neighborhood. We locked those findings before looking up their biological labels. That helps test the search method, but it does not show that every DNA piece has the same job.” The Research layer would expose the exact literals, occurrences, orientation, spacing definition, null procedure, post-freeze annotations, and bounded claims.[1,7]

Analogy should introduce a question, never supply evidence. “DNA detective work” can explain searching and checking. Calling every repeated sequence an instruction, or treating all genomes as interchangeable software, would exceed the evidence. Failed models should remain as easy to find as positive calibrations.

W3C guidance supports short, clear text, literal wording, explanations of implied content, and alternatives to numerically demanding explanations. WCAG 2.2’s Reading Level criterion supports supplemental accessible content for advanced text; it is an AAA criterion, not a claim that the whole site meets AAA. The next interface review should also test applicable AA requirements such as text contrast and visible keyboard focus.[13–14]

Use comprehension tasks as well as readability checks. A younger reader should be able to say what was measured, what remains unknown, and why a failed model matters. A scientist should be able to reach the source, reproduce a selected derivation, distinguish discovery from later annotation, and inspect a correction’s audit trail. Both should identify whether a picture is observed, reconstructed, predicted, or hypothetical. These are proposed acceptance tests, not completed user-study findings.

## Release decision

Proceed with **Core v0.10 reconciliation and provenance**, followed by a separately versioned interface update consuming its gated snapshot. Preserve the live v0.9.4 reading modes and four pillars. Correct the frontier so it reports the archive as verified but reconciliation incomplete. Keep all running-experiment outcomes behind the original reveal barrier.

The recovery has restored the inputs for a more complete and auditable Codebook. It has not yet established a complete historical migration, populated history network, successful phenotype predictor, or final EXP-0002 result. Those distinctions should be visible to both audiences and machine-enforced beneath the website.

## Sources

1. LIFE-CODE, [Mainline Recovery & Continuation Lock v0.10](https://github.com/KreepyKrawl/life-code-public-codebook/blob/14131542d3793be1a2c2e41519ad63864645635a/program_sources/LIFE_CODE_MAINLINE_RECOVERY_LOCK_v0.10_2026-09-05.md), September 5, 2026, sections 1–11. A controlling design/status record; stale mount-dependent statements are reconciled in this report.
2. Private project records: `LIFE_CODE_BOOK_CONTROL_v0.1.md`, `LIFE_CODE_PROJECT_MASTER_INDEX_2026-09-03.md`; retrieved conversation “Recover experiment data,” September 12, 2026, observations around 21:21–21:24 UTC; latest operator message in this conversation reporting background execution. Conversation retrieval supplies summarized observations, not independently verified current workstation files.
3. LIFE-CODE, [live website](https://kreepykrawl.github.io/life-code-public-codebook/), inspected September 12, 2026; [Pages deployment run 34154497543](https://github.com/KreepyKrawl/life-code-public-codebook/actions/runs/34154497543), successful September 7, 2026.
4. LIFE-CODE, [Public Codebook v0.9 JSON](https://kreepykrawl.github.io/life-code-public-codebook/data/LIFE_CODE_PUBLIC_CODEBOOK_v0.9.json), generated September 4, 2026; downloaded and inspected September 12. Counts, sequences, missing values, metadata, and data equality checked directly.
5. LIFE-CODE, [repository README at reviewed commit](https://github.com/KreepyKrawl/life-code-public-codebook/blob/14131542d3793be1a2c2e41519ad63864645635a/README.md), September 7, 2026.
6. `LIFE_CODE_CODEBOOK_v0.0.81.zip`, recovered private archive. Size, SHA-256, ZIP integrity, and extracted inventory checked September 12, 2026. Exact archive hash is recorded in this report.
7. Archive source `sources/PC1_RAW_RECURRENCE_RESULTS.json`, sections `input_validation` and `focus_cluster`; SHA-256 `c31705d4869ec3085444126fd83ad57583a66f52583f928791a4bb75c704c6d5`. Private recovered source, directly inspected.
8. Local draft `LIFE_CODE_CODEBOOK_CONTINUATION_v0.9.1.sqlite` and `tools/migrate_v0_8_to_v0_9_1.py`, September 5 development branch. Inspected September 12; not the current public deployment. Measurements PC1-M02 and PC1-M04 and occurrence construction reviewed directly.
9. Archive documents `196_BOUNDARY_RESIDUAL_MODEL_v3_RESULT.md`, `198_MODEL_V3_FRESH_VALIDATION_PANEL_PREREG_v1.md`, and `199_MODEL_V3_FRESH_VALIDATION_PANEL_FREEZE_v1.json`. Private recovered sources; development/validation distinction and NOT_RUN states inspected directly.
10. LIFE-CODE, [Framework Context v0.9.4](https://github.com/KreepyKrawl/life-code-public-codebook/blob/14131542d3793be1a2c2e41519ad63864645635a/data/LIFE_CODE_FRAMEWORK_CONTEXT_v0.9.4.json), September 7, 2026; pillars, evidence states, visual states, history ontology, frontier.
11. LIFE-CODE, [Program Context v0.9.4](https://github.com/KreepyKrawl/life-code-public-codebook/blob/14131542d3793be1a2c2e41519ad63864645635a/data/LIFE_CODE_PROGRAM_CONTEXT_v0.9.4.json), September 7, 2026; predictive architecture and benchmark contracts. Cohort figures are cited as contract contents, not independently reanalyzed study data.
12. LIFE-CODE, [Scientific Release Policy](https://github.com/KreepyKrawl/life-code-public-codebook/blob/14131542d3793be1a2c2e41519ad63864645635a/SCIENTIFIC_RELEASE_POLICY.md), [snapshot publisher](https://github.com/KreepyKrawl/life-code-public-codebook/blob/14131542d3793be1a2c2e41519ad63864645635a/tools/publish_public_snapshot.py), and [snapshot validator](https://github.com/KreepyKrawl/life-code-public-codebook/blob/14131542d3793be1a2c2e41519ad63864645635a/tools/validate_public_snapshot.py), reviewed September 12, 2026.
13. W3C, [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/), criteria 1.4.3, 2.4.7, and 3.1.5; accessed September 12, 2026.
14. W3C Web Accessibility Initiative, [Use Clear and Understandable Content](https://www.w3.org/WAI/WCAG2/supplemental/objectives/o3-clear-content/), supplemental cognitive accessibility guidance; accessed September 12, 2026.
