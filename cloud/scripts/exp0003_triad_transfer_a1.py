#!/usr/bin/env python3
"""Outcome-blind parallel execution adapter for frozen EXP-0003 scoring.

Scientific semantics are delegated to the frozen production scorer. This module
changes only scheduling of independent MUMmer calls:
- training candidate generation is parallelized across frozen reference shards
  and query orientations;
- held-out membership tests are parallelized across frozen held-out shards.

The candidate set is merged by SQLite UNION semantics (INSERT OR IGNORE), so
L*, null seeds, representations, folds, thresholds, and transfer rules are
unchanged.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import shutil
import sqlite3
import exp0003_triad_transfer_prod as frozen

DEFAULT_WORKERS = 3

def _candidate_part(shard, query, min_len, work, task_id):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    db = work / f"part_{task_id:05d}.sqlite"
    db.unlink(missing_ok=True)
    con = sqlite3.connect(db)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("PRAGMA synchronous=OFF")
    con.execute("PRAGMA temp_store=FILE")
    con.execute("CREATE TABLE candidates(seq BLOB PRIMARY KEY,length INTEGER NOT NULL)")
    refs = frozen.ref_map(shard)
    pending = 0

    def accept(m):
        nonlocal pending
        if m["length"] < min_len:
            return
        rid = m["ref"]
        start = m["ref_pos"] - 1
        end = start + m["length"]
        if rid not in refs:
            raise RuntimeError("unknown reference ID")
        s = refs[rid]
        if start < 0 or end > len(s):
            raise RuntimeError("coordinate outside reference record")
        cand = s[start:end]
        con.execute(
            "INSERT OR IGNORE INTO candidates(seq,length) VALUES(?,?)",
            (cand.encode("ascii"), len(cand)),
        )
        pending += 1
        if pending >= 5000:
            con.commit()
            pending = 0

    try:
        nmatch = frozen.stream_matches(
            shard, query, min_len, accept, work / f"part_{task_id:05d}.stderr"
        )
        con.commit()
    finally:
        con.close()
    return str(db), nmatch

def candidate_db_parallel(train_ref_shards, train_queries, min_len, work, workers=DEFAULT_WORKERS):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    master = work / "candidates.sqlite"
    master.unlink(missing_ok=True)
    con = sqlite3.connect(master)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("PRAGMA synchronous=OFF")
    con.execute("PRAGMA temp_store=FILE")
    con.execute("CREATE TABLE candidates(seq BLOB PRIMARY KEY,length INTEGER NOT NULL)")
    parts = work / "parts"
    if parts.exists():
        shutil.rmtree(parts)
    parts.mkdir(parents=True)

    tasks = []
    task_id = 0
    for shard in train_ref_shards:
        for query in train_queries:
            task_id += 1
            tasks.append((shard, query, min_len, parts, task_id))

    total_matches = 0
    try:
        with ThreadPoolExecutor(max_workers=max(1, int(workers))) as pool:
            futures = [pool.submit(_candidate_part, *t) for t in tasks]
            for fut in as_completed(futures):
                db_path, nmatch = fut.result()
                total_matches += nmatch
                con.execute("ATTACH DATABASE ? AS partdb", (db_path,))
                con.execute("INSERT OR IGNORE INTO candidates(seq,length) SELECT seq,length FROM partdb.candidates")
                con.commit()
                con.execute("DETACH DATABASE partdb")
                Path(db_path).unlink(missing_ok=True)

        con.execute("CREATE INDEX candidates_length_idx ON candidates(length DESC)")
        con.commit()
        n = con.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
        shutil.rmtree(parts, ignore_errors=True)
        return con, n, total_matches
    except Exception:
        con.close()
        raise

def _held_test(shard, cand, L, stderr):
    found = False
    def accept(m):
        nonlocal found
        if m["query"] and m["length"] >= L:
            found = True
    frozen.stream_matches(shard, cand, L, accept, stderr)
    return found

def heldout_best_parallel(con, held_shard_sets, min_threshold, work, workers=DEFAULT_WORKERS):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    lengths = [r[0] for r in con.execute("SELECT DISTINCT length FROM candidates ORDER BY length DESC")]
    workers = max(1, int(workers))
    for L in lengths:
        if L < min_threshold:
            continue
        cur = con.execute("SELECT rowid,seq FROM candidates WHERE length=? ORDER BY rowid", (L,))
        batch = 0
        while True:
            rows = []
            bases = 0
            while len(rows) < frozen.CANDIDATE_BATCH_RECORDS and bases < frozen.CANDIDATE_BATCH_BASES:
                x = cur.fetchone()
                if x is None:
                    break
                rows.append(x)
                bases += L
            if not rows:
                break
            batch += 1
            cand = work / f"candidates_L{L}_b{batch:05d}.fa"
            frozen.write_batch(rows, cand, L)
            pairs = []
            for oi, shards in enumerate(held_shard_sets, 1):
                for si, shard in enumerate(shards, 1):
                    pairs.append((oi, si, shard))
            found = False
            for offset in range(0, len(pairs), workers):
                wave = pairs[offset:offset + workers]
                with ThreadPoolExecutor(max_workers=len(wave)) as pool:
                    futures = [
                        pool.submit(
                            _held_test,
                            shard,
                            cand,
                            L,
                            work / f"held_o{oi}_s{si:05d}_L{L}_b{batch:05d}.stderr",
                        )
                        for oi, si, shard in wave
                    ]
                    if any(f.result() for f in futures):
                        found = True
                if found:
                    break
            cand.unlink(missing_ok=True)
            if found:
                return L
    return 0

def score_fold(raw_a, raw_b, raw_h, representation, triad_id, fold_name, replicate, work,
               shard_bases=frozen.DEFAULT_SHARD_BASES, workers=DEFAULT_WORKERS):
    root = Path(work)
    root.mkdir(parents=True, exist_ok=True)
    null_cell = None if replicate is None else (triad_id, fold_name, int(replicate))
    files = {}
    for label, path in [("A", raw_a), ("B", raw_b), ("H", raw_h)]:
        for rev in (False, True):
            olabel = "RC" if rev else "FWD"
            p = root / f"{label}_{olabel}.fa"
            files[(label, olabel)] = frozen.write_oriented_dataset(
                path, p, representation, rev, null_cell
            )

    train_ref = frozen.build_shards(files[("A", "FWD")], root / "shards_trainA", shard_bases)
    held_f = frozen.build_shards(files[("H", "FWD")], root / "shards_heldF", shard_bases)
    held_r = frozen.build_shards(files[("H", "RC")], root / "shards_heldR", shard_bases)
    ladder = frozen.thresholds(files[("A", "FWD")], files[("B", "FWD")])
    detail = []

    for threshold in ladder:
        tw = root / f"threshold_{threshold}"
        if tw.exists():
            shutil.rmtree(tw)
        tw.mkdir(parents=True)
        con = None
        try:
            con, ncand, nmatch = candidate_db_parallel(
                train_ref,
                [files[("B", "FWD")], files[("B", "RC")]],
                threshold,
                tw / "train",
                workers,
            )
            row = {
                "threshold": threshold,
                "unique_candidate_sequences": ncand,
                "training_match_records_seen": nmatch,
            }
            if ncand:
                best = heldout_best_parallel(
                    con, [held_f, held_r], threshold, tw / "held", workers
                )
                row["transfer_found"] = bool(best)
                detail.append(row)
                if best:
                    con.close()
                    con = None
                    shutil.rmtree(tw, ignore_errors=True)
                    return best, detail
            else:
                detail.append(row)
        finally:
            if con is not None:
                con.close()
        shutil.rmtree(tw, ignore_errors=True)
    return 0, detail
