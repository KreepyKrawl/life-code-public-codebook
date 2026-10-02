#!/usr/bin/env python3
"""EXP-0003 A3 N1 threshold checkpoint wrapper."""
from pathlib import Path
import argparse,json
import exp0003_triad_transfer_prod as frozen
import exp0003_engine as engine
import exp0003_n1_checkpoint_core_a3 as core

REPS=["ACGT","RY","MK","WS",*engine.CONTROL_TUPLES.keys()]
FOLDS=("AB_C","AC_B","BC_A")

def fold_paths(a,b,c,fold):
    return {"AB_C":(a,b,c),"AC_B":(a,c,b),"BC_A":(b,c,a)}[fold]

def new_state(a,b,h,rep,tid,fold,r,cap,workers):
    return {
      "schema":"LIFE_CODE_EXP0003_N1_CHECKPOINT_A3_V1",
      "execution_amendment":"EXP-0003-A3","triad_id":tid,
      "representation":rep,"fold":fold,"replicate":int(r),"null":True,
      "input_sha256":{"A":frozen.sha(a),"B":frozen.sha(b),"H":frozen.sha(h)},
      "shard_bases":int(cap),"workers":int(workers),
      "ladder":None,"next_index":0,"detail":[],"complete":False,"Lstar":None
    }

def validate(s,a,b,h,rep,tid,fold,r,cap,workers):
    ok=(s.get("schema")=="LIFE_CODE_EXP0003_N1_CHECKPOINT_A3_V1" and
        s.get("execution_amendment")=="EXP-0003-A3" and
        s.get("triad_id")==tid and s.get("representation")==rep and
        s.get("fold")==fold and s.get("replicate")==int(r) and
        s.get("null") is True and
        s.get("input_sha256")=={"A":frozen.sha(a),"B":frozen.sha(b),"H":frozen.sha(h)} and
        int(s.get("shard_bases"))==int(cap) and int(s.get("workers"))==int(workers))
    if not ok: raise RuntimeError("checkpoint identity mismatch")
    return s

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--a",required=True); p.add_argument("--b",required=True); p.add_argument("--c",required=True)
    p.add_argument("--representation",required=True,choices=REPS)
    p.add_argument("--triad-id",required=True); p.add_argument("--fold",required=True,choices=FOLDS)
    p.add_argument("--replicate",type=int,required=True); p.add_argument("--state-in")
    p.add_argument("--work",required=True); p.add_argument("--out",required=True)
    p.add_argument("--workers",type=int,default=3); p.add_argument("--thresholds",type=int,default=1)
    p.add_argument("--shard-bases",type=int,default=frozen.DEFAULT_SHARD_BASES)
    x=p.parse_args()
    if not 0<=x.replicate<99: raise SystemExit("replicate must be 0..98")
    A,B,C=map(Path,(x.a,x.b,x.c)); a,b,h=fold_paths(A,B,C,x.fold)
    if x.state_in:
        s=validate(json.loads(Path(x.state_in).read_text()),a,b,h,x.representation,x.triad_id,x.fold,x.replicate,x.shard_bases,x.workers)
    else:
        s=new_state(a,b,h,x.representation,x.triad_id,x.fold,x.replicate,x.shard_bases,x.workers)
    s=core.advance(a,b,h,x.representation,x.triad_id,x.fold,x.replicate,x.work,s,x.shard_bases,x.workers,x.thresholds)
    here=Path(__file__).resolve().parent
    s["engine_sha256"]=frozen.sha(here/"exp0003_engine.py")
    s["frozen_prod_scorer_sha256"]=frozen.sha(here/"exp0003_triad_transfer_prod.py")
    s["a1_executor_sha256"]=frozen.sha(here/"exp0003_triad_transfer_a1.py")
    s["a3_core_sha256"]=frozen.sha(here/"exp0003_n1_checkpoint_core_a3.py")
    s["a3_executor_sha256"]=frozen.sha(Path(__file__))
    out=Path(x.out); out.parent.mkdir(parents=True,exist_ok=True)
    tmp=out.with_suffix(out.suffix+".partial")
    tmp.write_text(json.dumps(s,indent=2,sort_keys=True)+"\n"); tmp.replace(out)
    print(json.dumps({"status":"CHECKPOINT_WRITTEN","triad_id":x.triad_id,
      "representation":x.representation,"fold":x.fold,"replicate":x.replicate},sort_keys=True))

if __name__=="__main__": main()
