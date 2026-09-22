#!/usr/bin/env python3
import argparse,hashlib,json,os,re,shutil,sqlite3,subprocess
from pathlib import Path

CANONICAL_WRAPPER_SHA256='f3b9fb457a4ee11fe41af70962b7d268f4f12ef22e2441b20160379c9208db5e'
DEFAULT_SHARD_BASES=128*1024*1024
TARGET_LEN=299
THRESHOLD=256


def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def iter_fasta(path):
    name=None;chunks=[]
    with open(path,encoding='ascii') as f:
        for raw in f:
            line=raw.strip()
            if not line:continue
            if line.startswith('>'):
                if name is not None:yield name,''.join(chunks).upper()
                name=line[1:].split()[0];chunks=[]
            else:chunks.append(line)
    if name is not None:yield name,''.join(chunks).upper()


def stream_shards(source,outdir,cap=DEFAULT_SHARD_BASES):
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    batch=[];bases=0;idx=0
    def emit(records,n):
        p=outdir/f'shard_{n:05d}.fa'
        with open(p,'w',encoding='ascii') as f:
            for name,seq in records:f.write(f'>{name}\n{seq}\n')
        return p
    for name,seq in iter_fasta(source):
        if not seq:continue
        if set(seq)-set('ACGT'):raise RuntimeError(f'non-ACGT sequence: {source} {name}')
        if batch and bases+len(seq)>cap:
            idx+=1;p=emit(batch,idx)
            try:yield idx,p
            finally:p.unlink(missing_ok=True)
            batch=[];bases=0
        batch.append((name,seq));bases+=len(seq)
    if batch:
        idx+=1;p=emit(batch,idx)
        try:yield idx,p
        finally:p.unlink(missing_ok=True)


def shard_ref_map(path):return {n:s for n,s in iter_fasta(path)}


def mummer_exe():
    x=os.environ.get('MUMMER_EXE') or shutil.which('mummer')
    if not x:raise RuntimeError('mummer not found')
    return x


def stream_mummer(ref,query,min_len,on_match,stderr_path):
    cmd=[mummer_exe(),'-maxmatch','-n','-l',str(min_len),'-b','-F',str(ref),str(query)]
    stderr_path=Path(stderr_path);stderr_path.parent.mkdir(parents=True,exist_ok=True)
    query_id=None;orient='+';count=0
    with open(stderr_path,'w',encoding='utf-8') as err:
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err,text=True,bufsize=1)
        for raw in p.stdout:
            line=raw.strip()
            if not line or line.startswith('#'):continue
            if line.startswith('>'):
                h=line[1:].strip();orient='-' if re.search(r'\bReverse\b',h) else '+';query_id=h.split()[0] if h else None;continue
            parts=line.split()
            if len(parts)<4:continue
            try:m={'ref':parts[0],'ref_pos':int(parts[-3]),'query':query_id,'query_pos':int(parts[-2]),'length':int(parts[-1]),'orientation':orient}
            except ValueError:continue
            count+=1;on_match(m)
        rc=p.wait()
    if rc:raise RuntimeError('FAILED: '+' '.join(cmd)+'\n'+stderr_path.read_text(errors='replace')[-20000:])
    return count


def candidate_db(train_ref,train_query,work):
    work=Path(work);work.mkdir(parents=True,exist_ok=True);db=work/'candidates.sqlite'
    if db.exists():db.unlink()
    con=sqlite3.connect(db);con.execute('PRAGMA journal_mode=OFF');con.execute('PRAGMA synchronous=OFF');con.execute('PRAGMA temp_store=FILE');con.execute('CREATE TABLE candidates(seq BLOB PRIMARY KEY,length INTEGER NOT NULL)')
    match_count=0;pending=0;shards=0
    for si,shard in stream_shards(train_ref,work/'streamed_train_shards'):
        shards=si;refs=shard_ref_map(shard)
        def accept(m):
            nonlocal pending
            if m['length']<THRESHOLD:return
            rid=m['ref'];start=m['ref_pos']-1;end=start+m['length'];seq=refs[rid][start:end]
            if len(seq)!=m['length']:raise RuntimeError('candidate extraction mismatch')
            if set(seq)<=set('ACGT'):
                con.execute('INSERT OR IGNORE INTO candidates(seq,length) VALUES(?,?)',(seq.encode('ascii'),len(seq)));pending+=1
                if pending>=5000:con.commit();pending=0
        match_count+=stream_mummer(shard,train_query,THRESHOLD,accept,work/f'train_{si:05d}.stderr')
    con.commit();con.execute('CREATE INDEX candidates_length_idx ON candidates(length DESC)');con.commit()
    return con,con.execute('SELECT COUNT(*) FROM candidates').fetchone()[0],match_count,shards


def write_candidates(rows,path):
    with open(path,'w',encoding='ascii') as f:
        for rowid,seqb in rows:f.write(f'>C{rowid}|L{TARGET_LEN}\n{bytes(seqb).decode("ascii")}\n')


def query_hits(query_fa,ref_source,min_len,work):
    hits=[];shards=0
    for si,shard in stream_shards(ref_source,Path(work)/'streamed_ref_shards'):
        shards=si
        def accept(m):
            if m.get('query') and m['length']>=min_len:
                x=dict(m);x['shard_index']=si;hits.append(x)
        stream_mummer(shard,query_fa,min_len,accept,Path(work)/f'shard_{si:05d}.stderr')
    return hits,shards


def parse_candidate(qid):
    m=re.match(r'^C(\d+)\|L(\d+)$',qid or '')
    return (int(m.group(1)),int(m.group(2))) if m else (None,None)


def write_query(path,seq,rowid):Path(path).write_text(f'>C{rowid}|L{TARGET_LEN}\n{seq}\n',encoding='ascii')


def one_fold(name,train_a,train_b,held,work):
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    con,ncand,nmatches,train_shard_count=candidate_db(train_a,train_b,work/'candidate_build')
    rows=con.execute('SELECT rowid,seq FROM candidates WHERE length=? ORDER BY rowid',(TARGET_LEN,)).fetchall();byrow={r:bytes(s).decode('ascii') for r,s in rows}
    cand=work/'candidates_299.fa';write_candidates(rows,cand)
    held_hits,held_shard_count=query_hits(cand,held,TARGET_LEN,work/'held_scan') if rows else ([],0)
    winner_rows=[];seen=set()
    for h in held_hits:
        rowid,L=parse_candidate(h.get('query'))
        if rowid in byrow and L==TARGET_LEN and rowid not in seen:seen.add(rowid);winner_rows.append(rowid)
    winners=[]
    for rowid in winner_rows:
        seq=byrow[rowid];q=work/f'winner_{rowid}.fa';write_query(q,seq,rowid)
        ah,_=query_hits(q,train_a,TARGET_LEN,work/f'map_{rowid}_a');bh,_=query_hits(q,train_b,TARGET_LEN,work/f'map_{rowid}_b');hh,_=query_hits(q,held,TARGET_LEN,work/f'map_{rowid}_held')
        winners.append({'candidate_rowid':rowid,'sequence':seq,'sequence_sha256':hashlib.sha256(seq.encode()).hexdigest(),'train_a_hits':ah,'train_b_hits':bh,'held_hits':hh})
    con.close()
    return {'fold':name,'threshold':THRESHOLD,'target_length':TARGET_LEN,'training_match_records_seen':nmatches,'unique_candidates_all_lengths':ncand,'candidate_count_length_299':len(rows),'heldout_hit_count_length_ge_299':len(held_hits),'training_reference_shards':train_shard_count,'held_reference_shards':held_shard_count,'first_heldout_shard_with_hit':min((h['shard_index'] for h in held_hits),default=None),'winner_count':len(winners),'winners':winners}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--human',required=True);ap.add_argument('--chicken',required=True);ap.add_argument('--zebrafish',required=True);ap.add_argument('--work',default='forensics-work');ap.add_argument('--out',default='EXP0002A_A3_299_FORENSICS.json');a=ap.parse_args()
    paths={'A_HSAP':Path(a.human),'A_GGAL':Path(a.chicken),'A_DRER':Path(a.zebrafish)}
    for k,p in paths.items():
        if not p.exists():raise SystemExit(f'MISSING_INPUT {k} {p}')
    folds=[('AB_C',paths['A_HSAP'],paths['A_GGAL'],paths['A_DRER']),('AC_B',paths['A_HSAP'],paths['A_DRER'],paths['A_GGAL']),('BC_A',paths['A_GGAL'],paths['A_DRER'],paths['A_HSAP'])]
    root=Path(a.work);root.mkdir(parents=True,exist_ok=True);results=[one_fold(*f,root/f[0]) for f in folds]
    sets=[{w['sequence_sha256'] for w in r['winners']} for r in results];common=set.intersection(*sets) if sets else set()
    version=subprocess.check_output([mummer_exe(),'--version'],text=True,stderr=subprocess.STDOUT).strip()
    payload={'schema':'LIFE_CODE_EXP0002A_A3_299_FORENSICS_V1','status':'COMPLETE','method_state':'POST_FREEZE_FORENSIC_DERIVATIVE_OF_CANONICAL_LONGEST_BLOCK','canonical_longest_block_wrapper_sha256_reference':CANONICAL_WRAPPER_SHA256,'mummer_executable':mummer_exe(),'mummer_version':version,'input_sha256':{k:sha256(v) for k,v in paths.items()},'threshold':THRESHOLD,'target_length':TARGET_LEN,'folds':results,'sequence_hashes_common_to_all_three_folds':sorted(common),'same_299_sequence_present_in_all_three_folds':bool(common)}
    Path(a.out).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps({'status':'COMPLETE','winner_counts':{r['fold']:r['winner_count'] for r in results},'common_sequence_count':len(common)},sort_keys=True))

if __name__=='__main__':main()
