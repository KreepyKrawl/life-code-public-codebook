#!/usr/bin/env python3
"""Enforce the EXP-0002 sealed-result barrier before primary scoring."""
from pathlib import Path
import argparse,csv,subprocess,sys,json,hashlib

EXPECTED=[
 ("Bacterial ladder",1,"B1"),("Bacterial ladder",2,"B2"),("Bacterial ladder",3,"B3"),
 ("Fungal ladder",1,"F1"),("Fungal ladder",2,"F2"),("Fungal ladder",3,"F3"),
 ("Plant ladder",1,"P1"),("Plant ladder",2,"P2"),("Plant ladder",3,"P3"),
 ("Animal ladder",1,"A1"),("Animal ladder",2,"A2"),("Animal ladder",3,"A3"),
]
METRICS=["MAX_K","LONGEST_BLOCK","ORDERED_TRANSFER"]

def validate(path):
    rows=list(csv.DictReader(open(path,encoding="utf-8")))
    idx={(r["ladder"],int(r["depth_ordinal"]),r["triad_id"]):r for r in rows}
    errs=[]
    if len(rows)!=12: errs.append(f"expected exactly 12 rows, found {len(rows)}")
    for key in EXPECTED:
        r=idx.get(key)
        if r is None:
            errs.append(f"missing frozen stratum {key}")
            continue
        for m in METRICS:
            v=r.get(m,"").strip()
            if v=="":
                errs.append(f"{key[2]}: {m} blank")
                continue
            try: float(v)
            except: errs.append(f"{key[2]}: {m} not numeric: {v!r}")
    extras=set(idx)-set(EXPECTED)
    if extras: errs.append(f"unexpected strata: {sorted(extras)}")
    return errs

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results",required=True)
    ap.add_argument("--score-out")
    ap.add_argument("--check-only",action="store_true")
    args=ap.parse_args()
    errs=validate(args.results)
    if errs:
        print("EXP-0002 RESULT ENVELOPE: SEALED / INCOMPLETE")
        for e in errs: print(" -",e)
        sys.exit(2)
    print("EXP-0002 RESULT ENVELOPE: SEALED_READY")
    if args.check_only: return
    if not args.score_out: raise SystemExit("--score-out required unless --check-only")
    score=Path(__file__).with_name("exp0002_hierarchy_score.py")
    subprocess.run([sys.executable,str(score),args.results,"--out",args.score_out],check=True)

if __name__=="__main__": main()
