#!/usr/bin/env python3
"""EXP-0003 three-genome transfer scorer primitives.

This module implements the frozen EXP-0003 transfer statistic on projected
representations without ever applying DNA reverse-complement semantics to an
already-projected stream.

For each fold, training candidates are exact maximal blocks shared by the two
training genomes under explicit raw-first orientation of the second genome.
Candidate sequence identity is taken from the forward-projected first training
genome.  Candidates are then tested exactly, longest-first, against both
raw-first projected orientations of the held-out genome.

The production-scale runner may shard/project records for resource control, but
must preserve these semantics exactly.
"""
from pathlib import Path
import os, re, shutil, subprocess, tempfile
import exp0003_engine as e
import exp0003_transfer as orient

FOLD_ORDER=("AB_C","AC_B","BC_A")


def _mummer_exe():
    x=os.environ.get('MUMMER_EXE') or shutil.which('mummer')
    if not x: raise RuntimeError('mummer not found')
    return x


def _write_records(path, records):
    with open(path,'w',encoding='ascii',newline='\n') as f:
        for name,seq in records:
            f.write(f'>{name}\n{seq}\n')


def oriented_projected_records(raw_fasta, representation, reverse=False):
    out=[]
    for name,raw in e.iter_fasta(raw_fasta):
        src=orient.reverse_complement(raw) if reverse else raw
        out.append((name,e.project_sequence(src,representation)))
    return out


def _ref_map(path):
    d={}
    for name,seq in e.iter_fasta(path):
        if name in d: raise RuntimeError(f'duplicate record id: {name}')
        d[name]=seq
    return d


def _stream_forward_matches(ref, query, min_len):
    cmd=[_mummer_exe(),'-maxmatch','-n','-l',str(min_len),'-F',str(ref),str(query)]
    p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('FAILED: '+' '.join(cmd)+'\n'+p.stderr[-20000:])
    qid=None
    for raw in p.stdout.splitlines():
        line=raw.strip()
        if not line or line.startswith('#'): continue
        if line.startswith('>'):
            h=line[1:].strip(); qid=h.split()[0] if h else None
            continue
        parts=line.split()
        if len(parts)<4: continue
        try:
            yield {
                'ref':parts[0],
                'ref_pos':int(parts[-3]),
                'query':qid,
                'query_pos':int(parts[-2]),
                'length':int(parts[-1]),
            }
        except ValueError:
            continue


def training_maximal_candidates(raw_a, raw_b, representation, min_len=1, work=None):
    root=Path(work) if work else Path(tempfile.mkdtemp(prefix='exp0003-triad-train-'))
    root.mkdir(parents=True,exist_ok=True)
    af=root/'a_fwd.fa'; bf=root/'b_fwd.fa'; br=root/'b_rc.fa'
    _write_records(af,oriented_projected_records(raw_a,representation,False))
    _write_records(bf,oriented_projected_records(raw_b,representation,False))
    _write_records(br,oriented_projected_records(raw_b,representation,True))
    refs=_ref_map(af)
    candidates=set()
    for q in (bf,br):
        for m in _stream_forward_matches(af,q,min_len):
            rid=m['ref']
            if rid not in refs: raise RuntimeError(f'unknown reference id: {rid}')
            i=m['ref_pos']-1; j=i+m['length']; seq=refs[rid]
            if i<0 or j>len(seq): raise RuntimeError('MUMmer coordinate outside record')
            s=seq[i:j]
            if len(s)!=m['length']: raise RuntimeError('candidate extraction mismatch')
            candidates.add(s)
    return candidates


def heldout_best(candidates, raw_held, representation, min_len=1, work=None):
    if not candidates: return 0
    root=Path(work) if work else Path(tempfile.mkdtemp(prefix='exp0003-triad-held-'))
    root.mkdir(parents=True,exist_ok=True)
    hf=root/'held_fwd.fa'; hr=root/'held_rc.fa'; cf=root/'candidates.fa'
    _write_records(hf,oriented_projected_records(raw_held,representation,False))
    _write_records(hr,oriented_projected_records(raw_held,representation,True))
    ordered=sorted((s for s in candidates if len(s)>=min_len),key=lambda s:(-len(s),s))
    with open(cf,'w',encoding='ascii',newline='\n') as f:
        for i,s in enumerate(ordered): f.write(f'>C{i}|L{len(s)}\n{s}\n')
    best=0
    for ref in (hf,hr):
        for m in _stream_forward_matches(ref,cf,min_len):
            if m['query'] and m['length']>best: best=m['length']
    # A MUMmer match can be a prefix/subblock of a candidate.  The frozen
    # transfer requirement is exact occurrence of the complete learned block,
    # so explicitly verify candidate identity against oriented held records.
    heldseq=[s for _,s in e.iter_fasta(hf)] + [s for _,s in e.iter_fasta(hr)]
    for s in ordered:
        if len(s)<=best and any(s in h for h in heldseq):
            return len(s)
    # best may be shorter than the first complete candidate; check all exactly.
    for s in ordered:
        if any(s in h for h in heldseq): return len(s)
    return 0


def fold_score(raw_a, raw_b, raw_held, representation, min_len=1, work=None):
    root=Path(work) if work else Path(tempfile.mkdtemp(prefix='exp0003-triad-fold-'))
    root.mkdir(parents=True,exist_ok=True)
    cand=training_maximal_candidates(raw_a,raw_b,representation,min_len,root/'train')
    best=heldout_best(cand,raw_held,representation,min_len,root/'held')
    return best, {'training_candidate_count':len(cand)}


def triad_scores(A,B,C,representation,min_len=1,work=None):
    root=Path(work) if work else Path(tempfile.mkdtemp(prefix='exp0003-triad-'))
    root.mkdir(parents=True,exist_ok=True)
    specs=[('AB_C',A,B,C),('AC_B',A,C,B),('BC_A',B,C,A)]
    vals={}; detail={}
    for name,x,y,h in specs:
        vals[name],detail[name]=fold_score(x,y,h,representation,min_len,root/name)
    return vals,detail
