# UCB-0004X Execution Amendment v1.0.4

Date: 2026-09-28
Scientific protocol: UCB-0004X v1.0 (unchanged)
Execution patch: v1.0.4
Prior execution attempts preserved: 36273814889, 36275536604, 36279396238, 36279557473

## Failure observed

After GitHub-hosted runner allocation resumed, the exact authorized Zenodo files were downloaded and all frozen MD5 checks passed. The v1.0.1 shape adapter then stopped before producing any target result with:

`ADAPTER_U_SAMPLE_PERIOD_MISMATCH`

Inspection was restricted to execution structure needed to diagnose the parser failure. The exact files show one shared monotonic reference timebase with nominal 4 s sampling and small acquisition jitter; the largest observed deviation of an adjacent interval from exactly 4 s is about 0.001535 s. h1.csv and h2.csv contain 81 numeric state rows; U.csv contains 80 numeric control rows. No UCB target score/signature, null outcome, held-out classification, bridge result, or LIFE-CODE EXP-0003 output was inspected.

## Repair classification

Implementation / timebase canonicalization only. No scientific hypothesis, state threshold, operation threshold, discovery/validation/holdout split, Jeffreys alpha, null count, random seed, grammar, wrong-grammar control, identifiability rule, classification threshold, bridge mapping, or reveal rule is changed.

The source files remain hash-pinned by the original frozen MD5 checks. The time column is not used by the frozen scorer to construct state bits, action bits, transition counts, model probabilities, nulls, or scores; it is used only for shape/timebase/sample-period validation.

## Frozen repair

The original scorer remains byte-identical at its frozen SHA-256.

A new execution-only adapter v1.0.4 imports the frozen scorer and changes only the representation of the reference-time column presented to it:

- h1.csv and h2.csv must still decode to exactly 81 x 11 numeric arrays.
- U.csv must still decode to exactly 80 x 2 numeric rows.
- all values must be finite and raw time columns must be strictly increasing.
- the three reference-time columns are canonicalized to the documented nominal sampling grid `0, 4, 8, ..., 320` seconds.
- U.csv receives one structural final row at 320 s carrying a duplicate of its final observed control value; the frozen scorer immediately removes that final control value via its pre-existing `[:-1]`, preserving the original 80 observed control intervals.

All non-time columns remain byte-derived from the exact hash-pinned inputs and are not modified by the adapter.

## Integrity consequence

This repair is downstream of input identity verification and upstream of any target outcome production. It resolves a structural parser assumption about exact floating-point timestamps; it does not refit or alter the scientific test. The earlier failed attempts remain part of the audit chain. UCB-0004X remains eligible for its preregistered interpretation if the amended execution completes and all frozen gates remain satisfied.
