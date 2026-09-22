#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

MAPS = {
    "ACGT": {"A":"A","C":"C","G":"G","T":"T"},
    "RY":   {"A":"R","G":"R","C":"Y","T":"Y"},
    "MK":   {"A":"M","C":"M","G":"K","T":"K"},
    "WS":   {"A":"W","T":"W","C":"S","G":"S"},
}

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def project(inp,out,rep):
    m=MAPS[rep]
    with open(inp,"rt",encoding="ascii") as src, open(out,"wt",encoding="ascii",newline="\n") as dst:
        for raw in src:
            if raw.startswith(">"):
                dst.write(raw.rstrip("\r\n")+"\n")
                continue
            s=raw.strip().upper()
            if not s:
                continue
            bad=set(s)-set("ACGT")
            if bad:
                raise SystemExit(f"non-ACGT symbol(s) in normalized input: {sorted(bad)}")
            dst.write("".join(m[c] for c in s)+"\n")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--representation",choices=MAPS,required=True)
    ap.add_argument("--expected-input-sha256")
    a=ap.parse_args()
    inp,out=Path(a.input),Path(a.output)
    observed=sha256(inp)
    if a.expected_input_sha256 and observed!=a.expected_input_sha256:
        raise SystemExit(f"input SHA mismatch: {observed}")
    out.parent.mkdir(parents=True,exist_ok=True)
    project(inp,out,a.representation)
    result={
        "schema":"LIFE_CODE_PROJECTION_RESULT_V1",
        "representation":a.representation,
        "input":str(inp),
        "input_sha256":observed,
        "output":str(out),
        "output_sha256":sha256(out),
        "mapping":MAPS[a.representation],
    }
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__": main()
