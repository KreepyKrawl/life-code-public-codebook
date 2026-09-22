#!/usr/bin/env python3
import argparse,csv,hashlib,json,subprocess,sys
from pathlib import Path

EXPECTED_NORMALIZER_SHA256='f705448fa0dfc20aed7a4a3fa3023eb79d5a1bbbcb4b75d0489a8481ca587712'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()

def binding(tsv,assembly_id):
    with open(tsv,newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f,delimiter='\t'):
            if r['assembly_id']==assembly_id:
                return r
    raise SystemExit(f'assembly not in frozen binding: {assembly_id}')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--assembly-id',required=True)
    ap.add_argument('--binding',default='cloud/FROZEN_CORPUS_BINDING.tsv')
    ap.add_argument('--work',default='work')
    ap.add_argument('--normalizer',default='cloud/canonical/v0.1.33/exp0002_normalize_fasta.py')
    ap.add_argument('--out',default='normalization-verify-result.json')
    a=ap.parse_args()

    normalizer=Path(a.normalizer)
    actual_normalizer_sha=sha256(normalizer)
    if actual_normalizer_sha!=EXPECTED_NORMALIZER_SHA256:
        raise SystemExit(f'CANONICAL_NORMALIZER_SHA_MISMATCH {actual_normalizer_sha}')

    row=binding(a.binding,a.assembly_id)
    work=Path(a.work)
    hits=list((work/'package').rglob('*_genomic.fna'))
    if len(hits)!=1:
        raise SystemExit(f'expected one reacquired genomic FASTA, found {len(hits)}')
    raw=hits[0]
    raw_sha=sha256(raw)
    if raw_sha!=row['raw_fasta_sha256']:
        raise SystemExit(f'RAW_SHA_MISMATCH {raw_sha}')

    outdir=work/'canonical_normalization'
    outdir.mkdir(parents=True,exist_ok=True)
    fasta=outdir/f'{a.assembly_id}.normalized.fasta'
    cmap=outdir/f'{a.assembly_id}.coordinate_map.tsv'
    report=outdir/f'{a.assembly_id}.normalization_report.json'
    subprocess.run([sys.executable,str(normalizer),'--raw',str(raw),'--out-fasta',str(fasta),'--out-map',str(cmap),'--out-report',str(report)],check=True)

    norm_sha=sha256(fasta)
    map_sha=sha256(cmap)
    norm_ok=norm_sha==row['normalized_fasta_sha256']
    map_ok=map_sha==row['coordinate_map_sha256']
    result={
        'schema':'LIFE_CODE_CANONICAL_NORMALIZATION_VERIFY_V1',
        'assembly_id':a.assembly_id,
        'accession':row['accession'],
        'canonical_normalizer_sha256':actual_normalizer_sha,
        'raw_fasta_sha256':raw_sha,
        'expected_normalized_fasta_sha256':row['normalized_fasta_sha256'],
        'actual_normalized_fasta_sha256':norm_sha,
        'expected_coordinate_map_sha256':row['coordinate_map_sha256'],
        'actual_coordinate_map_sha256':map_sha,
        'normalized_fasta_match':norm_ok,
        'coordinate_map_match':map_ok,
        'status':'PASS' if norm_ok and map_ok else 'FAIL'
    }
    Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True))
    if result['status']!='PASS':
        raise SystemExit('CANONICAL_NORMALIZATION_MISMATCH')

if __name__=='__main__':
    main()
