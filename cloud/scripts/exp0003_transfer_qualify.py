#!/usr/bin/env python3
import hashlib,json,tempfile
from pathlib import Path
import exp0003_engine as e
import exp0003_transfer as t

REPS=['ACGT','RY','MK','WS',*e.CONTROL_TUPLES.keys()]
MOTIF='ACGTTGCAAGTCCGATGCTAACGTGACCTAGTCGATACGGTCA'
RAW_REF='TTGACCATGGAACCTT'+MOTIF+'CGTACCTAGGTTACGA'
RAW_QUERY=t.reverse_complement(MOTIF)

def sha256_text(s): return hashlib.sha256(s.encode()).hexdigest()

def main():
    checks={}; detail={}
    assert t.reverse_complement(t.reverse_complement(MOTIF))==MOTIF
    checks['dna_rc_involution']=True
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        ref=td/'ref.fa'; qry=td/'qry.fa'
        ref.write_text('>ref\n'+RAW_REF+'\n',encoding='ascii')
        qry.write_text('>qry\n'+RAW_QUERY+'\n',encoding='ascii')
        for rep in REPS:
            brute,bparts=t.brute_oriented_max(RAW_REF,RAW_QUERY,rep)
            vendor,vparts=t.oriented_mummer_max(ref,qry,rep,min_len=4,work=td/rep)
            ok=(brute==vendor==len(MOTIF) and vparts['reverse_raw_projected_max']==len(MOTIF))
            checks[f'{rep}_vendor_equals_brute_and_recovers_rc']=ok
            if not ok:
                raise SystemExit(f'{rep} mismatch brute={brute} vendor={vendor} b={bparts} v={vparts}')
            # Explicitly show that projected-stream DNA RC is not the orientation rule for quotients/controls.
            projected=e.project_sequence(RAW_QUERY,rep)
            naive_projected_dna_rc=t.reverse_complement(projected) if set(projected)<=set('ACGT') else None
            if rep!='ACGT':
                checks[f'{rep}_naive_projected_rc_not_used']=(naive_projected_dna_rc != e.project_sequence(t.reverse_complement(RAW_QUERY),rep))
                if not checks[f'{rep}_naive_projected_rc_not_used']:
                    raise SystemExit(f'{rep} naive projected RC unexpectedly equals frozen raw-first rule')
            detail[rep]={'brute':brute,'vendor':vendor,'vendor_parts':vparts,'brute_parts':bparts}
        # Memory-1 boundary reset: independent records must equal independent project_sequence calls.
        for cid in e.CONTROL_TUPLES:
            fa=td/f'{cid}-two.fa'; out=td/f'{cid}-two-proj.fa'
            fa.write_text('>a\nACGTTGCA\n>b\nTGCACGTA\n',encoding='ascii')
            t.write_oriented_projected_fasta(fa,out,cid,reverse=True)
            rows=list(e.iter_fasta(out))
            expected=[e.project_sequence(t.reverse_complement('ACGTTGCA'),cid),e.project_sequence(t.reverse_complement('TGCACGTA'),cid)]
            got=[s for _,s in rows]
            checks[f'{cid}_rc_record_state_reset']=(got==expected)
            if got!=expected: raise SystemExit(f'{cid} record reset mismatch')
    payload={
      'schema':'LIFE_CODE_EXP0003_TRANSFER_ORIENTATION_QUALIFICATION_V1',
      'status':'PASS',
      'synthetic_only':True,
      'exp0003_primary_outcomes_inspected':False,
      'representations_tested':REPS,
      'motif_length':len(MOTIF),
      'motif_sha256':sha256_text(MOTIF),
      'checks':checks,
      'detail':detail,
    }
    Path('exp0003-transfer-qualification.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','representations':len(REPS),'checks':len(checks)},sort_keys=True))

if __name__=='__main__': main()
