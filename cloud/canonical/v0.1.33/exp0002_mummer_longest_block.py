#!/usr/bin/env python3
"""
EXP-0002 LONGEST_BLOCK production wrapper around the real MUMmer exact-match
engine.

Frozen biological metric:
- exact maximal blocks;
- direct OR exact reverse-complement identity allowed;
- three held-out folds;
- triad value = median fold maximum.

v0.1.30 resource-bounded execution remains unchanged:
- reference FASTA is partitioned ONLY at pre-existing normalized FASTA record
  boundaries; records are never split;
- core `mummer -maxmatch` is run independently on each reference shard against
  the unchanged complete query FASTA;
- MUMmer stdout is streamed;
- candidate sequences are deduplicated in disk-backed SQLite;
- held-out testing is exact and longest-first.

v0.1.31 execution-resume correction:
- completed threshold/fold control-flow state is checkpointed atomically;
- interruption inside a threshold causes only that threshold to be recomputed;
- completed folds are cached privately for deterministic continuation;
- an authenticated v0.1.30 migration bridge may restart an interrupted fold at
  the threshold that v0.1.30 had already entered, while recomputing that current
  threshold from scratch;
- no partial candidate SQLite state from v0.1.30 is trusted.

The biological metric, threshold ladder, MUMmer flags, candidate reconstruction,
held-out folds, and median statistic are unchanged.
"""
from pathlib import Path
import argparse, subprocess, os, shutil, re, json, statistics, sqlite3, hashlib

DEFAULT_SHARD_BASES = 128 * 1024 * 1024
CANDIDATE_BATCH_BASES = 64 * 1024 * 1024
CANDIDATE_BATCH_RECORDS = 50000
FOLD_ORDER = ("AB_C","AC_B","BC_A")
CHECKPOINT_SCHEMA = "EXP0002_LONGEST_BLOCK_EXECUTION_CHECKPOINT_V1"

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def atomic_json(path,payload):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".partial")
    tmp.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    tmp.replace(path)

def exe():
    x=os.environ.get("MUMMER_EXE") or shutil.which("mummer")
    if not x: raise RuntimeError("mummer not found")
    return x

def iter_fasta(path):
    name=None;chunks=[]
    with open(path,encoding="ascii") as f:
        for raw in f:
            line=raw.strip()
            if not line:continue
            if line.startswith(">"):
                if name is not None:yield name,"".join(chunks).upper()
                name=line[1:].split()[0];chunks=[]
            else:chunks.append(line)
    if name is not None:yield name,"".join(chunks).upper()

def maxlen(path):
    m=0
    for _,s in iter_fasta(path):
        if len(s)>m:m=len(s)
    return m

def thresholds(a,b):
    m=min(maxlen(a),maxlen(b))
    p=1<<(max(m,8).bit_length()-1)
    vals=[]
    while p>=8:
        vals.append(p);p//=2
    if 8 not in vals:vals.append(8)
    return vals

def build_shards(source,outdir,cap_bases):
    """Copy whole FASTA records into deterministic bounded reference shards."""
    source=Path(source);outdir=Path(outdir)
    if outdir.exists():shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    shards=[];current=None;current_bases=0;current_records=0
    total_bases=0;total_records=0;max_record=0
    def open_new():
        nonlocal current,current_bases,current_records
        if current is not None:current.close()
        p=outdir/f"shard_{len(shards)+1:05d}.fa"
        current=open(p,"w",encoding="ascii");shards.append(p)
        current_bases=0;current_records=0
    for name,seq in iter_fasta(source):
        if not seq:continue
        if set(seq)-set("ACGT"):
            raise RuntimeError(f"non-ACGT sequence reached MUMmer shard stage: {source} {name}")
        if current is None or (current_records>0 and current_bases+len(seq)>cap_bases):
            open_new()
        current.write(f">{name}\n{seq}\n")
        current_bases+=len(seq);current_records+=1
        total_bases+=len(seq);total_records+=1;max_record=max(max_record,len(seq))
    if current is not None:current.close()
    if not shards:raise RuntimeError(f"no FASTA records to shard: {source}")
    manifest={"source":str(source.resolve()),"source_sha256":sha(source),"cap_bases":cap_bases,
              "shard_count":len(shards),"record_count":total_records,"total_bases":total_bases,
              "max_record_bases":max_record,"record_boundaries_preserved":True,"records_split":False}
    atomic_json(outdir/"SHARD_MANIFEST.json",manifest)
    return shards,manifest

def shard_ref_map(path):
    d={}
    for n,s in iter_fasta(path):
        if n in d:raise RuntimeError(f"duplicate FASTA record ID in shard: {n}")
        d[n]=s
    return d

def stream_mummer(ref,query,min_len,on_match,stderr_path):
    cmd=[exe(),"-maxmatch","-n","-l",str(min_len),"-b","-F",str(ref),str(query)]
    stderr_path=Path(stderr_path);stderr_path.parent.mkdir(parents=True,exist_ok=True)
    query_id=None;orient="+";count=0
    with open(stderr_path,"w",encoding="utf-8") as err:
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err,text=True,bufsize=1)
        assert p.stdout is not None
        for raw in p.stdout:
            line=raw.strip()
            if not line or line.startswith("#"):continue
            if line.startswith(">"):
                h=line[1:].strip()
                orient="-" if re.search(r"\bReverse\b",h) else "+"
                query_id=h.split()[0] if h else None
                continue
            parts=line.split()
            if len(parts)<4:continue
            try:
                m={"ref":parts[0],"ref_pos":int(parts[-3]),"query":query_id,
                   "query_pos":int(parts[-2]),"length":int(parts[-1]),"orientation":orient}
            except ValueError:continue
            count+=1
            on_match(m)
        rc=p.wait()
    if rc:
        tail=stderr_path.read_text(encoding="utf-8",errors="replace")[-20000:]
        raise RuntimeError("FAILED: "+" ".join(cmd)+"\n"+tail)
    return cmd,count

def candidate_db_for_threshold(train_ref_shards,train_query,min_len,work):
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    dbpath=work/"candidates.sqlite"
    if dbpath.exists():dbpath.unlink()
    con=sqlite3.connect(dbpath)
    con.execute("PRAGMA journal_mode=OFF");con.execute("PRAGMA synchronous=OFF")
    con.execute("PRAGMA temp_store=FILE")
    con.execute("CREATE TABLE candidates(seq BLOB PRIMARY KEY, length INTEGER NOT NULL)")
    commands=[];match_count=0;pending=0
    try:
        for si,shard in enumerate(train_ref_shards,1):
            refs=shard_ref_map(shard)
            def accept(m):
                nonlocal pending
                if m["length"]<min_len:return
                rid=m["ref"]
                if rid not in refs:raise RuntimeError(f"MUMmer reference ID not found in active shard: {rid}")
                start=m["ref_pos"]-1;end=start+m["length"];s=refs[rid]
                if start<0 or end>len(s):raise RuntimeError(f"MUMmer coordinate outside shard record: {rid}")
                seq=s[start:end]
                if len(seq)!=m["length"]:raise RuntimeError("candidate extraction length mismatch")
                if set(seq)<=set("ACGT"):
                    con.execute("INSERT OR IGNORE INTO candidates(seq,length) VALUES(?,?)",(seq.encode("ascii"),len(seq)))
                    pending+=1
                    if pending>=5000:con.commit();pending=0
            cmd,n=stream_mummer(shard,train_query,min_len,accept,work/f"train_shard_{si:05d}.stderr")
            commands.append(cmd);match_count+=n
        con.commit()
        con.execute("CREATE INDEX candidates_length_idx ON candidates(length DESC)");con.commit()
        n=con.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
        return con,n,commands,match_count
    except Exception:
        con.close();raise

def write_candidate_batch(rows,path,length):
    count=0;bases=0
    with open(path,"w",encoding="ascii") as f:
        for rowid,seqb in rows:
            seq=bytes(seqb).decode("ascii")
            if len(seq)!=length:raise RuntimeError("candidate DB length mismatch")
            f.write(f">C{rowid}|L{length}\n{seq}\n");count+=1;bases+=len(seq)
    return count,bases

def heldout_best(con,held_shards,min_threshold,work):
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    commands=[]
    lengths=[r[0] for r in con.execute("SELECT DISTINCT length FROM candidates ORDER BY length DESC")]
    for L in lengths:
        if L<min_threshold:continue
        cur=con.execute("SELECT rowid,seq FROM candidates WHERE length=? ORDER BY rowid",(L,))
        batch_no=0
        while True:
            rows=[];bases=0
            while len(rows)<CANDIDATE_BATCH_RECORDS and bases<CANDIDATE_BATCH_BASES:
                x=cur.fetchone()
                if x is None:break
                rows.append(x);bases+=L
            if not rows:break
            batch_no+=1;cand=work/f"candidates_L{L}_b{batch_no:05d}.fa"
            write_candidate_batch(rows,cand,L);found=False
            for si,shard in enumerate(held_shards,1):
                def accept(m):
                    nonlocal found
                    if m["query"] and m["length"]>=L:found=True
                cmd,_=stream_mummer(shard,cand,L,accept,work/f"held_L{L}_b{batch_no:05d}_s{si:05d}.stderr")
                commands.append(cmd)
                if found:
                    cand.unlink(missing_ok=True);return L,commands
            cand.unlink(missing_ok=True)
    return 0,commands

def input_sig(A,B,C):
    return {str(Path(p).resolve()):sha(Path(p)) for p in (A,B,C)}

def checkpoint_payload(A,B,C,shard_bases,current_fold,next_threshold,details,commands,completed_folds):
    return {"schema":CHECKPOINT_SCHEMA,"status":"IN_PROGRESS","wrapper_sha256":sha(Path(__file__)),
            "input_path_sha256":input_sig(A,B,C),"shard_bases":shard_bases,
            "current_fold":current_fold,"next_threshold":next_threshold,"threshold_detail_so_far":details,
            "commands_so_far":commands,"completed_folds":completed_folds}

def validate_resume_state(x,A,B,C,shard_bases):
    if x.get("input_path_sha256")!=input_sig(A,B,C):raise RuntimeError("LONGEST_BLOCK resume input signature mismatch")
    if int(x.get("shard_bases"))!=int(shard_bases):raise RuntimeError("LONGEST_BLOCK resume shard-cap mismatch")
    if x.get("current_fold") not in FOLD_ORDER:raise RuntimeError("LONGEST_BLOCK resume fold invalid")
    return x

def load_migration_bridge(path,A,B,C,shard_bases):
    if not path:return None
    p=Path(path);x=json.loads(p.read_text())
    if x.get("status")!="VERIFIED_PRE_V0131_LONGEST_BLOCK_CONTROL_FLOW_RESUME":raise RuntimeError("invalid v0.1.30 LONGEST_BLOCK migration bridge status")
    if x.get("target_mummer_wrapper_sha256")!=sha(Path(__file__)):raise RuntimeError("migration bridge targets different wrapper")
    if x.get("input_path_sha256")!=input_sig(A,B,C):raise RuntimeError("migration bridge input signature mismatch")
    if int(x.get("shard_bases"))!=int(shard_bases):raise RuntimeError("migration bridge shard-cap mismatch")
    if x.get("fold") not in FOLD_ORDER:raise RuntimeError("migration bridge fold invalid")
    return x

def fold(train_a,train_b,held,work,shard_sets,start_threshold=None,prior_details=None,prior_commands=None,checkpoint_cb=None):
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    commands=list(prior_commands or []);threshold_details=list(prior_details or [])
    train_shards=shard_sets[str(Path(train_a).resolve())][0]
    held_shards=shard_sets[str(Path(held).resolve())][0]
    ladder=thresholds(train_a,train_b)
    if start_threshold is not None:
        if int(start_threshold) not in ladder:raise RuntimeError("resume threshold not in deterministic threshold ladder")
        ladder=ladder[ladder.index(int(start_threshold)):]
    for pos,t in enumerate(ladder):
        tw=work/f"threshold_{t}"
        if tw.exists():shutil.rmtree(tw)
        tw.mkdir(parents=True);con=None
        try:
            con,ncand,cmds,nmatches=candidate_db_for_threshold(train_shards,train_b,t,tw/"train")
            commands.extend(cmds)
            td={"threshold":t,"training_match_records_seen":nmatches,"unique_candidate_sequences":ncand,"training_reference_shards":len(train_shards),"held_reference_shards":len(held_shards)}
            if ncand==0:
                threshold_details.append(td);con.close();con=None;shutil.rmtree(tw,ignore_errors=True)
                nxt=ladder[pos+1] if pos+1<len(ladder) else None
                if checkpoint_cb:checkpoint_cb(nxt,threshold_details,commands)
                continue
            best,hcmds=heldout_best(con,held_shards,t,tw/"held")
            commands.extend(hcmds);td["transfer_found"]=bool(best);threshold_details.append(td)
            con.close();con=None;shutil.rmtree(tw,ignore_errors=True)
            if best:return best,t,commands,threshold_details
            nxt=ladder[pos+1] if pos+1<len(ladder) else None
            if checkpoint_cb:checkpoint_cb(nxt,threshold_details,commands)
        finally:
            if con is not None:con.close()
        shutil.rmtree(tw,ignore_errors=True)
    return 0,8,commands,threshold_details

def main():
    ap=argparse.ArgumentParser();ap.add_argument("a");ap.add_argument("b");ap.add_argument("c");ap.add_argument("--work",required=True);ap.add_argument("--out",required=True);ap.add_argument("--shard-bases",type=int,default=DEFAULT_SHARD_BASES);ap.add_argument("--resume-bridge");a=ap.parse_args()
    if a.shard_bases<1024:raise SystemExit("--shard-bases must be >=1024 in production wrapper")
    A,B,C=map(Path,(a.a,a.b,a.c));work=Path(a.work);work.mkdir(parents=True,exist_ok=True)
    checkpoint=work/"LONGEST_BLOCK_CHECKPOINT.json";fold_cache=work/"_fold_cache";fold_cache.mkdir(exist_ok=True)
    shard_root=work/"_reference_shards"
    if shard_root.exists():shutil.rmtree(shard_root)
    shard_sets={}
    for label,p in (("A",A),("B",B),("C",C)):
        shards,manifest=build_shards(p,shard_root/label,a.shard_bases);shard_sets[str(p.resolve())]=(shards,manifest)
    resume=None
    if checkpoint.exists():
        x=json.loads(checkpoint.read_text())
        if x.get("status")=="IN_PROGRESS":resume=validate_resume_state(x,A,B,C,a.shard_bases)
    migration=load_migration_bridge(a.resume_bridge,A,B,C,a.shard_bases) if not resume else None
    vals=[];detail={};completed_folds=[];fold_specs=[("AB_C",A,B,C),("AC_B",A,C,B),("BC_A",B,C,A)]
    for fname,_,_,_ in fold_specs:
        fp=fold_cache/f"{fname}.json"
        if fp.exists():
            fc=json.loads(fp.read_text())
            if fc.get("input_path_sha256")!=input_sig(A,B,C) or fc.get("wrapper_sha256")!=sha(Path(__file__)):raise RuntimeError(f"{fname}: incompatible private fold cache")
            detail[fname]=fc["detail"];vals.append(fc["value"]);completed_folds.append(fname)
        else:break
    start_index=len(completed_folds)
    if start_index>=len(fold_specs):start_index=len(fold_specs)
    for idx in range(start_index,len(fold_specs)):
        name,x,y,h=fold_specs[idx];prior_details=[];prior_commands=[];start_threshold=None
        if resume and resume["current_fold"]==name:
            start_threshold=resume.get("next_threshold");prior_details=resume.get("threshold_detail_so_far") or [];prior_commands=resume.get("commands_so_far") or []
        elif migration and migration["fold"]==name:
            start_threshold=int(migration["restart_threshold"]);full=thresholds(x,y)
            if start_threshold not in full:raise RuntimeError("migration threshold absent from deterministic ladder")
            prior_details=[{"threshold":t,"execution_resume_status":"completed_pre_v0131_control_flow_checkpoint","diagnostic_counts_not_reconstructed":True} for t in full[:full.index(start_threshold)]];prior_commands=[];shutil.rmtree(work/name,ignore_errors=True)
        else:shutil.rmtree(work/name,ignore_errors=True)
        def save_cp(next_threshold,details_so_far,commands_so_far):
            if next_threshold is None:return
            atomic_json(checkpoint,checkpoint_payload(A,B,C,a.shard_bases,name,int(next_threshold),details_so_far,commands_so_far,completed_folds))
        if start_threshold is None:start_threshold=thresholds(x,y)[0]
        atomic_json(checkpoint,checkpoint_payload(A,B,C,a.shard_bases,name,int(start_threshold),prior_details,prior_commands,completed_folds))
        v,t,cmds,td=fold(x,y,h,work/name,shard_sets,start_threshold,prior_details,prior_commands,save_cp)
        fd={"longest_transferred_block":v,"stopping_threshold":t,"commands":cmds,"candidate_reconstruction":"reference_fasta_coordinates","execution_strategy":"record_boundary_reference_shards_streaming_sqlite_checkpointed","threshold_detail":td}
        fc={"status":"PRIVATE_FOLD_COMPLETE","fold":name,"value":v,"detail":fd,"wrapper_sha256":sha(Path(__file__)),"input_path_sha256":input_sig(A,B,C)}
        atomic_json(fold_cache/f"{name}.json",fc);detail[name]=fd;vals.append(v);completed_folds.append(name)
        if idx+1<len(fold_specs):
            nname,nx,ny,_=fold_specs[idx+1];nstart=thresholds(nx,ny)[0];atomic_json(checkpoint,checkpoint_payload(A,B,C,a.shard_bases,nname,int(nstart),[],[],completed_folds))
        resume=None;migration=None
    payload={"metric":"LONGEST_BLOCK","fold_values":vals,"LONGEST_BLOCK":statistics.median(vals),"candidate_reconstruction":"full_reference_fasta_sequence_from_mummer_coordinates","mummer_display_substring_used":False,"execution_strategy":"record_boundary_reference_shards_streaming_sqlite_exact_checkpointed","reference_shard_cap_bases":a.shard_bases,"records_split_by_execution_sharding":False,"fold_detail":detail}
    out=Path(a.out);out.write_text(json.dumps(payload,indent=2));atomic_json(checkpoint,{"schema":CHECKPOINT_SCHEMA,"status":"COMPLETE","wrapper_sha256":sha(Path(__file__)),"input_path_sha256":input_sig(A,B,C),"output_sha256":sha(out),"completed_folds":FOLD_ORDER});print(json.dumps(payload,indent=2))

if __name__=="__main__":main()
