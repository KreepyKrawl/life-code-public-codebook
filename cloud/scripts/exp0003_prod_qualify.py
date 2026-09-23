#!/usr/bin/env python3
import hashlib,json,tempfile
from pathlib import Path
import exp0003_engine as e
import exp0003_triad_transfer as simple
import exp0003_triad_transfer_qualify as q
import exp0003_triad_transfer_prod as prod

REPS=q.REPS


def first64(s):return int(hashlib.sha256(s.encode('utf-8')).hexdigest()[:16],16)

def parse_one(path):return list(e.iter_fasta(path))

def main():
    checks={};detail={}
    with tempfile.TemporaryDirectory() as td:
        td=Path(td);fa=td/'A.fa';fb=td/'B.fa';fc=td/'C.fa'
        q.write_fa(fa,q.A);q.write_fa(fb,q.B);q.write_fa(fc,q.C)
        specs=[('AB_C',q.A,q.B,q.C,fa,fb,fc),('AC_B',q.A,q.C,q.B,fa,fc,fb),('BC_A',q.B,q.C,q.A,fb,fc,fa)]
        for rep in REPS:
            detail[rep]={}
            for fold,ar,br,hr,ap,bp,hp in specs:
                oracle,_,_=q.brute_fold(ar,br,hr,rep,q.MIN_LEN)
                sv,_=simple.fold_score(ap,bp,hp,rep,q.MIN_LEN,td/f'simple-{rep}-{fold}')
                # Production threshold ladder bottoms at 8, so this fixture is
                # constructed with transferable blocks above 8 and compared at
                # production semantics rather than the qualifier's min=4 tail.
                pv,_=prod.score_fold(ap,bp,hp,rep,'SYNTH',fold,None,td/f'prod-{rep}-{fold}',shard_bases=64)
                ok=(pv==sv==oracle)
                checks[f'{rep}_{fold}_production_equals_simple_equals_oracle']=ok
                if not ok:raise SystemExit(f'{rep} {fold}: prod={pv} simple={sv} oracle={oracle}')
                detail[rep][fold]={'production':pv,'simple':sv,'oracle':oracle}

            # Verify the frozen N1 dual-orientation seed derivation byte-for-byte
            # for the first A record, replicate 0, fold AB_C.
            for reverse,label in ((False,'FWD'),(True,'RC')):
                out1=td/f'n1-{rep}-{label}-1.fa';out2=td/f'n1-{rep}-{label}-2.fa'
                prod.write_oriented_dataset(fa,out1,rep,reverse,('SYNTH','AB_C',0))
                prod.write_oriented_dataset(fa,out2,rep,reverse,('SYNTH','AB_C',0))
                checks[f'{rep}_{label}_n1_deterministic']=(out1.read_bytes()==out2.read_bytes())
                if not checks[f'{rep}_{label}_n1_deterministic']:raise SystemExit('N1 nondeterministic')
                got=parse_one(out1)[0][1]
                name,raw=q.A[0]
                src=prod.orient.reverse_complement(raw) if reverse else raw
                projected=e.project_sequence(src,rep)
                cell=e.seed64(rep,'SYNTH','AB_C',0)
                seed=cell ^ first64(f'{name}|0|{label}')
                expected=e.generate_n1(projected,seed)
                checks[f'{rep}_{label}_n1_seed_exact']=(got==expected)
                if got!=expected:raise SystemExit(f'{rep} {label}: seed derivation mismatch')

        # Deterministic rerun of one complete null fold should be identical.
        v1,_=prod.score_fold(fa,fb,fc,'RY','SYNTH','AB_C',0,td/'null-rerun-1',shard_bases=64)
        v2,_=prod.score_fold(fa,fb,fc,'RY','SYNTH','AB_C',0,td/'null-rerun-2',shard_bases=64)
        checks['complete_null_fold_deterministic']=(v1==v2)
        if v1!=v2:raise SystemExit('complete null fold nondeterministic')

    payload={'schema':'LIFE_CODE_EXP0003_PRODUCTION_ENGINE_QUALIFICATION_V1','status':'PASS','synthetic_only':True,'primary_outcomes_inspected':False,'representations':REPS,'checks':checks,'detail':detail}
    Path('exp0003-production-qualification.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','checks':len(checks),'representations':len(REPS),'observed_fold_cells':48},sort_keys=True))

if __name__=='__main__':main()
