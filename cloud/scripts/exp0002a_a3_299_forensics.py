#!/usr/bin/env python3
import argparse,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path

EXPECTED_WRAPPER_SHA='f3b9fb457a4ee11fe41af70962b7d268f4f12ef22e2441b20160379c9208db5e'
TARGET_LEN=299
THRESHOLD=256


def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def load_wrapper(path):
    if sha256(path)!=EXPECTED_WRAPPER_SHA:
        raise SystemExit(f'CANONICAL_MUMMER_WRAPPER_SHA_MISMATCH {sha256(path)}')
    spec=importlib.util.spec_from_file_location('canon_mummer',path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def query_hits(mod,query_fa,ref_shards,min_len,work):
    hits=[]
    for si,shard in enumerate(ref_shards,1):
        def accept(m):
            if m.get('query') and m['length']>=min_len:
                x=dict(m); x['shard_index']=si; hits.append(x)
        mod.stream_mummer(shard,query_fa,min_len,accept,Path(work)/f'shard_{si:05d}.stderr')
    return hits


def candidate_id_to_rowid(qid):
    m=re.match(r'^C(\d+)\|L(\d+)$',qid or '')
    return (int(m.group(1)),int(m.group(2))) if m else (None,None)


def write_query(path,seq,label='Q'):
    Path(path).write_text(f'>{label}\n{seq}\n',encoding='ascii')


def one_fold(mod,name,train_a,train_b,held,work):
    work=Path(work); work.mkdir(parents=True,exist_ok=True)
    train_shards,_=mod.build_shards(train_a,work/'train_ref_shards',mod.DEFAULT_SHARD_BASES)
    held_shards,_=mod.build_shards(held,work/'held_shards',mod.DEFAULT_SHARD_BASES)
    con,ncand,_,nmatches=mod.candidate_db_for_threshold(train_shards,train_b,THRESHOLD,work/'candidate_build')
    rows=con.execute('SELECT rowid,seq FROM candidates WHERE length=? ORDER BY rowid',(TARGET_LEN,)).fetchall()
    candidate_fa=work/'candidates_299.fa'
    mod.write_candidate_batch(rows,candidate_fa,TARGET_LEN)
    held_hits=query_hits(mod,candidate_fa,held_shards,TARGET_LEN,work/'held_scan') if rows else []
    byrow={rowid:bytes(seqb).decode('ascii') for rowid,seqb in rows}
    winner_rows=[]
    seen=set()
    for h in held_hits:
        rowid,L=candidate_id_to_rowid(h.get('query'))
        if rowid is None or L!=TARGET_LEN or rowid not in byrow: continue
        if rowid not in seen:
            seen.add(rowid); winner_rows.append(rowid)
    winners=[]
    all_a,_=mod.build_shards(train_a,work/'map_train_a',mod.DEFAULT_SHARD_BASES)
    all_b,_=mod.build_shards(train_b,work/'map_train_b',mod.DEFAULT_SHARD_BASES)
    for rowid in winner_rows:
        seq=byrow[rowid]; q=work/f'winner_{rowid}.fa'; write_query(q,seq,f'C{rowid}|L{TARGET_LEN}')
        winners.append({
            'candidate_rowid':rowid,
            'sequence':seq,
            'sequence_sha256':hashlib.sha256(seq.encode('ascii')).hexdigest(),
            'train_a_hits':query_hits(mod,q,all_a,TARGET_LEN,work/f'map_{rowid}_a'),
            'train_b_hits':query_hits(mod,q,all_b,TARGET_LEN,work/f'map_{rowid}_b'),
            'held_hits':query_hits(mod,q,held_shards,TARGET_LEN,work/f'map_{rowid}_held')
        })
    con.close()
    first_shard=min((h['shard_index'] for h in held_hits),default=None)
    return {
        'fold':name,'threshold':THRESHOLD,'target_length':TARGET_LEN,
        'training_match_records_seen':nmatches,'unique_candidates_all_lengths':ncand,
        'candidate_count_length_299':len(rows),'heldout_hit_count_length_ge_299':len(held_hits),
        'first_heldout_shard_with_hit':first_shard,'winner_count':len(winners),'winners':winners
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--human',required=True);ap.add_argument('--chicken',required=True);ap.add_argument('--zebrafish',required=True)
    ap.add_argument('--wrapper',default='cloud/canonical/v0.1.33/exp0002_mummer_longest_block.py')
    ap.add_argument('--work',default='forensics-work');ap.add_argument('--out',default='EXP0002A_A3_299_FORENSICS.json')
    a=ap.parse_args(); mod=load_wrapper(a.wrapper)
    paths={'A_HSAP':Path(a.human),'A_GGAL':Path(a.chicken),'A_DRER':Path(a.zebrafish)}
    for k,p in paths.items():
        if not p.exists(): raise SystemExit(f'MISSING_INPUT {k} {p}')
    folds=[('AB_C',paths['A_HSAP'],paths['A_GGAL'],paths['A_DRER']),('AC_B',paths['A_HSAP'],paths['A_DRER'],paths['A_GGAL']),('BC_A',paths['A_GGAL'],paths['A_DRER'],paths['A_HSAP'])]
    root=Path(a.work);root.mkdir(parents=True,exist_ok=True)
    results=[one_fold(mod,*f,root/f[0]) for f in folds]
    sets=[{w['sequence_sha256'] for w in r['winners']} for r in results]
    common=set.intersection(*sets) if sets else set()
    payload={
      'schema':'LIFE_CODE_EXP0002A_A3_299_FORENSICS_V1','status':'COMPLETE',
      'canonical_mummer_wrapper_sha256':sha256(a.wrapper),'mummer_executable':os.environ.get('MUMMER_EXE') or shutil.which('mummer'),
      'mummer_version':subprocess.check_output([os.environ.get('MUMMER_EXE') or shutil.which('mummer'),'--version'],text=True,stderr=subprocess.STDOUT).strip(),
      'input_sha256':{k:sha256(v) for k,v in paths.items()},'threshold':THRESHOLD,'target_length':TARGET_LEN,
      'folds':results,'sequence_hashes_common_to_all_three_folds':sorted(common),
      'same_299_sequence_present_in_all_three_folds':bool(common)
    }
    Path(a.out).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'COMPLETE','winner_counts':{r['fold']:r['winner_count'] for r in results},'common_sequence_count':len(common)},sort_keys=True))

if __name__=='__main__':main()
