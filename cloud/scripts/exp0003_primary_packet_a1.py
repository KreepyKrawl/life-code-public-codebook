#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path
import exp0003_engine as engine
import exp0003_triad_transfer_prod as frozen
import exp0003_triad_transfer_a1 as a1

REPS = ["ACGT", "RY", "MK", "WS", *engine.CONTROL_TUPLES.keys()]
FOLDS = ("AB_C", "AC_B", "BC_A")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def fold_paths(a, b, c, fold):
    if fold == "AB_C":
        return a, b, c
    if fold == "AC_B":
        return a, c, b
    if fold == "BC_A":
        return b, c, a
    raise ValueError(fold)

def packet_replicates(packet):
    if packet == "OBS":
        return [None]
    m = re.fullmatch(r"N1_(\d{2})_(\d{2})", packet)
    if not m:
        raise ValueError(packet)
    lo, hi = map(int, m.groups())
    if not (0 <= lo <= hi <= 98):
        raise ValueError(packet)
    return list(range(lo, hi + 1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--c", required=True)
    ap.add_argument("--representation", required=True, choices=REPS)
    ap.add_argument("--triad-id", required=True)
    ap.add_argument("--fold", required=True, choices=FOLDS)
    ap.add_argument("--packet", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=a1.DEFAULT_WORKERS)
    ap.add_argument("--shard-bases", type=int, default=frozen.DEFAULT_SHARD_BASES)
    x = ap.parse_args()

    A, B, C = map(Path, (x.a, x.b, x.c))
    ta, tb, th = fold_paths(A, B, C, x.fold)
    reps = packet_replicates(x.packet)
    rows = []
    root = Path(x.work)
    root.mkdir(parents=True, exist_ok=True)

    for r in reps:
        w = root / ("OBS" if r is None else f"N1_{r:02d}")
        val, detail = a1.score_fold(
            ta, tb, th, x.representation, x.triad_id, x.fold, r, w,
            x.shard_bases, x.workers
        )
        rows.append({"replicate": r, "Lstar": val, "detail": detail})

    here = Path(__file__).resolve().parent
    payload = {
        "schema": "LIFE_CODE_EXP0003_EXECUTION_PACKET_A1_V1",
        "execution_amendment": "EXP-0003-A1",
        "triad_id": x.triad_id,
        "representation": x.representation,
        "fold": x.fold,
        "packet": x.packet,
        "replicate_ids": [r["replicate"] for r in rows],
        "scores": rows,
        "input_sha256": {"A": sha256(A), "B": sha256(B), "C": sha256(C)},
        "engine_sha256": sha256(here / "exp0003_engine.py"),
        "frozen_prod_scorer_sha256": sha256(here / "exp0003_triad_transfer_prod.py"),
        "a1_executor_sha256": sha256(here / "exp0003_triad_transfer_a1.py"),
        "packet_runner_sha256": sha256(Path(__file__)),
        "workers": x.workers,
        "shard_bases": x.shard_bases,
        "status": "COMPLETE",
    }
    Path(x.out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "COMPLETE",
        "triad_id": x.triad_id,
        "representation": x.representation,
        "fold": x.fold,
        "packet": x.packet,
        "n_scores": len(rows),
    }, sort_keys=True))

if __name__ == "__main__":
    main()
