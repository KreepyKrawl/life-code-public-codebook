#!/usr/bin/env python3
"""UCB-0004X execution-only timestamp canonicalization adapter v1.0.4.

Scientific protocol UCB-0004X v1.0 and the frozen scorer remain unchanged.
The exact hash-pinned Zenodo files use a common monotonic reference timebase with
nominal 4 s sampling but small acquisition jitter. U.csv also contains 80 numeric
control rows while h1.csv/h2.csv contain 81 state rows. The frozen scorer uses the
first column only for structural timebase/sample-period checks; all state/action
values and all scoring use the remaining columns.

This adapter therefore:
1) requires the exact expected numeric shapes and finite, strictly increasing raw
   time columns;
2) replaces ONLY the time column with the canonical nominal grid 0,4,...,320 s;
3) for U.csv, appends one structural final row whose control value duplicates the
   final observed control value. The frozen scorer immediately discards that final
   control value via its existing `[:-1]`, leaving the original 80 control intervals.

No state value, control value used by a transition, threshold, split, seed, null,
model, grammar, classification rule, bridge mapping, or reveal rule is changed.
"""
import argparse
import importlib.util
import sys
from pathlib import Path
import numpy as np

ADAPTER_VERSION = "1.0.4"
FROZEN_RUNNER = Path("cloud/ucb0004x/ucb0004x_target_runner_v1.0.py")


def load_frozen_runner(path: Path):
    spec = importlib.util.spec_from_file_location("ucb0004x_frozen_v1_0", path)
    if spec is None or spec.loader is None:
        raise SystemExit("ADAPTER_IMPORT_FAILED")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def canonicalize_time(arr: np.ndarray, expected_rows: int, name: str) -> np.ndarray:
    if arr.shape[0] != expected_rows:
        raise SystemExit(f"ADAPTER_UNEXPECTED_{name}_ROWS:{arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise SystemExit(f"ADAPTER_NONFINITE_{name}")
    t = arr[:, 0]
    if len(t) < 2 or not np.all(np.diff(t) > 0):
        raise SystemExit(f"ADAPTER_NONMONOTONIC_{name}_TIME")
    out = arr.copy()
    out[:, 0] = np.arange(expected_rows, dtype=float) * 4.0
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    mod = load_frozen_runner(FROZEN_RUNNER)
    original_loader = mod.load_numeric_csv

    def adapted_loader(path):
        arr = original_loader(path)
        name = Path(path).name
        if name == "h1.csv":
            if arr.shape != (81, 11):
                raise SystemExit(f"ADAPTER_UNEXPECTED_H1_SHAPE:{arr.shape}")
            return canonicalize_time(arr, 81, "H1")
        if name == "h2.csv":
            if arr.shape != (81, 11):
                raise SystemExit(f"ADAPTER_UNEXPECTED_H2_SHAPE:{arr.shape}")
            return canonicalize_time(arr, 81, "H2")
        if name == "U.csv":
            if arr.shape != (80, 2):
                raise SystemExit(f"ADAPTER_UNEXPECTED_U_SHAPE:{arr.shape}")
            arr = canonicalize_time(arr, 80, "U")
            sentinel = np.array([[320.0, float(arr[-1, 1])]], dtype=float)
            return np.vstack([arr, sentinel])
        return arr

    mod.load_numeric_csv = adapted_loader
    sys.argv = [str(FROZEN_RUNNER), "--data-dir", args.data_dir, "--output", args.output]
    mod.main()


if __name__ == "__main__":
    main()
