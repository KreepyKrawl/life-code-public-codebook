#!/usr/bin/env python3
"""Exact EXP-0002 primary hierarchy score. No genomic sequence is read."""
from pathlib import Path
import csv, itertools, math, json, argparse, statistics

LADDERS=['Bacterial ladder','Fungal ladder','Plant ladder','Animal ladder']
METRICS=['MAX_K','LONGEST_BLOCK','ORDERED_TRANSFER']

def rank_avg(vals):
    n=len(vals); order=sorted(range(n), key=lambda i: vals[i])
    ranks=[0.0]*n; i=0
    while i<n:
        j=i+1
        while j<n and vals[order[j]]==vals[order[i]]: j+=1
        r=(i+1+j)/2.0
        for k in range(i,j): ranks[order[k]]=r
        i=j
    return ranks

def pearson(x,y):
    mx=sum(x)/len(x); my=sum(y)/len(y)
    dx=[a-mx for a in x]; dy=[b-my for b in y]
    den=math.sqrt(sum(a*a for a in dx)*sum(b*b for b in dy))
    if den==0: return 0.0
    return sum(a*b for a,b in zip(dx,dy))/den

def spearman(x,y): return pearson(rank_avg(x),rank_avg(y))

def load(path):
    rows=list(csv.DictReader(open(path)))
    data={}
    for r in rows:
        key=(r['ladder'],int(r['depth_ordinal']))
        data[key]={m:float(r[m]) for m in METRICS}
    missing=[(l,d) for l in LADDERS for d in (1,2,3) if (l,d) not in data]
    if missing: raise ValueError(f'missing strata: {missing}')
    return data

def evaluate(data, depth_perms=None):
    corrs={}; ladder_means={}; metric_means={}
    for li,l in enumerate(LADDERS):
        depths=list(depth_perms[li]) if depth_perms else [1,2,3]
        vals_by_m={m:[data[(l,d)][m] for d in (1,2,3)] for m in METRICS}
        for m in METRICS: corrs[(l,m)]=spearman(depths,vals_by_m[m])
        ladder_means[l]=statistics.mean(corrs[(l,m)] for m in METRICS)
    for m in METRICS: metric_means[m]=statistics.mean(corrs[(l,m)] for l in LADDERS)
    score=-statistics.mean(corrs.values())
    return score,corrs,ladder_means,metric_means

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input_csv'); ap.add_argument('--out',required=True); args=ap.parse_args()
    data=load(args.input_csv)
    observed,corrs,lmeans,mmeans=evaluate(data)
    perms=list(itertools.permutations([1,2,3]))
    dist=[]
    for pset in itertools.product(perms,repeat=4):
        s,*_=evaluate(data,pset); dist.append(s)
    ge=sum(s>=observed-1e-15 for s in dist)
    p=ge/len(dist)
    conditions={
      'permutation_p_lt_0.05':p<0.05,
      'at_least_3_of_4_ladders_negative':sum(v<0 for v in lmeans.values())>=3,
      'no_primary_metric_positive_mean':all(v<=0 for v in mmeans.values()),
    }
    out={
      'observed_hierarchy_score':observed,'exact_permutation_n':len(dist),'exact_one_sided_p':p,
      'ladder_metric_correlations':{f'{l}|{m}':v for (l,m),v in corrs.items()},
      'ladder_mean_correlations':lmeans,'metric_mean_correlations':mmeans,
      'support_conditions':conditions,'primary_support':all(conditions.values()),
      'permutation_scores':dist
    }
    Path(args.out).write_text(json.dumps(out,indent=2)); print(json.dumps({k:v for k,v in out.items() if k!='permutation_scores'},indent=2))
if __name__=='__main__': main()
