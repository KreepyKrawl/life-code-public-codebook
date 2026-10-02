#!/usr/bin/env python3
from pathlib import Path
import argparse,json

GROUPS={
 "N1_00_24":list(range(0,25)),
 "N1_25_49":list(range(25,50)),
 "N1_50_74":list(range(50,75)),
 "N1_75_98":list(range(75,99)),
}

def same(vals,label):
    vals=list(vals)
    if not vals: raise RuntimeError("missing "+label)
    if any(v!=vals[0] for v in vals[1:]): raise RuntimeError("inconsistent "+label)
    return vals[0]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input-dir",required=True)
    p.add_argument("--group",required=True,choices=GROUPS)
    p.add_argument("--triad-id",required=True)
    p.add_argument("--representation",required=True)
    p.add_argument("--fold",required=True)
    p.add_argument("--out",required=True)
    x=p.parse_args()

    objs=[]
    for f in sorted(Path(x.input_dir).rglob("*.json")):
        o=json.loads(f.read_text())
        if o.get("schema")!="LIFE_CODE_EXP0003_N1_SCORE_A3_V1": continue
        if o.get("triad_id")==x.triad_id and o.get("representation")==x.representation and o.get("fold")==x.fold:
            objs.append(o)
    expected=GROUPS[x.group]
    got=sorted(int(o["replicate"]) for o in objs)
    if got!=expected: raise RuntimeError(f"replicate coverage mismatch got={got} expected={expected}")
    rows=[o["score"] for o in sorted(objs,key=lambda z:int(z["replicate"]))]
    out={
      "schema":"LIFE_CODE_EXP0003_PRIMARY_CHUNK_V1","execution_amendment":"EXP-0003-A3",
      "triad_id":x.triad_id,"representation":x.representation,"fold":x.fold,"chunk":x.group,
      "replicate_ids":[r["replicate"] for r in rows],"scores":rows,
      "input_sha256":same((o["input_sha256"] for o in objs),"input_sha256"),
      "engine_sha256":same((o["engine_sha256"] for o in objs),"engine_sha256"),
      "prod_scorer_sha256":same((o["frozen_prod_scorer_sha256"] for o in objs),"prod_scorer_sha256"),
      "a1_executor_sha256":same((o["a1_executor_sha256"] for o in objs),"a1_executor_sha256"),
      "a3_core_sha256":same((o["a3_core_sha256"] for o in objs),"a3_core_sha256"),
      "a3_executor_sha256":same((o["a3_executor_sha256"] for o in objs),"a3_executor_sha256"),
      "finalizer_sha256":same((o["finalizer_sha256"] for o in objs),"finalizer_sha256"),
      "status":"COMPLETE"
    }
    q=Path(x.out); q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"COMPLETE","triad_id":x.triad_id,
      "representation":x.representation,"fold":x.fold,"group":x.group,
      "n_scores":len(rows)},sort_keys=True))
if __name__=="__main__": main()
