#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
import exp0003_engine as e
import exp0003_triad_transfer_prod as prod

CHUNKS={
 'OBS':None,
 'N1_00_24':range(0,25),
 'N1_25_49':range(25,50),
 'N1_50_74':range(50,75),
 'N1_75_98':range(75,99),
}
REPS=['ACGT','RY','MK','WS',*e.CONTROL_TUPLES.keys()]
FOLDS=('AB_C','AC_B','BC_A')

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def fold_paths(a,b,c,fold):
    if fold=='AB_C':return a,b,c
    if fold=='AC_B':return a,c,b
    if fold=='BC_A':return b,c,a
    raise ValueError(fold)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--a',required=True);ap.add_argument('--b',required=True);ap.add_argument('--c',required=True)
    ap.add_argument('--representation',required=True,choices=REPS)
    ap.add_argument('--triad-id',required=True);ap.add_argument('--fold',required=True,choices=FOLDS)
    ap.add_argument('--chunk',required=True,choices=CHUNKS)
    ap.add_argument('--work',required=True);ap.add_argument('--out',required=True)
    ap.add_argument('--shard-bases',type=int,default=prod.DEFAULT_SHARD_BASES)
    x=ap.parse_args()
    A,B,C=map(Path,(x.a,x.b,x.c));ta,tb,th=fold_paths(A,B,C,x.fold)
    reps=[None] if CHUNKS[x.chunk] is None else list(CHUNKS[x.chunk])
    rows=[]
    root=Path(x.work);root.mkdir(parents=True,exist_ok=True)
    for r in reps:
        w=root/('OBS' if r is None else f'N1_{r:02d}')
        val,detail=prod.score_fold(ta,tb,th,x.representation,x.triad_id,x.fold,r,w,x.shard_bases)
        rows.append({'replicate':r,'Lstar':val,'detail':detail})
    payload={
      'schema':'LIFE_CODE_EXP0003_PRIMARY_CHUNK_V1',
      'triad_id':x.triad_id,'representation':x.representation,'fold':x.fold,'chunk':x.chunk,
      'replicate_ids':[r['replicate'] for r in rows],
      'scores':rows,
      'input_sha256':{'A':sha256(A),'B':sha256(B),'C':sha256(C)},
      'engine_sha256':sha256(Path(__file__).with_name('exp0003_engine.py')),
      'prod_scorer_sha256':sha256(Path(__file__).with_name('exp0003_triad_transfer_prod.py')),
      'status':'COMPLETE'
    }
    Path(x.out).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'COMPLETE','triad_id':x.triad_id,'representation':x.representation,'fold':x.fold,'chunk':x.chunk,'n_scores':len(rows)},sort_keys=True))
if __name__=='__main__':main()
