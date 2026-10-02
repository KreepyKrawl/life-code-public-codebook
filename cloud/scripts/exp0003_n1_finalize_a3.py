#!/usr/bin/env python3
from pathlib import Path
import argparse,json
import exp0003_triad_transfer_prod as frozen

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--state",required=True); p.add_argument("--out",required=True)
    x=p.parse_args()
    s=json.loads(Path(x.state).read_text())
    if s.get("schema")!="LIFE_CODE_EXP0003_N1_CHECKPOINT_A3_V1": raise SystemExit("bad checkpoint schema")
    if s.get("execution_amendment")!="EXP-0003-A3" or s.get("null") is not True: raise SystemExit("bad amendment/null state")
    if not s.get("complete") or s.get("Lstar") is None: raise SystemExit("checkpoint incomplete")
    if int(s.get("next_index",-1))!=len(s.get("detail",[])): raise SystemExit("checkpoint index mismatch")
    row={"replicate":s["replicate"],"Lstar":s["Lstar"],"detail":s["detail"]}
    here=Path(__file__).resolve().parent
    out={
      "schema":"LIFE_CODE_EXP0003_N1_SCORE_A3_V1","execution_amendment":"EXP-0003-A3",
      "triad_id":s["triad_id"],"representation":s["representation"],"fold":s["fold"],
      "replicate":s["replicate"],"null":True,"score":row,
      "input_sha256":s["input_sha256"],"engine_sha256":s["engine_sha256"],
      "frozen_prod_scorer_sha256":s["frozen_prod_scorer_sha256"],
      "a1_executor_sha256":s["a1_executor_sha256"],"a3_core_sha256":s["a3_core_sha256"],
      "a3_executor_sha256":s["a3_executor_sha256"],
      "checkpoint_sha256":frozen.sha(x.state),
      "finalizer_sha256":frozen.sha(Path(__file__)),"status":"COMPLETE"
    }
    q=Path(x.out); q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"FINALIZED","triad_id":out["triad_id"],
      "representation":out["representation"],"fold":out["fold"],"replicate":out["replicate"]},sort_keys=True))
if __name__=="__main__": main()
