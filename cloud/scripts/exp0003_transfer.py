#!/usr/bin/env python3
import os,re,shutil,subprocess,tempfile
from pathlib import Path
import exp0003_engine as e

DNA_COMP=str.maketrans('ACGT','TGCA')

def reverse_complement(seq):
    s=seq.upper()
    if set(s)-set('ACGT'): raise ValueError('reverse complement input must be ACGT only')
    return s.translate(DNA_COMP)[::-1]

def write_oriented_projected_fasta(inp,out,representation,reverse=False):
    with open(out,'w',encoding='ascii',newline='\n') as dst:
        for name,raw in e.iter_fasta(inp):
            src=reverse_complement(raw) if reverse else raw
            proj=e.project_sequence(src,representation)
            suffix='|RC' if reverse else '|FWD'
            dst.write(f'>{name}{suffix}\n{proj}\n')

def mummer_exe():
    x=os.environ.get('MUMMER_EXE') or shutil.which('mummer')
    if not x: raise RuntimeError('mummer not found')
    return x

def _parse_mummer_max(stdout):
    best=0
    qid=None
    for raw in stdout.splitlines():
        line=raw.strip()
        if not line or line.startswith('#'): continue
        if line.startswith('>'):
            qid=line[1:].strip().split()[0] if line[1:].strip() else None
            continue
        parts=line.split()
        if len(parts)<4: continue
        try: L=int(parts[-1])
        except ValueError: continue
        if L>best: best=L
    return best

def mummer_forward_max(ref_fa,query_fa,min_len=1):
    cmd=[mummer_exe(),'-maxmatch','-n','-l',str(min_len),'-F',str(ref_fa),str(query_fa)]
    p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('FAILED: '+' '.join(cmd)+'\n'+p.stderr[-20000:])
    return _parse_mummer_max(p.stdout)

def oriented_mummer_max(raw_ref,raw_query,representation,min_len=1,work=None):
    root=Path(work) if work else Path(tempfile.mkdtemp(prefix='exp0003-transfer-'))
    root.mkdir(parents=True,exist_ok=True)
    ref=root/'ref.fa'; qf=root/'query_fwd.fa'; qr=root/'query_rc.fa'
    write_oriented_projected_fasta(raw_ref,ref,representation,False)
    write_oriented_projected_fasta(raw_query,qf,representation,False)
    write_oriented_projected_fasta(raw_query,qr,representation,True)
    a=mummer_forward_max(ref,qf,min_len)
    b=mummer_forward_max(ref,qr,min_len)
    return max(a,b),{'forward_max':a,'reverse_raw_projected_max':b}

def brute_lcs(a,b):
    # Synthetic qualification only: O(n^2) dynamic program.
    prev=[0]*(len(b)+1); best=0
    for ca in a:
        cur=[0]*(len(b)+1)
        for j,cb in enumerate(b,1):
            if ca==cb:
                cur[j]=prev[j-1]+1
                if cur[j]>best: best=cur[j]
        prev=cur
    return best

def brute_oriented_max(raw_ref_seq,raw_query_seq,representation):
    r=e.project_sequence(raw_ref_seq,representation)
    qf=e.project_sequence(raw_query_seq,representation)
    qr=e.project_sequence(reverse_complement(raw_query_seq),representation)
    return max(brute_lcs(r,qf),brute_lcs(r,qr)),{
        'forward_max':brute_lcs(r,qf),
        'reverse_raw_projected_max':brute_lcs(r,qr),
    }
