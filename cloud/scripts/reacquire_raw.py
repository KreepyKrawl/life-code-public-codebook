#!/usr/bin/env python3
import argparse,csv,hashlib,json,subprocess,zipfile
from pathlib import Path


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
    ap.add_argument('--out',default='raw-verify-result.json')
    a=ap.parse_args()

    row=binding(a.binding,a.assembly_id)
    work=Path(a.work); work.mkdir(parents=True,exist_ok=True)
    archive=work/f'{a.assembly_id}.zip'
    subprocess.run([
        'datasets','download','genome','accession',row['accession'],
        '--include','genome','--filename',str(archive)
    ],check=True)

    package=work/'package'
    with zipfile.ZipFile(archive) as z:
        z.extractall(package)
    hits=list(package.rglob('*_genomic.fna'))
    if len(hits)!=1:
        raise SystemExit(f'expected one genomic FASTA, found {len(hits)}')

    raw=hits[0]
    actual=sha256(raw)
    expected=row['raw_fasta_sha256']
    status='PASS' if actual==expected else 'FAIL'
    result={
        'schema':'LIFE_CODE_RAW_REACQUISITION_V1',
        'assembly_id':a.assembly_id,
        'accession':row['accession'],
        'expected_raw_fasta_sha256':expected,
        'actual_raw_fasta_sha256':actual,
        'raw_bytes':raw.stat().st_size,
        'status':status
    }
    Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True))
    if status!='PASS':
        raise SystemExit('RAW_SHA_MISMATCH')


if __name__=='__main__':
    main()
