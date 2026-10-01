#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path

GROUPS = {
    "OBS": [None],
    "N1_00_24": list(range(0, 25)),
    "N1_25_49": list(range(25, 50)),
    "N1_50_74": list(range(50, 75)),
    "N1_75_98": list(range(75, 99)),
}

def same_or_raise(values, label):
    vals = list(values)
    if not vals:
        raise RuntimeError(f"missing {label}")
    first = vals[0]
    if any(v != first for v in vals[1:]):
        raise RuntimeError(f"inconsistent {label}")
    return first

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--group", required=True, choices=GROUPS)
    ap.add_argument("--out-dir", required=True)
    x = ap.parse_args()

    inp = Path(x.input_dir)
    out = Path(x.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    payloads = []
    for p in sorted(inp.rglob("*.json")):
        obj = json.loads(p.read_text(encoding="utf-8"))
        if obj.get("schema") != "LIFE_CODE_EXP0003_EXECUTION_PACKET_A1_V1":
            continue
        payloads.append(obj)
    if not payloads:
        raise RuntimeError("no A1 packet payloads found")

    by_cell = defaultdict(list)
    for obj in payloads:
        key = (obj["triad_id"], obj["representation"], obj["fold"])
        by_cell[key].append(obj)

    expected = GROUPS[x.group]
    merged_count = 0
    for (tid, rep, fold), parts in sorted(by_cell.items()):
        rows = []
        seen = set()
        for part in parts:
            for row in part["scores"]:
                r = row["replicate"]
                marker = "OBS" if r is None else int(r)
                if marker in seen:
                    raise RuntimeError(f"duplicate replicate {marker} for {tid}/{rep}/{fold}")
                seen.add(marker)
                rows.append(row)

        expected_markers = {"OBS"} if expected == [None] else set(expected)
        if seen != expected_markers:
            raise RuntimeError(
                f"replicate coverage mismatch for {tid}/{rep}/{fold}: "
                f"got={sorted(map(str, seen))} expected={sorted(map(str, expected_markers))}"
            )
        rows.sort(key=lambda r: -1 if r["replicate"] is None else int(r["replicate"]))

        merged = {
            "schema": "LIFE_CODE_EXP0003_PRIMARY_CHUNK_V1",
            "execution_amendment": "EXP-0003-A1",
            "triad_id": tid,
            "representation": rep,
            "fold": fold,
            "chunk": x.group,
            "replicate_ids": [r["replicate"] for r in rows],
            "scores": rows,
            "input_sha256": same_or_raise((p["input_sha256"] for p in parts), "input_sha256"),
            "engine_sha256": same_or_raise((p["engine_sha256"] for p in parts), "engine_sha256"),
            "prod_scorer_sha256": same_or_raise(
                (p["frozen_prod_scorer_sha256"] for p in parts), "frozen_prod_scorer_sha256"
            ),
            "a1_executor_sha256": same_or_raise(
                (p["a1_executor_sha256"] for p in parts), "a1_executor_sha256"
            ),
            "packet_runner_sha256": same_or_raise(
                (p["packet_runner_sha256"] for p in parts), "packet_runner_sha256"
            ),
            "status": "COMPLETE",
        }
        name = f"{tid}_{rep}_{fold}_{x.group}.json"
        (out / name).write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        merged_count += 1

    if merged_count != 48:
        raise RuntimeError(f"expected 48 merged cells for group {x.group}, got {merged_count}")
    print(json.dumps({"status": "COMPLETE", "group": x.group, "n_cells": merged_count}, sort_keys=True))

if __name__ == "__main__":
    main()
