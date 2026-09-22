#!/usr/bin/env python3
import csv,hashlib,json,re,subprocess,zipfile
from collections import defaultdict,Counter
from pathlib import Path

K=16
MIN_D=16
MAX_D=10000
EXPECTED={
 ('ECOLI','PYRO','YEAST'):{'shared':2462,'modules':540},
 ('ECOLI','YEAST','PYRO'):{'shared':19112,'modules':989},
 ('PYRO','YEAST','ECOLI'):{'shared':16479,'modules':1395},
}
INPUTS={
 'ECOLI':('GCF_000005845.2','53bb6a51b6e92139ced1e38f74b7938781027c52200922ff03718c2237d23bb4'),
 'YEAST':('GCF_000146045.2','fe42735d3e6242f8c40b457a232940e34ef15eb4502717e54a34ed118face4c1'),
 'PYRO':('GCF_000007305.1','e9c87294756c7cfc15e61aa067c2169a8513ac755bce4a3d1f3eedf385cffa76'),
}
MAPS={
 'RY':str.maketrans({'A':'0','G':'0','C':'1','T':'1'}),
 'MK':str.maketrans({'A':'0','C':'0','G':'1','T':'1'}),
 'WS':str.maketrans({'A':'0','T':'0','G':'1','C':'1'}),
}

def sha256(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def reacquire(label,work):
 accession,expected=INPUTS[label]
 zpath=work/f'{label}.zip'; pkg=work/f'{label}_pkg'
 subprocess.run(['datasets','download','genome','accession',accession,'--include','genome','--filename',str(zpath)],check=True)
 with zipfile.ZipFile(zpath) as z:z.extractall(pkg)
 hits=list(pkg.rglob('*_genomic.fna'))
 if len(hits)!=1:raise SystemExit(f'{label}: expected one genomic FASTA, found {len(hits)}')
 got=sha256(hits[0])
 if got!=expected:raise SystemExit(f'{label}: RAW_SHA_MISMATCH expected={expected} got={got}')
 return hits[0],got

def read_runs(path):
 out=[];name=None;seq=[]
 def flush(name,seq):
  if name is None:return
  s=''.join(seq).upper()
  for i,x in enumerate(z for z in re.split(r'[^ACGT]+',s) if z):
   if len(x)>=K:out.append((f'{name}#{i}',x))
 with open(path,encoding='utf-8',errors='replace') as f:
  for line in f:
   line=line.strip()
   if not line:continue
   if line.startswith('>'):
    flush(name,seq);name=line[1:].split()[0];seq=[]
   else:seq.append(line)
 flush(name,seq)
 return out

def bases(records):return sum(len(s) for _,s in records)

def kmer_set(records):
 return {s[i:i+K] for _,s in records for i in range(len(s)-K+1)}

def shared_words(a,b):
 small,big=(a,b) if bases(a)<=bases(b) else (b,a)
 ks=kmer_set(small); shared=set()
 for _,s in big:
  for i in range(len(s)-K+1):
   w=s[i:i+K]
   if w in ks:shared.add(w)
 return shared

def module_set(records,allowed):
 byrec=defaultdict(list)
 for rid,s in records:
  arr=[]
  for i in range(len(s)-K+1):
   w=s[i:i+K]
   if w in allowed:arr.append((i,w))
  byrec[rid]=arr
 mods=set()
 for arr in byrec.values():
  n=len(arr)
  for i,(pi,a) in enumerate(arr):
   j=i+1
   while j<n and arr[j][0]-pi<MIN_D:j+=1
   while j<n:
    d=arr[j][0]-pi
    if d>MAX_D:break
    b=arr[j][1]
    if a!=b:mods.add((a,b))
    j+=1
 return mods

def project_word(w,q):return w.translate(MAPS[q])

def projected_relations(records,pmods,q):
 A={a for a,b in pmods};B={b for a,b in pmods};allowed=A|B;t=MAPS[q];rels=set()
 for rid,s in records:
  bs=s.translate(t);arr=[]
  for i in range(len(bs)-K+1):
   w=bs[i:i+K]
   if w in allowed:arr.append((i,w))
  n=len(arr)
  for i,(pi,a) in enumerate(arr):
   if a not in A:continue
   j=i+1
   while j<n and arr[j][0]-pi<MIN_D:j+=1
   while j<n:
    d=arr[j][0]-pi
    if d>MAX_D:break
    b=arr[j][1]
    if b in B:rels.add((a,b))
    j+=1
 return rels

def rescue(train_mods,held,q):
 coll=Counter((project_word(a,q),project_word(b,q)) for a,b in train_mods)
 pmods=set(coll);rels=projected_relations(held,pmods,q);hit=pmods&rels
 source=sum(n for m,n in coll.items() if m in rels)
 return {
  'source_modules':len(train_mods),'unique_projected_modules':len(pmods),
  'rescued_source':source,'rescued_unique':len(hit),
  'source_rescue_fraction':source/len(train_mods),
  'unique_rescue_fraction':len(hit)/len(pmods),
  'max_collision':max(coll.values()),'mean_collision':sum(coll.values())/len(coll),
  'heldout_projected_relation_count':len(rels),
 }

def main():
 work=Path('rcx-lcx-0001-work');work.mkdir(exist_ok=True)
 manifest={};records={}
 for label in ('ECOLI','PYRO','YEAST'):
  p,h=reacquire(label,work);records[label]=read_runs(p)
  manifest[label]={'accession':INPUTS[label][0],'raw_sha256':h,'analysis_runs':len(records[label]),'acgt_bases':bases(records[label])}
 folds={};pre={}
 for a,b,h in EXPECTED:
  shared=shared_words(records[a],records[b])
  ma=module_set(records[a],shared);mb=module_set(records[b],shared);mods=ma&mb
  got={'shared':len(shared),'modules':len(mods)};exp=EXPECTED[(a,b,h)]
  pre[f'{a}+{b}->{h}']={'got':got,'expected':exp,'pass':got==exp}
  folds[(a,b,h)]=mods
 if not all(v['pass'] for v in pre.values()):
  out={'experiment':'RCX-LCX-0001','stage':'A_REAL_SCREEN','status':'BLOCKED_BASELINE_MISMATCH','inputs':manifest,'precheck':pre}
  Path('rcx-lcx-0001-results.json').write_text(json.dumps(out,indent=2))
  raise SystemExit('BASELINE_MISMATCH: quotient scoring forbidden')
 print('BASELINE REPRODUCTION PASS')
 rows=[]
 for (a,b,h),mods in folds.items():
  for q in ('RY','MK','WS'):
   r={'fold':f'{a}+{b}->{h}','quotient':q,**rescue(mods,records[h],q)}
   rows.append(r);print(json.dumps(r,sort_keys=True))
 any_rescue=any(r['rescued_source'] or r['rescued_unique'] for r in rows)
 status='REAL_RESCUE_REQUIRES_NULL' if any_rescue else 'DECISIVE_NO_REAL_RESCUE'
 out={
  'experiment':'RCX-LCX-0001','stage':'A_REAL_SCREEN','status':status,
  'inputs':manifest,'precheck':pre,'results':rows,
  'nulls_executed':False,
  'next_step':'Run frozen null/conditioning stage only for observed rescue signals.' if any_rescue else 'Stage A stops: zero real rescue cannot have positive excess over a nonnegative null.'
 }
 Path('rcx-lcx-0001-results.json').write_text(json.dumps(out,indent=2))
 Path('rcx-lcx-0001-sha256.txt').write_text(f"{sha256(Path('rcx-lcx-0001-results.json'))}  rcx-lcx-0001-results.json\n")
 print('STATUS',status)
if __name__=='__main__':main()
