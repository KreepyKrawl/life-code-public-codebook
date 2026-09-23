#!/usr/bin/env python3
"""Synthetic, outcome-blind qualification of the complete EXP-0003 triadic scorer."""
from pathlib import Path
import json,tempfile
import exp0003_engine as e
import exp0003_transfer as o
import exp0003_triad_transfer as t

REPS=['ACGT','RY','MK','WS',*e.CONTROL_TUPLES.keys()]
MIN_LEN=4

# Synthetic design contains:
# - a longer A/B training-only decoy;
# - a shorter three-way transferable block;
# - held-out occurrence supplied in reverse-complement raw orientation;
# - multiple records, including a boundary trap that must never be joined.
TARGET='ACGTTGCAAGTCCGAT'
DECOY='GATTACCGTACGATTCGGAACCTA'
BOUND_LEFT='TTTTACGA'
BOUND_RIGHT='CGTAAAAA'

A=[
 ('A1','AACCGGTT'+DECOY+'TTAACCGG'+TARGET+'GGCCAATT'),
 ('A2',BOUND_LEFT),
 ('A3',BOUND_RIGHT),
]
B=[
 ('B1','CCGGAATT'+DECOY+'AACCTTGG'+o.reverse_complement(TARGET)+'TTGGAACC'),
 ('B2',BOUND_LEFT),
 ('B3',BOUND_RIGHT),
]
C=[
 ('C1','GGTTCCAA'+o.reverse_complement(TARGET)+'AACCGGTT'),
 ('C2','GGGG'+BOUND_LEFT),
 ('C3',BOUND_RIGHT+'CCCC'),
]


def write_fa(path,rows):
    with open(path,'w',encoding='ascii',newline='\n') as f:
        for n,s in rows:f.write(f'>{n}\n{s}\n')


def oriented_projected(rows,rep):
    fwd=[(n,e.project_sequence(s,rep)) for n,s in rows]
    rev=[(n,e.project_sequence(o.reverse_complement(s),rep)) for n,s in rows]
    return fwd,rev


def brute_maximal_candidates(Arows,Brows,rep,min_len):
    af,_=oriented_projected(Arows,rep)
    bf,br=oriented_projected(Brows,rep)
    out=set()
    for _,a in af:
        for _,b in bf+br:
            for i,ca in enumerate(a):
                for j,cb in enumerate(b):
                    if ca!=cb:continue
                    # only start a maximal run once; if both have matching left
                    # context, this cell belongs to an earlier maximal match.
                    if i>0 and j>0 and a[i-1]==b[j-1]:continue
                    k=0
                    while i+k<len(a) and j+k<len(b) and a[i+k]==b[j+k]:k+=1
                    if k>=min_len:out.add(a[i:i+k])
    return out


def brute_fold(Arows,Brows,Hrows,rep,min_len):
    cand=brute_maximal_candidates(Arows,Brows,rep,min_len)
    hf,hr=oriented_projected(Hrows,rep)
    hs=[s for _,s in hf+hr]
    best=max([len(c) for c in cand if any(c in h for h in hs)] or [0])
    return best,len(cand),max([len(c) for c in cand] or [0])


def main():
    checks={}; detail={}
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        fa=td/'A.fa';fb=td/'B.fa';fc=td/'C.fa'
        write_fa(fa,A);write_fa(fb,B);write_fa(fc,C)
        specs=[('AB_C',A,B,C,fa,fb,fc),('AC_B',A,C,B,fa,fc,fb),('BC_A',B,C,A,fb,fc,fa)]
        for rep in REPS:
            detail[rep]={}
            for fold,ar,br,hr,ap,bp,hp in specs:
                oracle,ncand,trainmax=brute_fold(ar,br,hr,rep,MIN_LEN)
                vendor,vdet=t.fold_score(ap,bp,hp,rep,MIN_LEN,td/f'{rep}-{fold}')
                ok=(vendor==oracle)
                checks[f'{rep}_{fold}_vendor_equals_independent_triad_oracle']=ok
                if not ok:
                    raise SystemExit(f'{rep} {fold} mismatch vendor={vendor} oracle={oracle}')
                detail[rep][fold]={
                    'vendor_Lstar':vendor,
                    'oracle_Lstar':oracle,
                    'oracle_training_candidate_count':ncand,
                    'oracle_training_max':trainmax,
                    'vendor_training_candidate_count':vdet['training_candidate_count'],
                }
        # ACGT AB_C specifically proves the scorer does not report the longer
        # training-only decoy as transferred.
        q=detail['ACGT']['AB_C']
        checks['ACGT_training_max_exceeds_transferred_Lstar']=(q['oracle_training_max']>q['oracle_Lstar']>0)
        if not checks['ACGT_training_max_exceeds_transferred_Lstar']:
            raise SystemExit(f'decoy transfer trap not exercised: {q}')
        # Confirm record boundaries matter in the fixture: the synthetic joined
        # boundary word is not itself a legal source record substring.
        boundary_word=BOUND_LEFT[-4:]+BOUND_RIGHT[:4]
        checks['boundary_trap_not_within_any_source_record']=all(boundary_word not in s for rows in (A,B,C) for _,s in rows)
        if not checks['boundary_trap_not_within_any_source_record']:
            raise SystemExit('boundary trap fixture invalid')
    payload={
      'schema':'LIFE_CODE_EXP0003_FULL_TRIAD_TRANSFER_QUALIFICATION_V1',
      'status':'PASS',
      'synthetic_only':True,
      'exp0003_primary_outcomes_inspected':False,
      'representations_tested':REPS,
      'folds':['AB_C','AC_B','BC_A'],
      'minimum_match_length_for_fixture':MIN_LEN,
      'checks':checks,
      'detail':detail,
    }
    Path('exp0003-triad-transfer-qualification.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','representations':len(REPS),'fold_cells':len(REPS)*3,'checks':len(checks)},sort_keys=True))

if __name__=='__main__':main()
