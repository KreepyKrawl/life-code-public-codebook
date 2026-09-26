#!/usr/bin/env python3
"""UCB-0004X execution-only input-shape adapter v1.0.1.

This adapter does not alter the frozen UCB-0004X scoring logic. It imports the
hash-pinned v1.0 target runner and only canonicalizes U.csv from the 80 numeric
control-interval rows returned by the frozen CSV loader to the 81-row shape the
frozen runner expects. The appended 81st control row is a structural sentinel:
its time is last_time + 4 s and its control value duplicates the preceding row.
The frozen runner itself discards that final control value via `[:-1]`, so no
observed transition, threshold, seed, null, split, model, or score is changed.
"""
import argparse
import importlib.util
import sys
from pathlib import Path
import numpy as np

ADAPTER_VERSION = "1.0.1"
FROZEN_RUNNER = Path("cloud/ucb0004x/ucb0004x_target_runner_v1.0.py")


def load_frozen_runner(path: Path):
    spec = importlib.util.spec_from_file_location("ucb0004x_frozen_v1_0", path)
    if spec is None or spec.loader is None:
        raise SystemExit("ADAPTER_IMPORT_FAILED")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    mod = load_frozen_runner(FROZEN_RUNNER)
    original_loader = mod.load_numeric_csv

    def adapted_loader(path):
        arr = original_loader(path)
        p = Path(path)
        if p.name != "U.csv":
            return arr
        if arr.shape != (80, 2):
            raise SystemExit(f"ADAPTER_UNEXPECTED_U_NUMERIC_SHAPE:{arr.shape}")
        if not np.all(np.isfinite(arr)):
            raise SystemExit("ADAPTER_NONFINITE_U")
        if not np.allclose(np.diff(arr[:, 0]), 4.0, atol=1e-9, rtol=0):
            raise SystemExit("ADAPTER_U_SAMPLE_PERIOD_MISMATCH")
        sentinel = np.array([[float(arr[-1, 0]) + 4.0, float(arr[-1, 1])]], dtype=float)
        return np.vstack([arr, sentinel])

    mod.load_numeric_csv = adapted_loader
    sys.argv = [str(FROZEN_RUNNER), "--data-dir", args.data_dir, "--output", args.output]
    mod.main()


if __name__ == "__main__":
    main()
