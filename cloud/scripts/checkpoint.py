#!/usr/bin/env python3
import argparse, hashlib, json, os, time
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def atomic_json(path,obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".partial")
    tmp.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(tmp,path)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--experiment",required=True)
    ap.add_argument("--chunk",required=True)
    ap.add_argument("--status",choices=["QUEUED","RUNNING","COMPLETE","FAILED"],required=True)
    ap.add_argument("--output",action="append",default=[])
    ap.add_argument("--checkpoint",required=True)
    ap.add_argument("--note")
    a=ap.parse_args()
    outs=[]
    for p in a.output:
        q=Path(p)
        if not q.exists(): raise SystemExit(f"missing output: {q}")
        outs.append({"path":str(q),"bytes":q.stat().st_size,"sha256":sha256(q)})
    obj={
      "schema":"LIFE_CODE_CHUNK_CHECKPOINT_V1",
      "experiment":a.experiment,
      "chunk":a.chunk,
      "status":a.status,
      "unix_time":int(time.time()),
      "outputs":outs,
      "note":a.note,
    }
    atomic_json(a.checkpoint,obj)
    print(json.dumps(obj,sort_keys=True))
if __name__=="__main__": main()
