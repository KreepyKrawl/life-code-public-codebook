#!/usr/bin/env python3
import argparse,csv,hashlib,json,subprocess,zipfile
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
    result={
      'schema':'LIFE_CODE_REACQUIRE_RAW_V1',
      'assembly_id':a.assembly_id,
      'accession':accession,
      'raw_sha256':raw_sha,
      'expected_normalized_sha256':row['normalized_fasta_sha256'],
      'expected_coordinate_map_sha256':row['coordinate_map_sha256'],
      'status':'RAW_VERIFIED_CANONICAL_NORMALIZER_REQUIRED',
      'raw_path':str(raw)
    }
    print(json.dumps(result,sort_keys=True))
    raise SystemExit('RAW VERIFIED. STOP: canonical v0.1.33 normalizer source is not yet online; normalization may not be reconstructed from memory.')
if __name__=='__main__':main()
