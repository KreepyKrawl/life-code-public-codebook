#!/usr/bin/env python3
"""EXP-0003 A3 N1 one-threshold checkpoint core."""
from pathlib import Path
import shutil
import exp0003_triad_transfer_prod as frozen
import exp0003_triad_transfer_a1 as a1

def prepare(a,b,h,rep,tid,fold,r,root,cap):
    files={}; cell=(tid,fold,int(r))
    for label,p in (("A",a),("B",b),("H",h)):
        for rev in (False,True):
            o="RC" if rev else "FWD"
            q=root/f"{label}_{o}.fa"
            files[(label,o)]=frozen.write_oriented_dataset(p,q,rep,rev,cell)
    train=frozen.build_shards(files[("A","FWD")],root/"train_shards",cap)
    hf=frozen.build_shards(files[("H","FWD")],root/"held_f",cap)
    hr=frozen.build_shards(files[("H","RC")],root/"held_r",cap)
    ladder=frozen.thresholds(files[("A","FWD")],files[("B","FWD")])
    return files,train,hf,hr,ladder

def advance(a,b,h,rep,tid,fold,r,root,state,cap,workers):
    root=Path(root); root.mkdir(parents=True,exist_ok=True)
    if state.get("complete"):
        return state
    files,train,hf,hr,ladder=prepare(a,b,h,rep,tid,fold,r,root,cap)
    if state.get("ladder") is None:
        state["ladder"]=ladder
    elif state["ladder"]!=ladder:
        raise RuntimeError("threshold ladder mismatch")
    i=int(state.get("next_index",0))
    if i!=len(state.get("detail",[])):
        raise RuntimeError("checkpoint index mismatch")
    if i>=len(ladder):
        state["Lstar"]=0; state["complete"]=True; return state
    threshold=ladder[i]
    work=root/f"threshold_{threshold}"
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True); con=None
    try:
        con,ncand,nmatch=a1.candidate_db_parallel(
            train,[files[("B","FWD")],files[("B","RC")]],
            threshold,work/"train",workers)
        row={"threshold":threshold,
             "unique_candidate_sequences":ncand,
             "training_match_records_seen":nmatch}
        best=0
        if ncand:
            best=a1.heldout_best_parallel(
                con,[hf,hr],threshold,work/"held",workers)
            row["transfer_found"]=bool(best)
        state["detail"].append(row); state["next_index"]=i+1
        if best:
            state["Lstar"]=best; state["complete"]=True
        elif state["next_index"]==len(ladder):
            state["Lstar"]=0; state["complete"]=True
    finally:
        if con is not None: con.close()
    shutil.rmtree(work,ignore_errors=True)
    return state
