#!/usr/bin/env python3
"""Lossless historical research ingestion under an explicit source-hash release manifest."""
import argparse,hashlib,json,re,shutil,sqlite3,zipfile
from pathlib import Path
PARENT='31b6c0deb4ad90448afe10bfa30768a63fcca690b316a3f75351d407e6df9dd9'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def refs(x):
 out=set()
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['source_refs','source']:
    for n in v if isinstance(v,list) else [v]:
     if isinstance(n,str):out.add(n)
   out|=refs(v)
 elif isinstance(x,list):
  for v in x:out|=refs(v)
 return out
def build(root,archive):
 m=json.loads((root/'research/release_manifest_v0.11.json').read_text());guide=json.loads((root/'research/reading_guide.json').read_text())
 require(sha(archive.read_bytes())==m['archive_sha256'],'archive hash')
 parent=root/'downloads/LIFE_CODE_CODEBOOK_CORE_v0.10.sqlite';require(sha(parent.read_bytes())==PARENT,'parent identity')
 out=root/'downloads/LIFE_CODE_CODEBOOK_CORE_v0.11.sqlite';require(not out.exists(),'refusing to overwrite')
 payloads={};source_bytes={}
 with zipfile.ZipFile(archive) as z:
  require(z.testzip() is None,'archive integrity');prefix=next(n for n in z.namelist() if n.endswith('/entries/LC-CORE-0001.json')).removesuffix('entries/LC-CORE-0001.json')
  for row in m['reviewed_records']:
   b=z.read(prefix+row['path']);require(sha(b)==row['sha256'],'record hash');j=json.loads(b)
   require(not re.search(r'EXP[-_ ]?0*2\b|SEALED_RESULT|LC-OBS-A[123]|\bA[123]\b',json.dumps(j),re.I),'sensitive record')
   payloads[row['path']]=(b,j)
  for row in m['sources']:
   b=z.read(prefix+row['archive_path']);require(sha(b)==row['sha256'],'source hash')
   if row['release_state']=='PUBLISHED':
    require(not re.search(r'EXP[-_ ]?0*2\b|SEALED_RESULT|LC-OBS-A[123]|\bA[123]\b',b.decode(),re.I),'source disclosure conflict '+row['name']);source_bytes[row['name']]=b
 shutil.copyfile(parent,out);c=sqlite3.connect(out);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON')
 c.executescript('''
 CREATE TABLE research_records(record_id TEXT PRIMARY KEY,kind TEXT NOT NULL,status TEXT NOT NULL,record_type TEXT NOT NULL,archive_version TEXT NOT NULL,source_path TEXT NOT NULL,source_sha256 TEXT NOT NULL,original_json TEXT NOT NULL);
 CREATE TABLE research_assertions(assertion_id TEXT PRIMARY KEY,record_id TEXT NOT NULL REFERENCES research_records(record_id),ordinal INTEGER NOT NULL,evidence_class TEXT NOT NULL,statement TEXT NOT NULL);
 CREATE TABLE research_sources(source_name TEXT PRIMARY KEY,archive_path TEXT NOT NULL,sha256 TEXT NOT NULL,bytes INTEGER NOT NULL,release_state TEXT NOT NULL);
 CREATE TABLE research_record_sources(record_id TEXT REFERENCES research_records(record_id),source_name TEXT REFERENCES research_sources(source_name),PRIMARY KEY(record_id,source_name));
 CREATE TABLE research_links(source_id TEXT REFERENCES research_records(record_id),target_id TEXT NOT NULL,relation TEXT NOT NULL,target_state TEXT NOT NULL,PRIMARY KEY(source_id,target_id,relation));
 CREATE TABLE research_reading_guide(guide_id TEXT PRIMARY KEY,ordinal INTEGER NOT NULL,title TEXT NOT NULL,plain_explanation TEXT NOT NULL,record_ids_json TEXT NOT NULL,layer_role TEXT NOT NULL);
 CREATE TABLE research_ingests(ingest_id TEXT PRIMARY KEY,parent_sha256 TEXT NOT NULL,archive_sha256 TEXT NOT NULL,manifest_sha256 TEXT NOT NULL,scope TEXT NOT NULL);
 ''')
 ids={j.get('entry_id',j.get('prediction_id')) for b,j in payloads.values()}
 for row in m['sources']:c.execute('INSERT INTO research_sources VALUES(?,?,?,?,?)',(row['name'],row['archive_path'],row['sha256'],row['bytes'],row['release_state']))
 for row in m['reviewed_records']:
  b,j=payloads[row['path']];rid=j.get('entry_id',j.get('prediction_id'));c.execute('INSERT INTO research_records VALUES(?,?,?,?,?,?,?,?)',(rid,row['kind'],j['status'],j.get('entry_type','PRED'),m['archive_version'],row['path'],row['sha256'],b.decode()))
  statements=j.get('evidence',[{'class':j.get('evidence_class','P1'),'statement':j.get('statement','')}])
  for i,e in enumerate(statements):c.execute('INSERT INTO research_assertions VALUES(?,?,?,?,?)',(rid+'-'+str(i),rid,i,e['class'],e['statement']))
  for n in sorted(refs(j)):c.execute('INSERT INTO research_record_sources VALUES(?,?)',(rid,n))
 for row in m['reviewed_records']:
  b,j=payloads[row['path']];rid=j.get('entry_id',j.get('prediction_id'))
  for field in ['relationships','predictions','dependencies']:
   for tid in j.get(field,[]):
    if isinstance(tid,str) and tid.startswith('LC-'):c.execute('INSERT OR IGNORE INTO research_links VALUES(?,?,?,?)',(rid,tid,field,'PUBLISHED' if tid in ids else 'NOT_IN_PUBLIC_RESEARCH_RELEASE'))
 for i,g in enumerate(guide):
  require(set(g['records'])<=ids,'guide has unresolved records');c.execute('INSERT INTO research_reading_guide VALUES(?,?,?,?,?,?)',(g['id'],i,g['title'],g['plain'],json.dumps(g['records']),'NONCANONICAL_EXPLANATION_LINKED_TO_ARCHIVE_RECORDS'))
 c.execute('INSERT INTO research_ingests VALUES(?,?,?,?,?)',('ARCHIVE-RESEARCH-20260912',PARENT,m['archive_sha256'],sha((root/'research/release_manifest_v0.11.json').read_bytes()),m['scope']))
 c.execute("UPDATE meta SET value='0.11' WHERE key='version'")
 c.execute("INSERT OR REPLACE INTO meta VALUES('research_scope',?)",('113 original historical records published losslessly with original evidence classes and status; 7 records held from public release. Historical results not rerun.',))
 for table in ['research_records','research_assertions','research_sources','research_record_sources','research_links','research_reading_guide','research_ingests']:
  for op in ['UPDATE','DELETE']:c.execute(f"CREATE TRIGGER immutable_{table}_{op} BEFORE {op} ON {table} BEGIN SELECT RAISE(ABORT,'immutable historical release'); END")
 require(not list(c.execute('PRAGMA foreign_key_check')),'foreign key integrity');c.commit()
 data={t:[dict(r) for r in c.execute('SELECT * FROM '+t+' ORDER BY '+('ordinal' if t=='research_reading_guide' else '1'))] for t in ['research_records','research_assertions','research_sources','research_record_sources','research_links','research_reading_guide','research_ingests']};c.close()
 data['metadata']={'schema':'LIFE_CODE_RESEARCH_SNAPSHOT_v0.11','archive_version':m['archive_version'],'source_database':out.name,'source_database_sha256':sha(out.read_bytes()),'held_record_count':m['held_record_count'],'historical_status_note':'Statuses and numeric results are preserved from archive v0.0.81. No experiments were rerun for this publication.'}
 data['counts']={t:len(v) for t,v in data.items() if isinstance(v,list)}
 core=json.loads((root/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.10.json').read_text())
 core['snapshot_schema']='LIFE_CODE_PUBLIC_SNAPSHOT_v0.11'
 core['source_database']['filename']=out.name;core['source_database']['sha256']=sha(out.read_bytes())
 conn=sqlite3.connect(out);core['source_database']['database_meta']=dict(conn.execute('SELECT key,value FROM meta'));conn.close()
 core['extension_snapshots']={'historical_research':'data/LIFE_CODE_RESEARCH_v0.11.json'}
 (root/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.11.json').write_text(json.dumps(core,indent=2,ensure_ascii=False)+'\n')
 (root/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.11.js').write_text('window.LIFE_CODE_SNAPSHOT='+json.dumps(core,separators=(',',':'),ensure_ascii=False)+';\n')
 (root/'data/LIFE_CODE_RESEARCH_v0.11.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');(root/'data/LIFE_CODE_RESEARCH_v0.11.js').write_text('window.LIFE_CODE_RESEARCH='+json.dumps(data,separators=(',',':'),ensure_ascii=False)+';\n')
 for path,(b,j) in payloads.items():
  p=root/'research'/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 for name,b in source_bytes.items():
  p=root/'research/sources'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 print(json.dumps(data['counts'],indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--archive',type=Path,required=True);a=p.parse_args();build(a.root,a.archive)
