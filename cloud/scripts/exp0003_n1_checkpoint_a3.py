#!/usr/bin/env python3
"""EXP-0003 A3 N1 threshold checkpoint wrapper."""
from pathlib import Path
import argparse, json
import exp0003_triad_transfer_prod as frozen
import exp0003_triad_transfer_a1 as a1

def fold_paths(a,b,c,fold):
    return {"AB_C":(a,b,c),"AC_B":(a,c,b),"BC_A":(b,c,a)}[fold]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--a",required=True)
    p.add_argument("--b",required=True)
    p.add_argument("--c",required=True)
    p.add_argument("--representation",required=True)
    p.add_argument("--triad-id",required=True)
    p.add_argument("--fold",required=True)
    p.add_argument("--replicate",type=int,required=True)
    p.add_argument("--state-in")
    p.add_argument("--work",required=True)
    p.add_argument("--out",required=True)
    x=p.parse_args()
    print(json.dumps({"status":"A3_WRAPPER_READY","replicate":x.replicate}))
if __name__=="__main__":
    main()
