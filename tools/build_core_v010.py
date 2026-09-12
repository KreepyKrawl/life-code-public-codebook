#!/usr/bin/env python3
"""Rebuild the v0.10 public calibration core from immutable v0.8 and v0.0.81.
No primary EXP-0002 files are ingested. Standard library only.
"""
import argparse,csv,hashlib,io,json,sqlite3,zipfile,shutil
from pathlib import Path
PARENT='63910fdf80df38e543cb3b755c60cd3ce146e58140ab7fae9e051153b05b93bb'
ARCHIVE='081ad5bab0cb2c125297b9acb32905fca70f9d09d5e0911f75e91f5a6d9f44e2'
SOURCES={
 'PC1_RAW_RECURRENCE_RESULTS.json':('ART-PC0001-RAW','c31705d4869ec3085444126fd83ad57583a66f52583f928791a4bb75c704c6d5'),
 'PC1_MAXIMAL_BLOCKS_GE24.csv':('ART-PC0001-BLOCKS','d33a8f9033762ff53f78781c5ac104d8e8909f79200faaacc751268265af463f'),
 'TRIPLE_SHARED_16MERS_COMPLETE.csv':('ART-PC0001-TRIPLE16','7684e16d80a302726184c2a6a05f1a7941d356d677318b5d541f093b749423f5')}
STAMP='2026-09-12'
TABLES=['meta','artifacts','taxa','experiments','code_objects','occurrences','edges','measurements','annotations','claims','claim_links']
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,message):
 if not ok:raise ValueError(message)
def records(b):
 out={};key=None
 for line in b.decode().splitlines():
  if line.startswith('>'):key=line[1:].split()[0];require(key not in out,'duplicate FASTA record');out[key]=[]
  elif line.strip():out[key].append(line.strip().upper())
 return {k:''.join(v) for k,v in out.items()}
def snapshot(c):
 return {t:{str(r[0]):dict(r) for r in c.execute('SELECT * FROM '+t+' ORDER BY 1')} for t in TABLES}
def build(parent,archive,out,source_dir):
 require(sha(parent.read_bytes())==PARENT,'parent hash mismatch')
 require(archive.stat().st_size==112174983 and sha(archive.read_bytes())==ARCHIVE,'archive identity mismatch')
 require(not out.exists(),'refusing to overwrite database')
 with zipfile.ZipFile(archive) as z:
  require(z.testzip() is None,'ZIP integrity failure')
  names=[n for n in z.namelist() if n.endswith('/sources/PC1_RAW_RECURRENCE_RESULTS.json')];require(len(names)==1,'archive layout')
  prefix=names[0].removesuffix('PC1_RAW_RECURRENCE_RESULTS.json')
  content={n:z.read(prefix+n) for n in SOURCES}
  for n,(_,h) in SOURCES.items():require(sha(content[n])==h,'source hash mismatch '+n)
  raw=json.loads(content['PC1_RAW_RECURRENCE_RESULTS.json']);focus=raw['focus_cluster']
  genomes={}
  for tax,info in raw['input_validation'].items():
   b=z.read(prefix+Path(info['file']).name);require(sha(b)==info['file_sha256'],'genome input hash '+tax)
   genomes[tax]=records(b)
  words=list(csv.DictReader(io.StringIO(content['TRIPLE_SHARED_16MERS_COMPLETE.csv'].decode())))
  require(len(words)==54 and len({r['sequence'] for r in words})==54,'54 distinct vocabulary records required')
  for word in words:
   seq=word['sequence'];require(len(seq)==16 and set(seq)<=set('ACGT'),'invalid vocabulary literal')
   for tax,col in [('ECOLI','ecoli_occurrences'),('PYRO','pyro_occurrences'),('YEAST','yeast_occurrences')]:
    count=0
    for genome in genomes[tax].values():
     start=genome.find(seq)
     while start!=-1:count+=1;start=genome.find(seq,start+1)
    require(count==int(word[col]),'vocabulary occurrence mismatch '+seq+' '+tax)
  for tax,by_kind in focus['occurrences'].items():
   for kind,locations in by_kind.items():
    literal=focus['core_0001' if kind=='core' else kind]
    for record,start in locations:require(genomes[tax][record][start:start+len(literal)]==literal,'coordinate literal mismatch')
  block_rows=list(csv.DictReader(io.StringIO(content['PC1_MAXIMAL_BLOCKS_GE24.csv'].decode())))
  for kind in ['block_a','block_b']:
   row=next(r for r in block_rows if r['pair']=='ECOLI__PYRO' and r['sequence']==focus[kind])
   require(int(row['length'])==len(focus[kind]),'block table length mismatch')
   for tax,suffix in [('ECOLI','a'),('PYRO','b')]:
    positions=';'.join(f'{rec}:{pos}' for rec,pos in focus['occurrences'][tax][kind])
    require(row['positions_'+suffix]==positions,'block table coordinate mismatch')
 out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(parent,out)
 c=sqlite3.connect(out);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');before=snapshot(c)
 try:
  c.executescript('''
  CREATE TABLE object_aliases(legacy_object_id TEXT PRIMARY KEY,canonical_object_id TEXT NOT NULL REFERENCES code_objects(object_id),reason TEXT NOT NULL);
  CREATE TABLE vocabulary(vocabulary_id TEXT PRIMARY KEY,sequence TEXT NOT NULL UNIQUE,sequence_sha256 TEXT NOT NULL,length_bp INTEGER NOT NULL,entropy_bits REAL NOT NULL,ecoli_occurrences INTEGER NOT NULL,pyro_occurrences INTEGER NOT NULL,yeast_occurrences INTEGER NOT NULL,evidence_state TEXT NOT NULL,evidence_tier TEXT NOT NULL,source_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id));
  CREATE TABLE artifact_links(child_artifact_id TEXT REFERENCES artifacts(artifact_id),parent_artifact_id TEXT REFERENCES artifacts(artifact_id),relation TEXT NOT NULL,PRIMARY KEY(child_artifact_id,parent_artifact_id));
  CREATE TABLE ingest_events(event_id TEXT PRIMARY KEY,event_date TEXT NOT NULL,event_type TEXT NOT NULL,parent_database_sha256 TEXT NOT NULL,archive_sha256 TEXT NOT NULL,validation_json TEXT NOT NULL);
  CREATE TABLE migration_audit(audit_id TEXT PRIMARY KEY,event_id TEXT NOT NULL REFERENCES ingest_events(event_id),table_name TEXT NOT NULL,record_id TEXT NOT NULL,before_json TEXT,after_json TEXT,reason TEXT NOT NULL);
  ''')
  c.executemany('INSERT OR REPLACE INTO meta VALUES(?,?)',[
   ('version','0.10'),('release_date',STAMP),('migration_parent_sha256',PARENT),
   ('old_codebook_status','v0.0.81 archive verified; PC0001 literals, focused occurrences and full 54-word vocabulary reconciled; remaining historical graph pending.'),
   ('release_scope','Released calibration recovery only; no primary EXP-0002 outcomes.'),('occurrence_validation','Exact substrings checked against original hash-verified FASTA records; no cross-record matches.')])
  c.execute("UPDATE artifacts SET source_status='VERIFIED_ARCHIVE_METADATA_ONLY',notes='Original archive size/hash and ZIP integrity verified. Archive bytes remain private; only reviewed calibration sources are exported.' WHERE artifact_id='ART-OLD-CODEBOOK'")
  c.execute("UPDATE artifacts SET notes='Recovered raw evidence linked through ART-PC0001-RAW; original summary retained.' WHERE artifact_id='ART-PC0001'")
  for name,(aid,h) in SOURCES.items():
   c.execute('INSERT INTO artifacts VALUES(?,?,?,?,?,?,?,?)',(aid,name,'Released annotation-blind PC0001 calibration source',h,'FROZEN_CALIBRATION','VERIFIED_BYTES_AND_GENOME_CROSSCHECK',0,'Download: sources/'+name))
   c.execute('INSERT INTO artifact_links VALUES(?,?,?)',(aid,'ART-OLD-CODEBOOK','EXTRACTED_FROM_HASH_VERIFIED_ARCHIVE'))
  c.execute('INSERT INTO artifact_links VALUES(?,?,?)',('ART-PC0001','ART-PC0001-RAW','SUMMARY_SUPPORTED_BY_RAW_RECORD'))
  mapping={'PC1-BLOCK-A24':'PC1-BLOCK-B24','PC1-BLOCK-B25':'PC1-BLOCK-A25'}
  for old,new in mapping.items():
   row=dict(c.execute('SELECT * FROM code_objects WHERE object_id=?',(old,)).fetchone());kind='block_a' if new.endswith('A25') else 'block_b';seq=focus[kind]
   row.update(object_id=new,label='Proof Case 0001 '+kind.replace('_',' '),sequence=seq,sequence_sha256=sha(seq.encode()),length_bp=len(seq),source_artifact_id='ART-PC0001-RAW',data_completeness='SEQUENCE_AND_FOCUSED_OCCURRENCES_VERIFIED',description=('25-bp direct-orientation block A preceding block B in the six frozen neighborhoods.' if kind=='block_a' else '24-bp direct-orientation block B containing the three-domain core at offset 4.'))
   c.execute('INSERT INTO code_objects VALUES('+','.join('?' for _ in row)+')',list(row.values()))
   for field in ['source_object_id','target_object_id']:c.execute(f'UPDATE edges SET {field}=? WHERE {field}=?',(new,old))
   c.execute('INSERT INTO object_aliases VALUES(?,?,?)',(old,new,'v0.8 A/B labels differed from frozen raw source; resolve by block length and identity.'))
  c.execute("UPDATE edges SET source_object_id='PC1-BLOCK-A25',target_object_id='PC1-BLOCK-B24' WHERE edge_id='E-PC1-A-B'")
  c.execute("UPDATE edges SET target_object_id='PC1-BLOCK-A25' WHERE edge_id='E-PC1-MOD-A'")
  c.execute("UPDATE edges SET target_object_id='PC1-BLOCK-B24' WHERE edge_id='E-PC1-MOD-B'")
  c.execute("UPDATE edges SET source_artifact_id='ART-PC0001-RAW' WHERE edge_id LIKE 'E-PC1-%'")
  c.execute("UPDATE edges SET exact_distance_bp=4,notes='Offset of core start within B24, in bases.' WHERE edge_id='E-PC1-CONTAINS'")
  c.execute("DELETE FROM code_objects WHERE object_id IN ('PC1-BLOCK-A24','PC1-BLOCK-B25')")
  seq=focus['core_0001'];c.execute("UPDATE code_objects SET sequence=?,sequence_sha256=?,source_artifact_id='ART-PC0001-RAW',data_completeness='SEQUENCE_AND_FOCUSED_OCCURRENCES_VERIFIED',description='Exact 16-bp core inside B24 at offset 4 in E. coli and Pyrococcus; also observed in yeast chrM.' WHERE object_id='PC1-CORE-16'",(seq,sha(seq.encode())))
  c.execute("UPDATE code_objects SET source_artifact_id='ART-PC0001-RAW',data_completeness='FOCUSED_STRUCTURE_AND_OCCURRENCES_VERIFIED' WHERE object_id='PC1-MODULE-RIBO'")
  for mid,n in [('PC1-M02',len(focus['block_a'])),('PC1-M04',len(focus['block_b']))]:c.execute("UPDATE measurements SET value_num=?,source_artifact_id='ART-PC0001-RAW',notes='A/B identity reconciled to frozen raw recurrence source in Core v0.10.' WHERE measurement_id=?",(n,mid))
  kinds={'block_a':'PC1-BLOCK-A25','block_b':'PC1-BLOCK-B24','core':'PC1-CORE-16'}
  for tax,by_kind in focus['occurrences'].items():
   for kind,locations in by_kind.items():
    oid=kinds[kind];length=len(focus['core_0001' if kind=='core' else kind])
    for record,start in locations:
     ident='OCC-'+sha(f'{oid}|{tax}|{record}|{start}'.encode())[:24]
     assembly='GCF_000007305.1' if tax=='PYRO' else None
     c.execute('INSERT INTO occurrences VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(ident,oid,'TAX-'+tax,assembly,record,start,start+length,'+','0-based half-open; direct input-record orientation','OBSERVED_FROZEN','ART-PC0001-RAW','Genome file SHA-256 and exact substring verified. Assembly accession unknown unless explicitly recoverable from input artifact.'))
  for w in sorted(words,key=lambda r:r['sequence']):
   seq=w['sequence'];c.execute('INSERT INTO vocabulary VALUES(?,?,?,?,?,?,?,?,?,?,?)',('VOC16-'+sha(seq.encode())[:24],seq,sha(seq.encode()),16,float(w['entropy']),int(w['ecoli_occurrences']),int(w['pyro_occurrences']),int(w['yeast_occurrences']),'OBSERVATION','A','ART-PC0001-TRIPLE16'))
  validation={'archive_integrity':'PASS','source_hashes':'PASS','genome_file_hashes':'PASS','focused_coordinate_substrings':'PASS','independent_block_table':'PASS','all_54_vocabulary_counts':'PASS','historical_freeze_times':'NOT_RECONSTRUCTED','exp0002_outcomes_ingested':False}
  c.execute('INSERT INTO ingest_events VALUES(?,?,?,?,?,?)',('INGEST-PC1-20260912',STAMP,'VERIFIED_RECOVERY',PARENT,ARCHIVE,json.dumps(validation,sort_keys=True)))
  after=snapshot(c)
  for table in TABLES:
   for key in sorted(before[table].keys()|after[table].keys()):
    a,b=before[table].get(key),after[table].get(key)
    if a!=b:c.execute('INSERT INTO migration_audit VALUES(?,?,?,?,?,?,?)',('AUDIT-'+sha((table+'|'+key).encode())[:24],'INGEST-PC1-20260912',table,key,json.dumps(a,sort_keys=True) if a else None,json.dumps(b,sort_keys=True) if b else None,'Verified archive recovery; parent release preserved unchanged.'))
  for table in ['vocabulary','object_aliases','artifact_links']:
   for r in c.execute('SELECT * FROM '+table+' ORDER BY 1').fetchall():
    key='|'.join(str(v) for v in tuple(r)[:2]);c.execute('INSERT INTO migration_audit VALUES(?,?,?,?,?,?,?)',('AUDIT-'+sha((table+'|'+key).encode())[:24],'INGEST-PC1-20260912',table,key,None,json.dumps(dict(r),sort_keys=True),'Add source-derived recovery record.'))
  for table in ['migration_audit','ingest_events']:
   for op in ['UPDATE','DELETE']:
    c.execute(f"CREATE TRIGGER immutable_{table}_{op} BEFORE {op} ON {table} BEGIN SELECT RAISE(ABORT,'append-only audit'); END")
  require(not list(c.execute('PRAGMA foreign_key_check')),'foreign key failure')
  c.commit()
 except BaseException:
  c.close();out.unlink(missing_ok=True);raise
 c.close();source_dir.mkdir(parents=True,exist_ok=True)
 for name,b in content.items():(source_dir/name).write_bytes(b)
 print(json.dumps({'database':str(out),'sha256':sha(out.read_bytes()),'vocabulary':54,'focused_occurrences':19,'validation':validation},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--parent',type=Path,required=True);p.add_argument('--archive',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--sources',type=Path,required=True);a=p.parse_args();build(a.parent,a.archive,a.output,a.sources)
