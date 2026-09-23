#!/usr/bin/env python3
"""Resource-bounded EXP-0003 fold scorer.

Production adaptation of the canonical EXP-0002 LONGEST_BLOCK execution strategy:
- exact maximal training blocks;
- deterministic power-of-two threshold ladder down to 8;
- reference sharding only at existing FASTA record boundaries;
- MUMmer 4.0.1 forward-only exact matching;
- disk-backed SQLite candidate deduplication;
- longest-first exact held-out testing;
- explicit P(x) and P(RC(x)) streams for observed and N1 data.

Scientific orientation/null semantics are frozen in EXP-0003 protocol records.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, sqlite3, subprocess
import exp0003_engine as e
import exp0003_transfer as orient

DEFAULT_SHARD_BASES=128*1024*1024
CANDIDATE_BATCH_BASES=64*1024*1024
CANDIDATE_BATCH_RECORDS=50000


def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def atomic_json(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_suffix(p.suffix+'.partial')
    q.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    q.replace(p)


def mummer_exe():
    x=os.environ.get('MUMMER_EXE') or shutil.which('mummer')
    if not x:raise RuntimeError('mummer not found')
    return x


def first64(s):return int(hashlib.sha256(s.encode('utf-8')).hexdigest()[:16],16)


def write_oriented_dataset(raw_path,out_path,representation,reverse=False,null_cell=None):
    """Write observed or N1 orientation stream record-by-record.

    null_cell is None for observed, otherwise tuple (triad_id,fold,replicate).
    """
    orientation='RC' if reverse else 'FWD'
    out_path=Path(out_path);out_path.parent.mkdir(parents=True,exist_ok=True)
    with open(out_path,'w',encoding='ascii',newline='\n') as dst:
        for idx,(name,raw) in enumerate(e.iter_fasta(raw_path)):
            src=orient.reverse_complement(raw) if reverse else raw
            projected=e.project_sequence(src,representation)
            if null_cell is not None:
                triad,fold,replicate=null_cell
                cell=e.seed64(representation,triad,fold,replicate)
                seed=cell ^ first64(f'{name}|{idx}|{orientation}')
                projected=e.generate_n1(projected,seed)
            dst.write(f'>{name}|{orientation}\n{projected}\n')
    return out_path


def max_record_len(path):
    return max((len(s) for _,s in e.iter_fasta(path)),default=0)


def thresholds(a,b):
    m=min(max_record_len(a),max_record_len(b))
    if m<8:return [8]
    p=1<<(m.bit_length()-1);vals=[]
    while p>=8:vals.append(p);p//=2
    return vals


def build_shards(source,outdir,cap_bases):
    source=Path(source);outdir=Path(outdir)
    if outdir.exists():shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    shards=[];fh=None;bases=0;records=0
    def new():
        nonlocal fh,bases,records
        if fh:fh.close()
        p=outdir/f'shard_{len(shards)+1:05d}.fa';shards.append(p)
        fh=open(p,'w',encoding='ascii',newline='\n');bases=0;records=0
    for name,seq in e.iter_fasta(source):
        if not seq:continue
        if fh is None or (records and bases+len(seq)>cap_bases):new()
        fh.write(f'>{name}\n{seq}\n');bases+=len(seq);records+=1
    if fh:fh.close()
    if not shards:raise RuntimeError(f'no FASTA records: {source}')
    return shards


def ref_map(path):
    d={}
    for n,s in e.iter_fasta(path):
        if n in d:raise RuntimeError(f'duplicate ref id {n}')
        d[n]=s
    return d


def stream_matches(ref,query,min_len,on_match,stderr):
    cmd=[mummer_exe(),'-maxmatch','-n','-l',str(min_len),'-F',str(ref),str(query)]
    stderr=Path(stderr);stderr.parent.mkdir(parents=True,exist_ok=True)
    qid=None;count=0
    with open(stderr,'w',encoding='utf-8') as err:
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err,text=True,bufsize=1)
        assert p.stdout is not None
        for raw in p.stdout:
            line=raw.strip()
            if not line or line.startswith('#'):continue
            if line.startswith('>'):
                h=line[1:].strip();qid=h.split()[0] if h else None;continue
            z=line.split()
            if len(z)<4:continue
            try:m={'ref':z[0],'ref_pos':int(z[-3]),'query':qid,'query_pos':int(z[-2]),'length':int(z[-1])}
            except ValueError:continue
            count+=1;on_match(m)
        rc=p.wait()
    if rc:
        tail=stderr.read_text(encoding='utf-8',errors='replace')[-20000:]
        raise RuntimeError('FAILED: '+' '.join(cmd)+'\n'+tail)
    return count


def candidate_db(train_ref_shards,train_queries,min_len,work):
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    db=work/'candidates.sqlite';db.unlink(missing_ok=True)
    con=sqlite3.connect(db);con.execute('PRAGMA journal_mode=OFF');con.execute('PRAGMA synchronous=OFF');con.execute('PRAGMA temp_store=FILE')
    con.execute('CREATE TABLE candidates(seq BLOB PRIMARY KEY,length INTEGER NOT NULL)')
    pending=0;matches=0
    try:
        for si,shard in enumerate(train_ref_shards,1):
            refs=ref_map(shard)
            for qi,query in enumerate(train_queries,1):
                def accept(m):
                    nonlocal pending
                    if m['length']<min_len:return
                    rid=m['ref'];start=m['ref_pos']-1;end=start+m['length']
                    if rid not in refs:raise RuntimeError('unknown reference ID')
                    s=refs[rid]
                    if start<0 or end>len(s):raise RuntimeError('coordinate outside reference record')
                    cand=s[start:end]
                    con.execute('INSERT OR IGNORE INTO candidates(seq,length) VALUES(?,?)',(cand.encode('ascii'),len(cand)))
                    pending+=1
                    if pending>=5000:con.commit();pending=0
                matches+=stream_matches(shard,query,min_len,accept,work/f'train_s{si:05d}_q{qi}.stderr')
        con.commit();con.execute('CREATE INDEX candidates_length_idx ON candidates(length DESC)');con.commit()
        n=con.execute('SELECT COUNT(*) FROM candidates').fetchone()[0]
        return con,n,matches
    except Exception:
        con.close();raise


def write_batch(rows,path,L):
    with open(path,'w',encoding='ascii',newline='\n') as f:
        for rowid,seqb in rows:
            seq=bytes(seqb).decode('ascii')
            if len(seq)!=L:raise RuntimeError('candidate length mismatch')
            f.write(f'>C{rowid}|L{L}\n{seq}\n')


def heldout_best(con,held_shard_sets,min_threshold,work):
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    lengths=[r[0] for r in con.execute('SELECT DISTINCT length FROM candidates ORDER BY length DESC')]
    for L in lengths:
        if L<min_threshold:continue
        cur=con.execute('SELECT rowid,seq FROM candidates WHERE length=? ORDER BY rowid',(L,));batch=0
        while True:
            rows=[];bases=0
            while len(rows)<CANDIDATE_BATCH_RECORDS and bases<CANDIDATE_BATCH_BASES:
                x=cur.fetchone()
                if x is None:break
                rows.append(x);bases+=L
            if not rows:break
            batch+=1;cand=work/f'candidates_L{L}_b{batch:05d}.fa';write_batch(rows,cand,L)
            found=False
            for oi,shards in enumerate(held_shard_sets,1):
                for si,shard in enumerate(shards,1):
                    def accept(m):
                        nonlocal found
                        if m['query'] and m['length']>=L:found=True
                    stream_matches(shard,cand,L,accept,work/f'held_o{oi}_s{si:05d}_L{L}_b{batch:05d}.stderr')
                    if found:break
                if found:break
            cand.unlink(missing_ok=True)
            if found:return L
    return 0


def score_fold(raw_a,raw_b,raw_h,representation,triad_id,fold_name,replicate,work,shard_bases=DEFAULT_SHARD_BASES):
    root=Path(work);root.mkdir(parents=True,exist_ok=True)
    null_cell=None if replicate is None else (triad_id,fold_name,int(replicate))
    files={}
    for label,path in [('A',raw_a),('B',raw_b),('H',raw_h)]:
        for rev in (False,True):
            olabel='RC' if rev else 'FWD';p=root/f'{label}_{olabel}.fa'
            files[(label,olabel)]=write_oriented_dataset(path,p,representation,rev,null_cell)
    # Candidate identity is anchored in train-A forward representation. Train-B
    # contributes both frozen raw-derived orientations.
    train_ref=build_shards(files[('A','FWD')],root/'shards_trainA',shard_bases)
    held_f=build_shards(files[('H','FWD')],root/'shards_heldF',shard_bases)
    held_r=build_shards(files[('H','RC')],root/'shards_heldR',shard_bases)
    ladder=thresholds(files[('A','FWD')],files[('B','FWD')])
    detail=[]
    for threshold in ladder:
        tw=root/f'threshold_{threshold}'
        if tw.exists():shutil.rmtree(tw)
        tw.mkdir(parents=True);con=None
        try:
            con,ncand,nmatch=candidate_db(train_ref,[files[('B','FWD')],files[('B','RC')]],threshold,tw/'train')
            row={'threshold':threshold,'unique_candidate_sequences':ncand,'training_match_records_seen':nmatch}
            if ncand:
                best=heldout_best(con,[held_f,held_r],threshold,tw/'held');row['transfer_found']=bool(best)
                detail.append(row)
                if best:
                    con.close();shutil.rmtree(tw,ignore_errors=True)
                    return best,detail
            else:detail.append(row)
        finally:
            if con is not None:con.close()
        shutil.rmtree(tw,ignore_errors=True)
    return 0,detail


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('a');ap.add_argument('b');ap.add_argument('held')
    ap.add_argument('--representation',required=True)
    ap.add_argument('--triad-id',required=True);ap.add_argument('--fold',required=True)
    ap.add_argument('--replicate',type=int)
    ap.add_argument('--work',required=True);ap.add_argument('--out',required=True)
    ap.add_argument('--shard-bases',type=int,default=DEFAULT_SHARD_BASES)
    x=ap.parse_args()
    if x.representation not in ['ACGT','RY','MK','WS',*e.CONTROL_TUPLES.keys()]:raise SystemExit('invalid representation')
    if x.fold not in ('AB_C','AC_B','BC_A'):raise SystemExit('invalid fold')
    if x.replicate is not None and not 0<=x.replicate<99:raise SystemExit('replicate must be 0..98')
    v,detail=score_fold(Path(x.a),Path(x.b),Path(x.held),x.representation,x.triad_id,x.fold,x.replicate,Path(x.work),x.shard_bases)
    payload={'schema':'LIFE_CODE_EXP0003_FOLD_SCORE_V1','triad_id':x.triad_id,'fold':x.fold,'representation':x.representation,'replicate':x.replicate,'Lstar':v,'null':x.replicate is not None,'detail':detail}
    Path(x.out).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:payload[k] for k in ('triad_id','fold','representation','replicate','Lstar')},sort_keys=True))

if __name__=='__main__':main()
