#!/usr/bin/env python3
import hashlib,json,tempfile
from pathlib import Path
import exp0003_engine as e

TEST_SEQ='ACGTACGTTGCAACGT'
EXPECTED={
 'ACGT':'ACGTACGTTGCAACGT',
 'RY':'ACACACACCACAACAC',
 'MK':'AACCAACCCCAAAACC',
 'WS':'ACCAACCAACCAACCA',
}

def sha_text(s):return hashlib.sha256(s.encode()).hexdigest()

def main():
    checks={}
    for rep,exp in EXPECTED.items():
        got=e.project_sequence(TEST_SEQ,rep)
        checks[f'projection_{rep}']=(got==exp)
        if got!=exp: raise SystemExit(f'{rep} projection mismatch: {got} != {exp}')
    for cid in e.CONTROL_TUPLES:
        a=e.project_sequence(TEST_SEQ,cid);b=e.project_sequence(TEST_SEQ,cid)
        checks[f'control_{cid}_deterministic']=(a==b and set(a)<=set('AC') and len(a)==len(TEST_SEQ))
        if not checks[f'control_{cid}_deterministic']:raise SystemExit(f'control fail {cid}')
    s0=e.seed64('RY','B1','AB_C',0);s0b=e.seed64('RY','B1','AB_C',0);s1=e.seed64('RY','B1','AB_C',1)
    checks['seed_schedule_reproducible']=(s0==s0b and s0!=s1)
    if not checks['seed_schedule_reproducible']:raise SystemExit('seed schedule fail')
    source='AACCAACCAACCAACCAACCAACC'
    n0=e.generate_n1(source,s0);n0b=e.generate_n1(source,s0);n1=e.generate_n1(source,s1)
    checks['n1_same_seed_same_output']=(n0==n0b)
    checks['n1_length_preserved']=(len(n0)==len(source))
    checks['n1_alphabet_preserved']=(set(n0)<=set(source))
    checks['n1_different_seed_changes_output']=(n0!=n1)
    if not all(checks.values()):raise SystemExit('qualification check failed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'in.fa';p.write_text('>r1\nACGTACGT\n>r2\nTTTTCCCCAAAAGGGG\n',encoding='ascii')
        for rep in ['ACGT','RY','MK','WS',*e.CONTROL_TUPLES.keys()]:
            out=Path(td)/f'{rep}.fa';e.write_projected_fasta(p,out,rep)
            rows=list(e.iter_fasta(out));src=list(e.iter_fasta(p))
            assert [x[0] for x in rows]==[x[0] for x in src]
            assert [len(x[1]) for x in rows]==[len(x[1]) for x in src]
        q1=Path(td)/'n1a.fa';q2=Path(td)/'n1b.fa'
        e.write_n1_fasta(p,q1,'RY','B1','AB_C',0);e.write_n1_fasta(p,q2,'RY','B1','AB_C',0)
        checks['fasta_n1_reproducible']=q1.read_bytes()==q2.read_bytes()
    payload={'schema':'LIFE_CODE_EXP0003_ENGINE_QUALIFICATION_V1','status':'PASS','synthetic_only':True,'exp0003_outcomes_inspected':False,'checks':checks,'test_sequence_sha256':sha_text(TEST_SEQ)}
    Path('exp0003-engine-qualification.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(payload,sort_keys=True))

if __name__=='__main__':main()
