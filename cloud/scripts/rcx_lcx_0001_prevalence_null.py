#!/usr/bin/env python3
import json,random,statistics,bisect
from collections import defaultdict,Counter
from pathlib import Path
import rcx_lcx_0001_stage_a as S

N=1000
SEED=260922

def projected_occurrences(records,pmods,q):
    allowed={x for m in pmods for x in m};t=S.MAPS[q];byrec={}
    for rid,s in records:
        bs=s.translate(t);arr=[]
        for i in range(len(bs)-S.K+1):
            w=bs[i:i+S.K]
            if w in allowed:arr.append((i,w))
        byrec[rid]=arr
    return byrec

def relation_exists(pa,pb):
    if not pa or not pb:return False
    for x in pa:
        j=bisect.bisect_left(pb,x+S.MIN_D)
        if j<len(pb) and pb[j]-x<=S.MAX_D:return True
    return False

def rescue_fraction_from_assignments(pmods,byrec):
    pos=defaultdict(lambda:defaultdict(list))
    for rid,arr in byrec.items():
        for p,w in arr:pos[w][rid].append(p)
    hit=0
    for a,b in pmods:
        ok=False
        for rid in byrec:
            if relation_exists(pos[a].get(rid,()),pos[b].get(rid,())):
                ok=True;break
        hit+=int(ok)
    return hit/len(pmods),hit

def shuffled_assignments(real_byrec,rng):
    out={}
    for rid,arr in real_byrec.items():
        positions=[p for p,w in arr];labels=[w for p,w in arr]
        rng.shuffle(labels)
        out[rid]=list(zip(positions,labels))
    return out

def holm(pvals):
    ordered=sorted(pvals.items(),key=lambda kv:kv[1]);m=len(ordered);adj={};running=0.0
    for i,(k,p) in enumerate(ordered):
        v=min(1.0,(m-i)*p);running=max(running,v);adj[k]=running
    return adj

def main():
    work=Path('rcx-lcx-0001-null-work');work.mkdir(exist_ok=True)
    records={};manifest={}
    for label in ('ECOLI','PYRO','YEAST'):
        p,h=S.reacquire(label,work);records[label]=S.read_runs(p)
        manifest[label]={'accession':S.INPUTS[label][0],'raw_sha256':h,'analysis_runs':len(records[label]),'acgt_bases':S.bases(records[label])}
    folds={};pre={}
    for a,b,h in S.EXPECTED:
        shared=S.shared_words(records[a],records[b]);mods=S.module_set(records[a],shared)&S.module_set(records[b],shared)
        got={'shared':len(shared),'modules':len(mods)};exp=S.EXPECTED[(a,b,h)]
        pre[f'{a}+{b}->{h}']={'got':got,'expected':exp,'pass':got==exp}
        folds[(a,b,h)]=mods
    if not all(x['pass'] for x in pre.values()):
        raise SystemExit('BASELINE_MISMATCH: prevalence null forbidden')

    rng=random.Random(SEED);rows=[];null_by_map=defaultdict(lambda:[[] for _ in range(3)])
    fold_order=list(folds)
    for fi,(a,b,h) in enumerate(fold_order):
        mods=folds[(a,b,h)]
        for q in ('RY','MK','WS'):
            pmods={(S.project_word(x,q),S.project_word(y,q)) for x,y in mods}
            real_occ=projected_occurrences(records[h],pmods,q)
            real_frac,real_hit=rescue_fraction_from_assignments(pmods,real_occ)
            null=[]
            for rep in range(N):
                sh=shuffled_assignments(real_occ,rng)
                f,_=rescue_fraction_from_assignments(pmods,sh);null.append(f)
                null_by_map[q][fi].append(f)
            med=statistics.median(null)
            p=(1+sum(x>=real_frac for x in null))/(N+1)
            row={
              'fold':f'{a}+{b}->{h}','quotient':q,'unique_projected_modules':len(pmods),
              'real_unique_rescue_fraction':real_frac,'real_unique_rescued':real_hit,
              'null_n':N,'null_median':med,'null_mean':statistics.mean(null),
              'delta_vs_null_median':real_frac-med,'empirical_p':p,
              'null_p90':sorted(null)[int(.9*(N-1))],'null_p99':sorted(null)[int(.99*(N-1))],
              'matched_null':'within-record label permutation over exact observed relevant projected-kmer positions; preserves per-record primitive counts, relevant-position density, record boundaries, k, direction and window'
            }
            rows.append(row);print(json.dumps(row,sort_keys=True))

    combined={};rawp={}
    for q in ('RY','MK','WS'):
        rs=[r for r in rows if r['quotient']==q]
        real_stat=statistics.median(r['real_unique_rescue_fraction'] for r in rs)
        null_stats=[]
        for i in range(N):
            null_stats.append(statistics.median(null_by_map[q][fi][i] for fi in range(3)))
        p=(1+sum(x>=real_stat for x in null_stats))/(N+1);rawp[q]=p
        combined[q]={
          'real_cross_fold_median':real_stat,'null_cross_fold_median':statistics.median(null_stats),
          'delta':real_stat-statistics.median(null_stats),'folds_positive_delta':sum(r['delta_vs_null_median']>0 for r in rs),
          'combined_empirical_p':p
        }
    hadj=holm(rawp)
    for q in combined:combined[q]['holm_adjusted_p']=hadj[q]
    out={
      'experiment':'RCX-LCX-0001','stage':'A_PREVALENCE_MATCHED_NULL','status':'COMPLETE',
      'seed':SEED,'null_n':N,'inputs':manifest,'precheck':pre,'fold_results':rows,'combined':combined,
      'interpretation_ceiling':'This Stage-A null tests whether quotient rescue exceeds prevalence/spatial-opportunity effects in the original three-domain calibration. It does not satisfy the full >=3-of-4 lineage-ladder primary gate.'
    }
    Path('rcx-lcx-0001-prevalence-null.json').write_text(json.dumps(out,indent=2))
    Path('rcx-lcx-0001-prevalence-null-sha256.txt').write_text(f"{S.sha256(Path('rcx-lcx-0001-prevalence-null.json'))}  rcx-lcx-0001-prevalence-null.json\n")
    print('COMBINED',json.dumps(combined,sort_keys=True))
if __name__=='__main__':main()
