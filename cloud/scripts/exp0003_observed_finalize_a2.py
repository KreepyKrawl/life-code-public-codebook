#!/usr/bin/env python3
"""Validate and finalize one completed EXP-0003 A2 observed checkpoint."""
from pathlib import Path
import argparse
import hashlib
import json


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", required=True)
    ap.add_argument("--out", required=True)
    x = ap.parse_args()

    state_path = Path(x.state)
    s = json.loads(state_path.read_text(encoding="utf-8"))
    if s.get("schema") != "LIFE_CODE_EXP0003_OBS_CHECKPOINT_A2_V1":
        raise SystemExit("unexpected checkpoint schema")
    if s.get("execution_amendment") != "EXP-0003-A2":
        raise SystemExit("unexpected amendment")
    if s.get("replicate") is not None or s.get("null") is not False:
        raise SystemExit("not an observed checkpoint")
    if not s.get("complete"):
        raise SystemExit("A2 observed checkpoint is incomplete")
    if s.get("Lstar") is None:
        raise SystemExit("complete checkpoint missing Lstar")
    if not isinstance(s.get("ladder"), list) or not s["ladder"]:
        raise SystemExit("missing ladder")
    if not isinstance(s.get("detail"), list):
        raise SystemExit("missing detail")
    if int(s.get("next_index", -1)) != len(s["detail"]):
        raise SystemExit("detail/index mismatch")
    if s["next_index"] > len(s["ladder"]):
        raise SystemExit("index exceeds ladder")

    payload = {
        "schema": "LIFE_CODE_EXP0003_OBS_A2_FINAL_V1",
        "execution_amendment": "EXP-0003-A2",
        "triad_id": s["triad_id"],
        "representation": s["representation"],
        "fold": s["fold"],
        "replicate": None,
        "null": False,
        "Lstar": s["Lstar"],
        "detail": s["detail"],
        "input_sha256": s["input_sha256"],
        "engine_sha256": s["engine_sha256"],
        "frozen_prod_scorer_sha256": s["frozen_prod_scorer_sha256"],
        "a2_executor_sha256": s["a2_executor_sha256"],
        "checkpoint_sha256": sha256(state_path),
        "status": "COMPLETE",
    }
    p = Path(x.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    q = p.with_suffix(p.suffix + ".partial")
    q.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    q.replace(p)
    print(json.dumps({
        "status": "FINALIZED",
        "triad_id": payload["triad_id"],
        "representation": payload["representation"],
        "fold": payload["fold"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
