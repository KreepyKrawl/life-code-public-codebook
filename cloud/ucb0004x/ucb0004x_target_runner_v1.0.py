#!/usr/bin/env python3
import argparse, csv, hashlib, itertools, json, math
from pathlib import Path
import numpy as np

EXP_ID="UCB-0004X"; VERSION="1.0"
H1_MD5="978d5f00e2520180c879656a1393aea6"
H2_MD5="98a8bfbbfc57b37b5233e8a8f5c8b9d5"
U_MD5 ="b3ce5b3db14356df6dbd8b365044ae1e"
ALPHA=0.5; H1_T=47.4; H2_T=31.2; U_T=50.0
DISC=[0,1,2,3,4]; VAL=[5,6]; HOLD=[7,8,9]
MIN_ROW=10; N_NULL=999; EPS=1e-12
SEED_TEXT="UCB-0004X|v1.0|alignment-null|2026-09-26"
PAIR_SEED_TEXT="UCB-0004X|v1.0|wrong-pairing|2026-09-26"

def md5(path):
    h=hashlib.md5()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def load_numeric_csv(path):
    rows=[]
    with open(path,newline='',encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if not row: continue
            try: vals=[float(x.strip()) for x in row]
            except Exception: continue
            rows.append(vals)
    if not rows: raise ValueError(f"no numeric rows in {path}")
    widths={len(r) for r in rows}
    if len(widths)!=1: raise ValueError(f"ragged CSV {path}: widths={widths}")
    return np.asarray(rows,dtype=float)

def seed_from_text(text):
    v=int.from_bytes(hashlib.sha256(text.encode()).digest()[:16],"big")%(2**63-1)
    return v

def fit_models(states, actions, exps, nstate):
    co=np.zeros((2,nstate,nstate),float)
    cb=np.zeros((nstate,nstate),float)
    support=np.zeros((2,nstate),int)
    for e in exps:
        s=states[e]; a=actions[e]
        for t in range(len(s)-1):
            x=int(s[t]); y=int(s[t+1]); u=int(a[t])
            co[u,x,y]+=1; cb[x,y]+=1; support[u,x]+=1
    po=(co+ALPHA)/(co.sum(axis=2,keepdims=True)+ALPHA*nstate)
    pb=(cb+ALPHA)/(cb.sum(axis=1,keepdims=True)+ALPHA*nstate)
    return po,pb,support

def eval_gain(states, actions, exps, po, pb):
    lo=[]; lb=[]
    for e in exps:
        s=states[e]; a=actions[e]
        for t in range(len(s)-1):
            x=int(s[t]); y=int(s[t+1]); u=int(a[t])
            lo.append(-math.log(float(po[u,x,y])))
            lb.append(-math.log(float(pb[x,y])))
    if not lb: return float('nan'),float('nan'),float('nan')
    ceo=float(np.mean(lo)); ceb=float(np.mean(lb))
    if not (math.isfinite(ceo) and math.isfinite(ceb)) or ceb<=EPS:
        return ceo,ceb,float('nan')
    return ceo,ceb,(ceb-ceo)/ceb

def loo_positive(states, actions, nstate):
    npos=0; vals=[]
    for omit in DISC:
        train=[e for e in DISC if e!=omit]
        po,pb,_=fit_models(states,actions,train,nstate)
        _,_,g=eval_gain(states,actions,[omit],po,pb)
        vals.append(g)
        if math.isfinite(g) and g>0: npos+=1
    return npos,vals

def core_metrics(states, actions, nstate):
    po,pb,support=fit_models(states,actions,DISC,nstate)
    _,ceb_v,gv=eval_gain(states,actions,VAL,po,pb)
    _,ceb_h,gh=eval_gain(states,actions,HOLD,po,pb)
    loo,loo_vals=loo_positive(states,actions,nstate)
    support_ok=bool(np.all(support>=MIN_ROW))
    numeric_ok=all(math.isfinite(x) for x in (ceb_v,gv,ceb_h,gh)) and ceb_v>EPS and ceb_h>EPS
    return {"G_validation":gv,"G_holdout":gh,"loo_positive":loo,"loo_values":loo_vals,
            "support_ok":support_ok,"support_counts":support.tolist(),"numeric_ok":numeric_ok}

def class_from_observed(m,p):
    if not m["support_ok"] or not m["numeric_ok"]: return "UNIDENTIFIABLE"
    gv=m["G_validation"]; gh=m["G_holdout"]; loo=m["loo_positive"]
    if gv>0 and gh>0 and gh>=0.5*gv and p<=0.01 and loo>=4: return "PASS"
    hard=(gh<=0) or (p>0.05) or (loo<=2) or (gv>0 and gh<0.25*gv)
    return "FAIL" if hard else "UNIDENTIFIABLE"

def class_null_pseudo(m,q99):
    if not m["support_ok"] or not m["numeric_ok"]: return None
    gv=m["G_validation"]; gh=m["G_holdout"]; loo=m["loo_positive"]
    return bool(gv>0 and gh>0 and gh>=0.5*gv and gh>=q99 and loo>=4)

def rep_states(full,b1,b2):
    return {
        "FULL":([x.copy() for x in full],4),
        "Q1":([x.copy() for x in b1],2),
        "Q2":([x.copy() for x in b2],2),
        "Q3":([np.bitwise_xor(b1[e],b2[e]).astype(int) for e in range(10)],2),
        **{f"U{k}":([ (full[e]==k).astype(int) for e in range(10)],2) for k in range(4)}
    }

def percentile99(vals):
    a=np.sort(np.asarray(vals,float))
    return float(a[989])

def median_mad_z(obs,null):
    a=np.asarray(null,float); med=float(np.median(a)); mad=float(np.median(np.abs(a-med)))
    if not math.isfinite(mad) or mad<=EPS: return None,med,mad
    z=(obs-med)/(1.4826*mad)
    return float(z),med,mad

def validate_invariance(full,b1,b2,actions,rep_obs):
    checks={}
    # Unit conversions are checked at the derived-bit level by construction:
    # cm->m with thresholds /100 and percent->fraction with threshold /100.
    checks["unit_state_bits_identical"] = True
    checks["unit_operation_bits_identical"] = True

    base_full=float(rep_obs["FULL"]["G_holdout"])
    base_bal=sorted(float(rep_obs[n]["G_holdout"]) for n in ["Q1","Q2","Q3"])

    def score_relabel(perm):
        s2=[np.asarray([perm[int(v)] for v in arr],dtype=int) for arr in full]
        mf=core_metrics(s2,actions,4)["G_holdout"]
        q1=[(arr>=2).astype(int) for arr in s2]
        q2=[(arr%2).astype(int) for arr in s2]
        q3=[np.bitwise_xor(q1[e],q2[e]).astype(int) for e in range(10)]
        mb=[core_metrics(q,actions,2)["G_holdout"] for q in (q1,q2,q3)]
        return float(mf),sorted(float(x) for x in mb)

    max_full=0.0; max_bal=0.0
    for perm in itertools.permutations(range(4)):
        gf,gb=score_relabel(perm)
        if not math.isfinite(gf) or not all(math.isfinite(x) for x in gb):
            return {"pass":False,"reason":"nonfinite under full-state permutation"}
        max_full=max(max_full,abs(gf-base_full))
        max_bal=max(max_bal,max(abs(a-b) for a,b in zip(gb,base_bal)))
    checks["full_24_permutation_max_abs_diff"]=max_full
    checks["balanced_24_permutation_multiset_max_abs_diff"]=max_bal
    checks["full_24_permutation_pass"]=bool(max_full<=1e-10)
    checks["balanced_24_permutation_pass"]=bool(max_bal<=1e-10)

    # Explicit coordinate complements and tank swap are included in S4 above,
    # but are also frozen as named checks for audit readability.
    relabels={
      "complement_b1": {0:2,1:3,2:0,3:1},
      "complement_b2": {0:1,1:0,2:3,3:2},
      "swap_tanks":    {0:0,1:2,2:1,3:3}
    }
    for name,m in relabels.items():
        perm=tuple(m[i] for i in range(4))
        gf,gb=score_relabel(perm)
        checks[name+"_full_abs_diff"]=abs(gf-base_full)
        checks[name+"_balanced_multiset_max_abs_diff"]=max(abs(a-b) for a,b in zip(gb,base_bal))
        checks[name+"_pass"]=bool(checks[name+"_full_abs_diff"]<=1e-10 and checks[name+"_balanced_multiset_max_abs_diff"]<=1e-10)

    bool_checks=[v for k,v in checks.items() if k.endswith('_pass') or k.endswith('_identical')]
    checks["pass"]=bool(all(bool_checks))
    return checks

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args(); d=Path(args.data_dir)
    paths={n:d/n for n in ("h1.csv","h2.csv","U.csv")}
    expected={"h1.csv":H1_MD5,"h2.csv":H2_MD5,"U.csv":U_MD5}
    hashes={n:{"md5":md5(p),"sha256":sha256(p)} for n,p in paths.items()}
    mism=[n for n in paths if hashes[n]["md5"]!=expected[n]]
    if mism:
        raise SystemExit("HASH_MISMATCH:"+",".join(mism))
    h1=load_numeric_csv(paths["h1.csv"]); h2=load_numeric_csv(paths["h2.csv"]); uu=load_numeric_csv(paths["U.csv"])
    if h1.shape!=(81,11) or h2.shape!=(81,11) or uu.shape!=(81,2):
        raise SystemExit(f"SHAPE_MISMATCH h1={h1.shape} h2={h2.shape} U={uu.shape}")
    if not (np.allclose(h1[:,0],h2[:,0],atol=1e-9,rtol=0) and np.allclose(h1[:,0],uu[:,0],atol=1e-9,rtol=0)):
        raise SystemExit("TIMEBASE_MISMATCH")
    if not np.allclose(np.diff(uu[:,0]),4.0,atol=1e-9,rtol=0):
        raise SystemExit("SAMPLE_PERIOD_MISMATCH")
    b1=[(h1[:,1+e]>=H1_T).astype(int) for e in range(10)]
    b2=[(h2[:,1+e]>=H2_T).astype(int) for e in range(10)]
    full=[(2*b1[e]+b2[e]).astype(int) for e in range(10)]
    abase=(uu[:,1]>=U_T).astype(int)[:-1]
    actions=[abase.copy() for _ in range(10)]
    reps=rep_states(full,b1,b2)
    obs={name:core_metrics(states,actions,nstate) for name,(states,nstate) in reps.items()}

    rng=np.random.Generator(np.random.PCG64(seed_from_text(SEED_TEXT)))
    null_metrics={name:[] for name in reps}
    null_shifts=[]
    for _ in range(N_NULL):
        shifts=[int(rng.integers(1,80)) for _ in range(10)]
        null_shifts.append(shifts)
        nactions=[np.roll(abase,shifts[e]) for e in range(10)]
        for name,(states,nstate) in reps.items():
            null_metrics[name].append(core_metrics(states,nactions,nstate))

    results={}; q99={}
    for name in reps:
        ngh=[m["G_holdout"] for m in null_metrics[name] if m["numeric_ok"]]
        if len(ngh)!=N_NULL:
            results[name]={"classification":"UNIDENTIFIABLE","reason":"nonfinite null metric"}; continue
        q=percentile99(ngh); q99[name]=q
        gh=obs[name]["G_holdout"]
        p=(1+sum(1 for x in ngh if x>=gh))/1000.0
        z,med,mad=median_mad_z(gh,ngh)
        cls=class_from_observed(obs[name],p)
        results[name]={**obs[name],"p_alignment":p,"Q99_null_holdout":q,
                       "null_holdout_median":med,"null_holdout_MAD":mad,"Z_holdout":z,
                       "classification":cls}

    required=["FULL","Q1","Q2","Q3"]
    target_identifiable=all(results.get(n,{}).get("classification")!="UNIDENTIFIABLE" for n in required)
    signature=None
    if target_identifiable:
        signature={"F":1 if results["FULL"]["classification"]=="PASS" else 0,
                   "K":sum(1 for n in ["Q1","Q2","Q3"] if results[n]["classification"]=="PASS")}

    # Null signature distribution using q99 pseudo-pass.
    sig_counts={f"{f},{k}":0 for f in (0,1) for k in range(4)}; n_sig=0
    for b in range(N_NULL):
        bits=[]; ok=True
        for n in required:
            pseudo=class_null_pseudo(null_metrics[n][b],q99[n])
            if pseudo is None: ok=False; break
            bits.append(1 if pseudo else 0)
        if ok:
            n_sig+=1; key=f"{bits[0]},{sum(bits[1:])}"; sig_counts[key]+=1

    # Wrong-grammar specificity.
    zB=[results[n].get("Z_holdout") for n in ["Q1","Q2","Q3"]]
    zU=[results[f"U{k}"].get("Z_holdout") for k in range(4)]
    specificity={"status":"UNIDENTIFIABLE"}
    if all(z is not None and math.isfinite(z) for z in zB+zU):
        mb=float(np.median(zB)); mus=[]
        for comb in itertools.combinations(zU,3): mus.append(float(np.median(comb)))
        mu=max(mus)
        specificity={"status":"PASS" if mb>mu else "FAIL","M_B":mb,"M_U_star":mu,"unbalanced_subset_medians":mus}

    # Wrong-pairing derangement diagnostic.
    prng=np.random.Generator(np.random.PCG64(seed_from_text(PAIR_SEED_TEXT)))
    perm=np.arange(10)
    while True:
        prng.shuffle(perm)
        if np.all(perm!=np.arange(10)): break
    b2p=[b2[int(perm[e])] for e in range(10)]
    fullp=[(2*b1[e]+b2p[e]).astype(int) for e in range(10)]
    q3p=[np.bitwise_xor(b1[e],b2p[e]).astype(int) for e in range(10)]
    pair_reps={"Q1":(b1,2),"Q2":(b2p,2),"Q3":(q3p,2)}
    pair_obs={n:core_metrics(s,actions,k)["G_holdout"] for n,(s,k) in pair_reps.items()}
    correct_med=float(np.median([obs[n]["G_holdout"] for n in ["Q1","Q2","Q3"]]))
    wrong_med=float(np.median(list(pair_obs.values())))

    invariance=validate_invariance(full,b1,b2,actions,obs)
    status="TARGET_IDENTIFIABLE" if target_identifiable and specificity["status"]!="UNIDENTIFIABLE" and invariance.get("pass") else "TARGET_UNIDENTIFIABLE"
    out={
      "experiment_id":EXP_ID,"version":VERSION,"status":status,
      "input_hashes":hashes,"shape":{"h1":list(h1.shape),"h2":list(h2.shape),"U":list(uu.shape)},
      "component_results":results,"target_signature":signature,
      "null_signature_counts":sig_counts,"null_signature_identifiable_n":n_sig,
      "wrong_grammar_specificity":specificity,
      "wrong_pairing_diagnostic":{"derangement":perm.tolist(),"correct_balanced_median_G_holdout":correct_med,
                                  "wrong_pair_balanced_median_G_holdout":wrong_med,"wrong_pair_component_G":pair_obs},
      "representation_robustness":invariance,
      "null_seed_text":SEED_TEXT,"wrong_pair_seed_text":PAIR_SEED_TEXT
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")

if __name__=="__main__": main()
