#!/usr/bin/env python3
import argparse,csv,hashlib,json,os,subprocess,zipfile
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def binding(tsv,assembly_id):
    with open(tsv,newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f,delimiter='\t'):
            if r['assembly_id']==assembly_id:return r
    raise SystemExit(f'assembly not in frozen binding: {assembly_id}')

def normalize(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    seg=0; rec=None; seq=[]
    def emit_record(name,s,out):
        nonlocal seg
        run=[]; start=0
        for i,ch in enumerate(s.upper()+'!'):
            if ch in 'ACGT':
                if not run:start=i
                run.append(ch)
            elif run:
                seg+=1
                end=i
                out.write(f'>{name}|segment={seg}|source_start={start+1}|source_end={end}\n')
                out.write(''.join(run)+'\n')
                run=[]
    with open(src,'rt',encoding='ascii',errors='strict') as inp, open(dst,'wt',encoding='ascii',newline='\n') as out:
        for raw in inp:
            if raw.startswith('>'):
                if rec is not None: emit_record(rec,''.join(seq),out)
                rec=raw[1:].strip().split()[0];seq=[]
            else: seq.append(raw.strip())
        if rec is not None: emit_record(rec,''.join(seq),out)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--assembly-id',required=True)
    ap.add_argument('--binding',default='cloud/FROZEN_CORPUS_BINDING.tsv')
    ap.add_argument('--work',default='work')
    a=ap.parse_args(); row=binding(a.binding,a.assembly_id); w=Path(a.work);w.mkdir(parents=True,exist_ok=True)
    accession=row['accession']; archive=w/f'{a.assembly_id}.zip'
    subprocess.run(['datasets','download','genome','accession',accession,'--include','genome','--filename',str(archive)],check=True)
    with zipfile.ZipFile(archive) as z:z.extractall(w/'package')
    hits=list((w/'package').rglob('*_genomic.fna'))
    if len(hits)!=1: raise SystemExit(f'expected one genomic FASTA, found {len(hits)}')
    raw=hits[0]; raw_sha=sha256(raw)
    if raw_sha!=row['raw_fasta_sha256']: raise SystemExit(f'RAW_SHA_MISMATCH {raw_sha}')
    norm=w/f'{a.assembly_id}.normalized.fasta';normalize(raw,norm); norm_sha=sha256(norm)
    if norm_sha!=row['normalized_fasta_sha256']: raise SystemExit(f'NORMALIZED_SHA_MISMATCH {norm_sha}')
    result={'schema':'LIFE_CODE_REACQUIRE_NORMALIZE_V1','assembly_id':a.assembly_id,'accession':accession,'raw_sha256':raw_sha,'normalized_sha256':norm_sha,'status':'PASS','normalized_path':str(norm)}
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
