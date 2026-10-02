#!/usr/bin/env python3
"""Outcome-blind threshold-boundary checkpoint executor for EXP-0003 A3 OBS.

This module delegates scientific operations to the frozen production scorer and
only adds restart boundaries between existing frozen thresholds.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import exp0003_triad_transfer_prod as frozen

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


def _prepare_observed(raw_a, raw_b, raw_h, representation, root, shard_bases):
    files = {}
    for label, path in [("A", raw_a), ("B", raw_b), ("H", raw_h)]:
        for rev in (False, True):
            olabel = "RC" if rev else "FWD"
            p = root / f"{label}_{olabel}.fa"
            files[(label, olabel)] = frozen.write_oriented_dataset(
                path, p, representation, rev, None
            )

    train_ref = frozen.build_shards(
        files[("A", "FWD")], root / "shards_trainA", shard_bases
    )
    held_f = frozen.build_shards(
        files[("H", "FWD")], root / "shards_heldF", shard_bases
    )
    held_r = frozen.build_shards(
        files[("H", "RC")], root / "shards_heldR", shard_bases
    )
    ladder = frozen.thresholds(files[("A", "FWD")], files[("B", "FWD")])
    return files, train_ref, held_f, held_r, ladder


def new_state(raw_a, raw_b, raw_h, representation, triad_id, fold_name, shard_bases):
    return {
        "schema": "LIFE_CODE_EXP0003_OBS_CHECKPOINT_A2_V1",
        "execution_amendment": "EXP-0003-A2",
        "triad_id": triad_id,
        "representation": representation,
        "fold": fold_name,
        "replicate": None,
        "null": False,
        "input_sha256": {
            "A": sha256(raw_a),
            "B": sha256(raw_b),
            "H": sha256(raw_h),
        },
        "shard_bases": int(shard_bases),
        "ladder": None,
        "next_index": 0,
        "detail": [],
        "complete": False,
        "Lstar": None,
    }


def validate_state(state, raw_a, raw_b, raw_h, representation, triad_id, fold_name, shard_bases):
    if state.get("schema") != "LIFE_CODE_EXP0003_OBS_CHECKPOINT_A2_V1":
        raise RuntimeError("unexpected checkpoint schema")
    if state.get("execution_amendment") != "EXP-0003-A2":
        raise RuntimeError("unexpected execution amendment")
    if state.get("triad_id") != triad_id:
        raise RuntimeError("triad mismatch")
    if state.get("representation") != representation:
        raise RuntimeError("representation mismatch")
    if state.get("fold") != fold_name:
        raise RuntimeError("fold mismatch")
    if state.get("replicate") is not None or state.get("null") is not False:
        raise RuntimeError("A2 checkpoint must be OBS")
    expected = {"A": sha256(raw_a), "B": sha256(raw_b), "H": sha256(raw_h)}
    if state.get("input_sha256") != expected:
        raise RuntimeError("input hash mismatch")
    if int(state.get("shard_bases")) != int(shard_bases):
        raise RuntimeError("shard size mismatch")
    if not isinstance(state.get("detail"), list):
        raise RuntimeError("detail is not a list")
    if not isinstance(state.get("next_index"), int) or state["next_index"] < 0:
        raise RuntimeError("invalid next_index")
    return state


def advance(raw_a, raw_b, raw_h, representation, triad_id, fold_name, work,
            state=None, max_thresholds=2, shard_bases=frozen.DEFAULT_SHARD_BASES):
    raw_a = Path(raw_a)
    raw_b = Path(raw_b)
    raw_h = Path(raw_h)
    root = Path(work)
    root.mkdir(parents=True, exist_ok=True)

    if state is None:
        state = new_state(
            raw_a, raw_b, raw_h, representation, triad_id, fold_name, shard_bases
        )
    else:
        state = validate_state(
            dict(state), raw_a, raw_b, raw_h, representation, triad_id,
            fold_name, shard_bases
        )

    if state["complete"]:
        if state["Lstar"] is None:
            raise RuntimeError("complete checkpoint missing Lstar")
        return state

    files, train_ref, held_f, held_r, ladder = _prepare_observed(
        raw_a, raw_b, raw_h, representation, root, shard_bases
    )
    if state["ladder"] is None:
        state["ladder"] = ladder
    elif state["ladder"] != ladder:
        raise RuntimeError("threshold ladder mismatch on resume")

    if state["next_index"] != len(state["detail"]):
        raise RuntimeError("checkpoint detail/index mismatch")
    if state["next_index"] > len(ladder):
        raise RuntimeError("checkpoint index beyond ladder")

    stop = min(len(ladder), state["next_index"] + max(1, int(max_thresholds)))
    while state["next_index"] < stop:
        idx = state["next_index"]
        threshold = ladder[idx]
        tw = root / f"threshold_{threshold}"
        if tw.exists():
            shutil.rmtree(tw)
        tw.mkdir(parents=True)

        con = None
        try:
            con, ncand, nmatch = frozen.candidate_db(
                train_ref,
                [files[("B", "FWD")], files[("B", "RC")]],
                threshold,
                tw / "train",
            )
            row = {
                "threshold": threshold,
                "unique_candidate_sequences": ncand,
                "training_match_records_seen": nmatch,
            }
            best = 0
            if ncand:
                best = frozen.heldout_best(
                    con, [held_f, held_r], threshold, tw / "held"
                )
                row["transfer_found"] = bool(best)
            state["detail"].append(row)
            state["next_index"] += 1

            if best:
                state["Lstar"] = best
                state["complete"] = True
                break
        finally:
            if con is not None:
                con.close()
        shutil.rmtree(tw, ignore_errors=True)

    if not state["complete"] and state["next_index"] == len(ladder):
        state["Lstar"] = 0
        state["complete"] = True

    return state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--c", required=True)
    ap.add_argument("--representation", required=True)
    ap.add_argument("--triad-id", required=True)
    ap.add_argument("--fold", required=True, choices=FOLDS)
    ap.add_argument("--state-in")
    ap.add_argument("--max-thresholds", type=int, default=2)
    ap.add_argument("--shard-bases", type=int, default=frozen.DEFAULT_SHARD_BASES)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    x = ap.parse_args()

    A, B, C = map(Path, (x.a, x.b, x.c))
    ta, tb, th = fold_paths(A, B, C, x.fold)

    state = None
    if x.state_in:
        state = json.loads(Path(x.state_in).read_text(encoding="utf-8"))

    out = advance(
        ta, tb, th, x.representation, x.triad_id, x.fold, Path(x.work),
        state=state, max_thresholds=x.max_thresholds,
        shard_bases=x.shard_bases,
    )

    here = Path(__file__).resolve().parent
    out["engine_sha256"] = sha256(here / "exp0003_engine.py")
    out["frozen_prod_scorer_sha256"] = sha256(
        here / "exp0003_triad_transfer_prod.py"
    )
    out["a2_executor_sha256"] = sha256(Path(__file__))

    p = Path(x.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    q = p.with_suffix(p.suffix + ".partial")
    q.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    q.replace(p)

    # Deliberately do not print L*, detail, stopping threshold, or completion
    # state. Those remain inside the sealed computation artifact.
    print(json.dumps({
        "status": "CHECKPOINT_WRITTEN",
        "triad_id": x.triad_id,
        "representation": x.representation,
        "fold": x.fold,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
