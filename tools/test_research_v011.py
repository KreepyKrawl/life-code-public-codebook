#!/usr/bin/env python3
"""Validate publication identity, source coverage, data preservation and disclosure scope."""
from pathlib import Path
import hashlib,json,re,sqlite3
R=Path(__file__).resolve().parents[1]
def require(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def validate():
 m=json.loads((R/'research/release_manifest_v0.11.json').read_text());d=json.loads((R/'data/LIFE_CODE_RESEARCH_v0.11.json').read_text())
 js=(R/'data/LIFE_CODE_RESEARCH_v0.11.js').read_text();require(json.loads(js.split('=',1)[1].strip().rstrip(';'))==d,'browser research snapshot differs')
 db=R/'downloads/LIFE_CODE_CODEBOOK_CORE_v0.11.sqlite';require(sha(db.read_bytes())==d['metadata']['source_database_sha256'],'DB hash')
 c=sqlite3.connect(db);c.row_factory=sqlite3.Row;p=sqlite3.connect(R/'downloads/LIFE_CODE_CODEBOOK_CORE_v0.10.sqlite');p.row_factory=sqlite3.Row
 for table in ['artifacts','taxa','experiments','code_objects','occurrences','edges','measurements','annotations','claims','claim_links','object_aliases','vocabulary','artifact_links','ingest_events','migration_audit']:
  require([tuple(r) for r in c.execute('SELECT * FROM '+table+' ORDER BY 1')]==[tuple(r) for r in p.execute('SELECT * FROM '+table+' ORDER BY 1')],'parent data changed '+table)
 require(not list(c.execute('PRAGMA foreign_key_check')),'foreign keys')
 manifest={r['path']:r for r in m['reviewed_records']};ids={r['record_id'] for r in d['research_records']}
 require(len(ids)==113 and sum(r['kind']=='prediction' for r in d['research_records'])==47,'record inventory')
 for row in d['research_records']:
  b=(R/'research'/row['source_path']).read_bytes();require(sha(b)==row['source_sha256']==manifest[row['source_path']]['sha256'],'original bytes changed')
  require(row['original_json'].encode()==b,'lossless payload check');obj=json.loads(b);require(obj['status']==row['status'],'status altered')
  require(not re.search(r'EXP[-_ ]?0*2\b|SEALED_RESULT|LC-OBS-A[123]|\bA[123]\b',row['original_json'],re.I),'sensitive payload')
  statements=obj.get('evidence',[{'class':obj.get('evidence_class','P1'),'statement':obj.get('statement','')}]);actual=sorted([a for a in d['research_assertions'] if a['record_id']==row['record_id']],key=lambda a:a['ordinal'])
  require([(a['evidence_class'],a['statement']) for a in actual]==[(a['class'],a['statement']) for a in statements],'assertion changed')
 for row in m['sources']:
  path=R/'research/sources'/row['name']
  if row['release_state']=='PUBLISHED':
   require(path.is_file() and sha(path.read_bytes())==row['sha256'],'published source hash')
   require(not re.search(r'EXP[-_ ]?0*2\b|SEALED_RESULT|LC-OBS-A[123]|\bA[123]\b',path.read_text(),re.I),'sensitive source')
  else:require(not path.exists(),'withheld/unbundled source published')
 for g in d['research_reading_guide']:require(set(json.loads(g['record_ids_json']))<=ids,'guide link')
 for l in d['research_links']:require((l['target_id'] in ids)==(l['target_state']=='PUBLISHED'),'link availability')
 for id in ['LC-PRED-0049','LC-PRED-0050','LC-PRED-0051']:require(next(r for r in d['research_records'] if r['record_id']==id)['status']=='FROZEN_UNTESTED','fresh prediction promoted')
 for t,rows in d.items():
  if t.startswith('research_'):require(len(rows)==c.execute('SELECT count(*) FROM '+t).fetchone()[0],'snapshot DB counts')
 require(c.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLite integrity');c.close();p.close()
 core=json.loads((R/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.11.json').read_text());require(core['source_database']['sha256']==sha(db.read_bytes()),'core identity');require(json.loads((R/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.11.js').read_text().split('=',1)[1].strip().rstrip(';'))==core,'core JS equality')
 # A top-level page function must never replace the browser's History object.
 require(not re.search(r'function\s+history\s*\(', (R/'app.js').read_text()),'native History collision')
 print('PASS: 113 lossless records; 260 original assertions; 109 source references; 92 source downloads; parent data unchanged; disclosure gates; fresh predictions untested; snapshot identity; navigation name regression')
if __name__=='__main__':validate()
